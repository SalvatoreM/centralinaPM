<?php
// Handling data in JSON format on the server-side using PHP
//
header("Content-Type: application/json");
// build a PHP variable from JSON sent using POST method
$v = stripslashes(file_get_contents("php://input"));
// build a PHP variable from JSON sent using GET method
//$v = $_GET["data"];
// encode the PHP variable to JSON and send it back on client-side
//var_dump($v);
//echo ($v);
$v=str_replace("},","},\n",$v)."\n";
$fp = fopen('caltable.json', 'w');
fwrite($fp,$v);
fclose($fp);
$j=JSON_decode($v,True);
$lung = count($j["calibration"]);
//var_dump($j["calibration"][$lung-1]);
//echo $j["calibration"][$lung-1]["measure"]."\n";
//echo $j["calibration"][$lung-1]["m"]."\n";
//echo $j["calibration"][$lung-1]["q"]."\n";
$pm=$j["calibration"][$lung-1]["measure"];
$m=$j["calibration"][$lung-1]["m"];
$q= $j["calibration"][$lung-1]["q"];
$s= "echo '/home/pi/alfetta/comandi/updateconf.sh ".$pm." ".$m." ".$q."'>  /var/www/html/alfetta/comandi/comando.sh";
//echo $s."\n";
exec($s);
?>
