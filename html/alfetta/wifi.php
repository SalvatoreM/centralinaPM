
<?php
$s="wavemon -d |grep 'essid:\|channel:\|bitrate:\|link quality:\|signal level'";
exec($s,$return);
$return[0]=trim($return[0]);
$return[1]=trim($return[1]);
$return[2]=trim($return[2]);
$return[3]=trim($return[3]);
$return[4]=trim($return[4]);
echo explode(" ",$return[0])[1]."\n";
echo explode(" ",$return[1])[1]."\n";
echo explode(" ",$return[2])[1]."\n";
$e=explode(" ",$return[3])[2];
//var_dump($return);
//echo explode(" ",$return[4])[5];
//echo $e;
//echo eval("return intval(".$e."*100.0);")."\n";
echo eval("return ".$e.";")."\n";
if (explode(" ",$return[4])[5]=="pW)"){
        echo str_replace("(","",(floatval(str_replace("(","",explode(" ",$return[4])[4]))/1000))."\n";
}
elseif (explode(" ",$return[4])[5]=="uW)"){
        echo str_replace("(","",(floatval(str_replace("(","",explode(" ",$return[4])[4]))*1000))."\n";
}
else {
        echo str_replace("(","",explode(" ",$return[4])[4])."\n";
}
echo explode(" ",$return[4])[2].explode(" ",$return[4])[3]."\n";
?>

