#! /bin/bash
rm reference$3.log
rm datalog$3.log
rm tempfile
rm tempfile1
#for d in {$2..0}
for (( d=$2; d>=0; d-- ))
do 
    echo $d
    file=$(LC_ALL=en_IE.utf8 date "+%a-%d-%b-%Y" -d "-$d days")_datalog.log
    echo $d $file
    wget -O tempfile  http://94.177.187.133/$1/datalogs/$file
    cat tempfile >> reference$3.log
    wget -O tempfile1  http://localhost/alfetta/datalogs/$file
    cat tempfile1 >> datalog$3.log
done 
