<?php
$path="/home/pi/alfetta/check.sh";
$s='echo "'.$path.'" >/var/www/html/alfetta/comandi/comando.sh';
//echo $s;
exec($s,$return);
exec('cat /var/www/html/alfetta/process.log 2>&1',$r,$return);
foreach ($r as $l){ echo $l;}
?>
