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
//   echo $strumento_campione;
   $exclude=$_GET["exclude"];

//   echo $n_giorni;
   $pm=$_GET["pm"];
//   echo $pm;
    $zi_mode=$_GET["zi"];
}
else {
   $exclude=$argv[2];
   $pm=$argv[1];
   $zi_mode=$argv[3];
}
if (($pm!="PM10") and ($pm!="PM2.5")){ exit("Errors Parametres 1\n");}
if (strlen($zi) > 0){
	if (!preg_match('/^[0-1]{1}/',$zi)){ exit("Errors Parametres 2\n");}
}
if (!preg_match('/^\[([0-9]{1,2},)?+([0-9]{1,2})?\]/',$exclude)){ exit("Errors Parametres 3\n");}
$s='echo "/home/pi/alfetta/calibration/autorecalibration.sh '.$pm.' '.$exclude.' ' .$zi_mode.'" >/var/www/html/alfetta/comandi/comando.sh';
//echo $s;
exec($s);

while (! file_exists ($path."errorcal" )){usleep(200);}
exec('cat '.$path.'errorcal 2>&1',$er,$return);
echo $er[0];
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
