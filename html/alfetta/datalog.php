<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN">
<HTML>
<HEAD>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" /><TITLE>Centralina - Diagnostica</TITLE></meta>
</HEAD>
<BODY>
<?php
exec("cat datalog.log",$result);
//var_dump($result);
$r=array_reverse($result);
foreach ($r as $l){
   echo $l."<br>";
}

?>
</BODY>
</HTML>

