<?php
$path="/var/www/html/alfetta/";
$s='echo "rm '.$path.'errorcal" >/var/www/html/alfetta/comandi/comando.sh';
exec($s);
while (file_exists ($path."errorcal" )){
//   exec($s);
   usleep(200);
}
//echo $s."\n";
//exec("rm ".$path."errorcal");
if ($_GET) {
   $strumento_campione=$_GET{"strcmp"};
//   echo $strumento_campione;
   $n_giorni=$_GET["n_day"];
//   echo $n_giorni;
   $pm=$_GET["pm"];
//   echo $pm;
}
else {
   $strumento_campione=$argv[1];
   $n_giorni=$argv[2];
   $pm=$argv[3];
}
$s='echo "/home/pi/alfetta/calibration/autocalibration.sh '.$strumento_campione.' '.$n_giorni.' '.$pm.'" >/var/www/html/alfetta/comandi/comando.sh';
//echo $s;
exec($s);

while (! file_exists ($path."errorcal" )){usleep(200);}
exec('cat '.$path.'errorcal 2>&1',$er,$return);
if (strpos($er[0],"OK") !== false){
//   usleep(500); // consente la chiusra dei files di registrazione
   exec('cat '.$path.'distribution 2>&1',$d,$return);
   exec('cat '.$path.'regressione 2>&1',$r,$return);
   exec('cat '.$path.'coefficient 2>&1',$c,$return);
//var_dump($r);
   echo $er[0]."\n";
   echo $d[0]."\n";
   echo $r[0]."\n";
   echo $c[0]."\n";
}
else {
   echo $er[0]."\n";
   echo "{}"."\n";
   echo "{}"."\n";
   echo "{}"."\n";
}
?>
