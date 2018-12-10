<?php
$path="/home/pi/alfetta/var/log/datalog.log";
$s='echo "tail -n 64 '.$path.' > /var/www/html/alfetta/rtdata" >/var/www/html/alfetta/comandi/comando.sh';
//echo $s;
exec($s,$return);
exec('cat /var/www/html/alfetta/rtdata 2>&1',$r,$return);
foreach ($r as $l){ echo $l."\n";}
?>
