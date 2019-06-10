
<?php
/*
wlan0     IEEE 802.11  ESSID:"YYYYYYYYY"
          Mode:Managed  Frequency:2.462 GHz  Access Point: xx:xx:xx:xx:xx
          Bit Rate=65 Mb/s   Tx-Power=31 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Power Management:on
          Link Quality=67/70  Signal level=-43 dBm 
          Rx invalid nwid:0  Rx invalid crypt:0  Rx invalid frag:0
          Tx excessive retries:9  Invalid misc:0   Missed beacon:0
*/

//$s="wavemon -d |grep 'essid:\|channel:\|bitrate:\|link quality:\|signal level'";
// Channel versus Freuency Tables
$chan=array("2.412"=>"1","2.417"=>"2","2.422"=>"3","2.427"=>"4","2.432"=>"5","2.437"=>"6","2.442"=>"7","2.447"=>"8","2.452"=>"9","2.457"=>"10","2.462"=>"11","2.467"=>"12","2.472"=>"13","2.484"=>"14");
// Retrieve Wifi monitor Data
$s="iwconfig wlan0 |grep 'ESSID\|Frequency\|Bit Rate\|Link Quality\|Signal level'";
exec($s,$return);
// Parse  Wifi Data return 
$return[0]=preg_replace("([ ]+)", " ", $return[0]); //trim($return[0]);
$return[1]=trim(preg_replace("([ ]+)", " ", $return[1])); //trim($return[1]);
$return[2]=trim(preg_replace("([ ]+)", " ", $return[2])); //trim($return[2]);
$return[3]=trim(preg_replace("([ ]+)", " ", $return[3])); //trim($return[3]);
// ------------------------------------------------
$ssid=explode(":",explode(" ",$return[0])[3])[1];
$frequency=explode(":",explode(" ",$return[1])[1])[1];
$bitrate=explode("=",explode(" ",$return[2])[1])[1];
$linkquality=explode("=",explode(" ",$return[3])[1])[1];
$linkperc=eval("return ".$linkquality.";");
$signallevel=explode("=",explode(" ",$return[3])[3])[1]; 
if ($signallevel > "-31") {$signallevel ="-31";}
$signalpower=number_format(pow(10,$signallevel/10)*1000000.0,10); # convert to nW
$unity="nW"; //base unit to calcolate wifi Power  from dBm
/*
if ($signalpower > 30){
//  Convert to uW is value to big
 	$unity="uW";
	$signalpower=$signalpower/1000.0;;
}
if ($signalpower < 0.05){
//  Convert to pW is value to  small
	$unity="pW";
	$signalpower=$signalpower*1000.0;;
}
*/
// Return Values to Web  client
echo $ssid."\n";
echo $chan[$frequency]."    (".$frequency." GHz)"."\n";
echo $bitrate."\n";
echo $linkperc."\n";
echo $signalpower."\n";
echo $signallevel."\n";
echo $unity."\n";
?>

