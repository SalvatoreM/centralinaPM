<?php

$lista["host"]=array();
$af = fopen("/home/pi/alfetta/etc/alfetta.conf", "r") or die("Unable to open file!");
while(!feof($af)) {
   $l=fgets($af);
   if ($l){
      if (explode("=",$l)[0]=="host"){
         array_push($lista[explode("=",$l)[0]],str_replace("\n","",explode("=",$l)[1]));
      }
      else {$lista[explode("=",$l)[0]]=str_replace("\n","",explode("=",$l)[1]); }
   }
}
fclose($af);
foreach ($lista["host"] as $h){
   echo($h."\n");
}
?>
