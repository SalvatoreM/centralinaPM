<?php
$af = fopen("sensor.log", "r") or die("Unable to open file!");
while(!feof($af)) {
   $l=fgets($af);
   if ($l){
      echo "SDS011 ".str_replace("\n","",$l); }
}
fclose($af);
?>
