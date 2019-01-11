#! /bin/bash
#
# Procdura di calibrazione automatica
# per lo strumento di misura PM
# $1 grandezza da calibrare  PM2.5 o PM10
# $2 vettore esclusioni punti 
#
dir=/home/pi/alfetta/calibration
webdir=/var/www/html/alfetta
#rm $wedir/errorcal
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
# Avvia calcolo regressione lineare escludendo i valori indicati in $2
sleep .2
if ! $dir/autocalibration.py $1 $2 ; then
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

