#! /bin/bash
#
# Procdura di calibrazione automatica
# per lo strumento di misura PM
# $1  Riferimento strumento campione  ex FI::Firenze-Test01
# $2  Numero giorni da considerare 1 - N
# $3 grandezza da calibrare  PM2.5 o PM10
#
dir=/home/pi/alfetta/calibration
webdir=/var/www/html/alfetta
#rm $wedir/errorcal
if [ -e $dir/reference$3.log ]
then
   rm $dir/reference$3.log
fi
if [ -e $dir/datalog$3.log ]
then
   rm $dir/datalog$3.log
fi
if [ -e $dir/tempfile ]
then
   rm $dir/tempfile
fi
if [ -e $dir/tempfile1 ]
then
   rm $dir/tempfile1
fi
if [ -e $webdir/regressione ] 
then
   rm $webdir/regressione
fi
if [ -e $webdir/distribution ]
then
   rm $webdir/distribution
fi
if [ -e $webdir/coefficient ]
then 
   rm $webdir/coefficient
fi
#touch $dir/datalog$3.log
#touch $dir/reference$3.log
for (( d=$2; d>=0; d-- ))
do
#    echo $d >> /home/pi/alfetta/calibration/autocalibration.log
    file=$(LC_ALL=en_IE.utf8 date "+%a-%d-%b-%Y" -d "-$d days")_datalog.log

    echo  $d $file >> /home/pi/alfetta/calibration/autocalibration.log
    if ! wget -q -O $dir/tempfile  http://94.177.187.133/$1/datalogs/$file ; then
      echo "Lettura dati remoti non riuscita " > $webdir/errorcal
      exit 1
    fi
    cat $dir/tempfile >> $dir/reference$3.log
    rm $dir/tempfile

    if ! wget -q -O $dir/tempfile1  http://localhost/alfetta/datalogs/$file ; then
      echo "Lettura dati locali non Riuscita " > $webdir/errorcal
      exit 1
    fi
    cat $dir/tempfile1 >> $dir/datalog$3.log
    rm $dir/tempfile1
done
# Avvia calcolo regressione lineare
sleep .2
if ! $dir/autocalibration.py $3 ; then
   echo "Calibrazione non eseguita per errore sui dati" > $webdir/errorcal
   exit 1
else
   echo "OK Calibrazione Eseguita" > $webdir/errorcal
fi   
#if ! ./autocalibration.py ; then 
#   echo "pkill sds011.py"
#   echo '/home/pi/alfetta/sds011.py'
#fi
date

