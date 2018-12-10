<?php
$path="/home/pi/alfetta/";
if ($_GET["op"]=="start") {
   $s='echo "'.$path.'sds_start.sh" >/var/www/html/alfetta/comandi/comando.sh';
}
if ($_GET["op"]=="stop") {
   $s='echo "'.$path.'sds_stop.sh" >/var/www/html/alfetta/comandi/comando.sh';
}
exec($s,$return);
usleep(100000);
exec('cat /var/www/html/alfetta/result.log 2>&1',$r,$return);
foreach ($r as $l){ echo $l;}
?>
