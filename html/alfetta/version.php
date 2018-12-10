<?php
$af = fopen("version.log", "r") or die("Unable to open file!");
//$l=fgets($af);
while(!feof($af)) {
   $line=fgets($af);
   if ( strpos($line,"#") === FALSE  && strlen($line) > 1) {
      echo ($line);
   }   
}
fclose($af);
?>
