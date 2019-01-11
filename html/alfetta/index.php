<html>
<!DOCTYPE HTML PUBLIC '-//W3C//DTD HTML 4.01//EN'>
<head>
<title>Configuration Manager</title>
</head>
<body bgcolor='#E6E6E6'>
<h2><center>Configuration Manager</h2>
<pre><p>
<table border="3" bgcolor='#f0f0f0' cellpadding = "5" align = "center" width = "800">
<tr>
<td>
<?php

function save(){
    $af = fopen("/home/pi/alfetta/etc/alfetta.conf", "w"); // or die("Unable to open file!");
    fwrite($af, "nome=".$_POST["nome"]."\n");
    fwrite($af, "lat=".$_POST["lat"]."\n");
    fwrite($af, "lon=".$_POST["lon"]."\n");
    fwrite($af, "kk1=".$_POST["kk1"]."\n");
    fwrite($af, "k1=".$_POST["k1"]."\n");
    fwrite($af, "q1=".$_POST["q1"]."\n");
    fwrite($af, "kk2=".$_POST["kk2"]."\n");
    fwrite($af, "k2=".$_POST["k2"]."\n");
    fwrite($af, "q2=".$_POST["q2"]."\n");
    fwrite($af, "sensore=".$_POST["sensore"]."\n");
    fwrite($af, "user=".$_POST["user"]."\n");
    fwrite($af, "pswdb=".$_POST["pswdb"]."\n");
    fwrite($af, "id=".$_POST["id"]."\n");
    foreach ($_POST["host"] as $h){
    	if ($h !="None"){fwrite($af, "host=".$h."\n");}
    }
    fclose($af);
}

function anagrafica(){
    $af = fopen("/home/pi/alfetta/etc/anagrafica.conf", "w"); // or die("Unable to open file!");
    fwrite($af, "nick=".$_POST["nick"]."\n");
    fwrite($af, "indirizzo=".$_POST["indirizzo"]."\n");
    fwrite($af, "city=".$_POST["city"]."\n");
    fwrite($af, "provincia=".$_POST["provincia"]."\n");
    fwrite($af, "cap=".$_POST["cap"]."\n");
    fwrite($af, "telefono=".$_POST["telefono"]."\n");
    fwrite($af, "responsabile=".$_POST["responsabile"]."\n");
    fwrite($af, "email=".$_POST["email"]."\n");
    fclose($af);
}

function report(){
    echo "salva rapporto"."<br>";
    $af = fopen("/home/pi/alfetta/etc/mail_account", "w"); // or die("Unable to open file!");
    fwrite($af, "emailsend#".$_POST["emailsend"]."\n");
    fwrite($af, "smtp#".$_POST["smtp"]."\n");
    fwrite($af, "account#".$_POST["account"]."\n");
    fwrite($af, "passwd#".base64_encode($_POST["passwd"])."\n");
    fwrite($af, "port#".$_POST["port"]."\n");
    fwrite($af, "sentfrom#".$_POST["sentfrom"]."\n");
    fwrite($af, "sendto#".$_POST["sendto"]."\n");
    fclose($af);
}

function connetti(){
    global $lista;
    echo "Mi connetto <br>";
    echo " a ".$lista["ssid"]."<br>";
    echo "con ".$lista["psw"]."<br>";
//	exec('sudo /home/pi/alfetta/connetti.sh '.$lista["ssid"].' '.$lista["psw"],$return);
    $s='echo "/home/pi/alfetta/comandi/connetti.sh '.$lista["ssid"].' '.$lista["psw"].'" >/var/www/html/alfetta/comandi/comando.sh';
    echo $s."<br>";
    exec('echo "/home/pi/alfetta/comandi/connetti.sh '.$lista["ssid"].' '.$lista["psw"].'" >/var/www/html/alfetta/comandi/comando.sh',$return);
    var_dump($return);
}

function recover(){
    global $lista;
    $lista["host"]=array();
//    echo "Recover"."<br>";
    $af = fopen("/home/pi/alfetta/etc/alfetta.conf", "r") or die("Unable to open file!");
    while(!feof($af)) {
        $l=fgets($af);
//        var_dump(explode("=",$l)[0]);
//	echo $l."<br>";
        if (explode("=",$l)[0]=="host"){
//		echo "array push  <br>";
//        	echo str_replace("\n","",explode("=",$l)[1])."<br>";
        	array_push($lista[explode("=",$l)[0]],str_replace("\n","",explode("=",$l)[1]));
//		var_dump($lista["host"]);
	}
	else { $lista[explode("=",$l)[0]]=str_replace("\n","",explode("=",$l)[1]); }
    }
    fclose($af);
//    var_dump($lista);
}

function recover_anagrafica(){
    global $lista;
    $af = fopen("/home/pi/alfetta/etc/anagrafica.conf", "r") or die("Unable to open file!");
    while(!feof($af)) {
        $l=fgets($af);
        $lista[explode("=",$l)[0]]=str_replace("\n","",explode("=",$l)[1]);
    }
    fclose($af);
//    var_dump($lista);
}

function recover_report(){
    global $lista;
    $af = fopen("/home/pi/alfetta/etc/mail_account", "r") or die("Unable to open file!");
    while(!feof($af)) {
        $l=fgets($af);
        if (explode("#",$l)[0]=="passwd"){
//		echo "array push  <br>";
//        	echo str_replace("\n","",explode("=",$l)[1])."<br>";
        	$lista[explode("#",$l)[0]]=str_replace("\n","",base64_decode(explode("#",$l)[1]));
	}
	else { $lista[explode("#",$l)[0]]=str_replace("\n","",explode("#",$l)[1]); }
    }
    fclose($af);
//    var_dump($lista);
}


function scan_option ($connesso){
	global $lista;
//		exec('sudo wpa_cli list_networks',$return);
        exec ('sudo iwlist wlan0 scan |grep ESSID',$return);
//	var_dump($lista);
	foreach($return as $network) {
	    $arrNetwork =explode(":",$network);
	    $arrNetwork=str_replace('"',"",$arrNetwork);
        $ssid = $arrNetwork[1];
//	    echo $lista["ssid"]."<br>";
            if (isset($ssid)) { 
				if ($ssid== $connesso) {echo '<option value="'.$ssid.'" selected>'.$ssid ."</option>\n";}
//				else  {echo '<option value="'.$ssid.' selected">'.$ssid ."</option>\n";}
				else  {echo '<option value="'.$ssid.'">'.$ssid ."</option>\n";}
	    }
        }
}

function option ($opt,$actual){
    global $lista;
	foreach($opt as $o) {
 	    if ($o == $lista[$actual]) {echo '<option value="'.$o.'" selected>'.$o ."</option>\n";}
	    else  {echo '<option  value="'.$o.'">'.$o ."</option>\n";}
    }
}

function connected(){
	exec('sudo wpa_cli list_networks',$return);
/*	for($shift = 0; $shift < 4; $shift++ ) {
		array_shift($return);
	}*/
	foreach($return as $network) {
		$arrNetwork = preg_split("/[\s\t]+/",$network);
		if (is_numeric($arrNetwork[0])){
	                $ssid = $arrNetwork[1];
                	if($arrNetwork[3]=="[CURRENT]"){
				echo "<big><big>Connesso alla rete ".$ssid."</big></big><br><br>\n"; 
				$ret=$ssid;}
        	}
        }
    	return($ret);
}
//-----------------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------------
$lista=array();
$lista["ssid"]= explode(" ",$_POST["ssid"])[0];
$lista["psw"]= $_POST["psw"];
$lista["nome"] = $_POST["nome"];
$lista["lat"]=$_POST["lat"];
$lista["lon"]=$_POST["lon"];
$lista["kk1"]=$_POST["kk1"];
$lista["k1"]=$_POST["k1"];
$lista["q1"]=$_POST["q1"];
$lista["kk2"]=$_POST["kk2"];
$lista["k2"]=$_POST["k2"];
$lista["q2"]=$_POST["q2"];
$lista["sensore"]=$_POST["sensore"];
$lista["user"]=$_POST["user"];
$lista["pswdb"]=$_POST["pswdb"];
$lista["id"]=$_POST["id"];
$lista["host"]=$_POST["host"];
$lista["nick"]=$_POST["nick"];
$lista["indirizzo"]=$_POST["indirizzo"];
$lista["responsabile"]=$_POST["responsabile"];
$lista["city"]=$_POST["city"];
$lista["provincia"]=$_POST["provincia"];
$lista["cap"]=$_POST["cap"];
$lista["telefono"]=$_POST["telefono"];
$lista["email"]=$_POST["email"];
$lista["emailsend"]=$_POST["emailsend"];
$lista["smtp"]=$_POST["smtp"];
$lista["passwd"]=$_POST["passwd"];
$lista["port"]=$_POST["port"];
$lista["sendto"]=$_POST["sendto"];
$lista["sentfrom"]=$_POST["sentfrom"];
//$city_option=array("Firenze","Sesto Fiorentino","Prato","Campi Bisenzio");
$city_option=array("Firenze","Scandicci","Sesto Fiorentino",
"Empoli","Campi_Bisenzio",
"Bagno_a_Ripoli","Fucecchio",
"Figline_e_Incisa_Valdarno",
"Pontassieve","Lastra_a_Signa","Signa,Borgo_San_Lorenzo","Castelfiorentino",
"Calenzano","San_Casciano_in_Val_di_Pesa","Reggello","Certaldo","Impruneta",
"Vinci","Montelupo_Fiorentino","Fiesole","Greve_in_Chianti",
"Montespertoli","Scarperia_e_San_Piero","Cerreto_Guidi","Barberino_di_Mugello",
"Rignano_sull'Arno",
"Vicchio","Tavarnelle_Val_di_Pesa","Capraia_e_Limite","Pelago","Rufina","Dicomano",
"Vaglia","Gambassi_Terme","Firenzuola","Barberino_Val_d'Elsa",
"Montaione","Marradi","Londa","San_Godenzo","Palazzuolo_sul_Senio");
$provincia_option=array("Firenze","Grosseto","Livorno","Lucca","MassaCarrara","Pisa","Pistoia","Siena","Prato");
/*----------------------------------------------------------------------------*/
/*----------------------------------------------------------------------------*/
/*-------------------------Opzioni di esecuzione------------------------------*/
if ($_POST["esegui"]=="rapporto"){
    report();
    recover();
    recover_anagrafica();
}
if ($_POST["esegui"]=="Connetti"){
    recover();
    recover_anagrafica();
    recover_report();
    connetti();
}
if ($_POST["esegui"]=="anagrafica"){
    anagrafica();
    recover();
    recover_report();
}
//if (isset($_POST["nome"])){
if ($_POST["esegui"]=="salva"){    
    save();
    recover_anagrafica();
    recover_report();
}
else {
    recover();
    recover_anagrafica();
    recover_report();
}
//var_dump($lista);
//var_dump($lista["host"]);
$conn=connected();
echo "<center>";
/*---------------------------Wifi-------------------------------------------------*/
echo "<form action='index.php'"." method='post'>".'<table border="1" style="center">';
echo  '<tr><th>SSID</th><th><select name="ssid">';
scan_option($conn);
echo "</select></th></tr>";
echo '<tr><th>Password:</th><th><input type="text" name="psw" value="'.$lista["psw"].'"/></th></tr></table>';
echo '<input type="hidden" name="esegui" value="Connetti" />';
echo '<input type="submit" value="Connetti" />';
echo "</form>";
/*----------------------------------------------------------------------------*/
/*-------------------------------Dati Necessari---------------------------------------------*/
echo "<br><br><b><big>Dati Necessari</big></b><br><br>";
/*----------------------------------------------------------------------------*/
echo "<form action='index.php'"." method='post'>".'<table border="1" style="center">';
/*--------------------------------------DataBase--------------------------------------*/
echo '<tr><th>Host DataBase(url/ip)</th>';
$checked="";
if  (in_array("salvatorehost.no-ip.org,InfluxDB",$lista["host"])){
    $checked="checked";
    echo '<th align="left"><input type="radio" name="host[]" value="salvatorehost.no-ip.org,InfluxDB" '.$checked.'/>Server Ninux (Consigliato)<br>';
    $checked="";
    echo '<input type="radio" name="host[]" value="94.177.187.133/ninuxback,InfluxDB" '.$checked.'/>Server Ninux Mirror<br>';
    $checked="";
    echo '<input type="radio" name="host[]" value="None" '.$checked.'/>Nessun Server Ninux<br>';
}
elseif (in_array("94.177.187.133/ninuxback,InfluxDB",$lista["host"])){
    $checked="";
    echo '<th align="left"><input type="radio" name="host[]" value="salvatorehost.no-ip.org,InfluxDB" '.$checked.'/>Server Ninux (Consigliato)<br>';
    $checked="checked";
    echo '<input type="radio" name="host[]" value="94.177.187.133/ninuxback,InfluxDB" '.$checked.'/>Server Ninux Mirror<br>';
    $checked="";
    echo '<input type="radio" name="host[]" value="None" '.$checked.'/>Nessun Server Ninux<br>';
}
else{
    $checked="";
    echo '<th align="left"><input type="radio" name="host[]" value="salvatorehost.no-ip.org,InfluxDB" '.$checked.'/>Server Ninux (Consigliato)<br>';
    echo '<input type="radio" name="host[]" value="94.177.817.133/ninuxback,InfluxDB" '.$checked.'/>Server Ninux Mirror<br>';
    $checked="checked";
    echo '<input type="radio" name="host[]" value="None" '.$checked.'/>Nessun Server Ninux<br>';
}
$checked="";
if  (in_array("db.cheariatira.it,CrateDB",$lista["host"])){$checked="checked";}
echo '<input type="checkbox" name="host[]" value="db.cheariatira.it,CrateDB" '.$checked.'/>Server MnI<br></th></tr>';
/*----------------------------------------------Dati ------------------------------*/
echo '<tr><th>Nome(Zona::IDName)</th><th><input type="text" pattern="[a-zA-Z0-9]+::[a-zA-Z0-9\-_:]+" name="nome" value="'.$lista["nome"].'"/></th></tr>';
echo "</th></tr>";
echo '<tr><th>User</th><th><input type="text" pattern="[a-zA-Z0-9]+" name="user" value="'.$lista["user"].'"/></th></tr>';
echo '<tr><th>Password</th><th><input type="password" pattern="[a-zA-Z0-9]+" name="pswdb" value="'.$lista["pswdb"].'"/></th></tr>';
echo '<tr><th>Codice ID (una o due cifre)</th><th><input type="text" pattern="[0-9]{1,2,3,4}" name="id" value="'.$lista["id"].'"/></th></tr>';
echo '<tr><th>Latitudine(+/-dd.ddd)</th><th><input type="text" pattern="[+-][0-9]+.[0-9]+" name="lat" value="'.$lista["lat"].'"/></th></tr>';
echo '<tr><th>Longitudine(+/-dd.ddd)</th><th><input type="text" pattern="[+-][0-9]+.[0-9]+" name="lon" value="'.$lista["lon"].'"/></th></tr>';

echo '<tr><th>Correzione PM10</th><th><input type="text" style="text-align: center;" pattern="[+-]?[0-9]+.[0-9]+" size="4" name="kk1" value="'.$lista["kk1"].'" />* X<SUP>2</SUP> +';
echo '<input type="text" style="text-align: center;" pattern="[+-]?[0-9]+.[0-9]+" size="4" name="k1" value="'.$lista["k1"].'" />* X +';
echo '<input type="text" style="text-align: center;" pattern="[+-]?[0-9]+.[0-9]+" size="4" name="q1" value="'.$lista["q1"].'" /></th></tr>';

echo '<tr><th>Correzione PM2.5</th><th><input type="text" style="text-align: center;" pattern="[+-]?[0-9]+.[0-9]+" size="4" name="kk2" value="'.$lista["kk2"].'" />* X<SUP>2</SUP> +';
echo '<input type="text" style="text-align: center;" pattern="[+-]?[0-9]+.[0-9]+" size="4" name="k2" value="'.$lista["k2"].'" />* X +';
echo '<input type="text" style="text-align: center;" pattern="[+-]?[0-9]+.[0-9]+" size="4" name="q2" value="'.$lista["q2"].'" /></th></tr>';
/*---------------------------------------------------Sensore-------------------------*/
echo '<tr><th>Sensore</th>';
$checked="";
if  ($lista["sensore"]=="SDS011"){$checked="checked";}
echo '<th align="left"><input type="radio" name="sensore" value="SDS011" '.$checked.'>SDS011<br>';
$checked="";
if  ($lista["sensore"]=="QBIT,10"){$checked="checked";}
echo '<input type="radio" name="sensore" value="QBIT,10" '.$checked.' disabled >QBIT_PM10<br>';
$checked="";
if ($lista["sensore"]=="QBIT,25"){$checked="checked";}
echo '<input type="radio" name="sensore" value="QBIT,25" '.$checked.' disabled >QBIT_PM25<br>';
/*if  ($lista["sensore"]=="Qbit"){$checked="checked";}
echo '<input type="radio" name="sensore" value="QBIT" '.$checked.' disabled>Qbit<br></th></tr>';*/
echo "</table><br>";
/*------------------------------Save----------------------------------------------*/
echo '<input type="hidden" name="esegui" value="salva" />';
echo '<input type="submit" value="Salva" />';
echo "</form>";
echo '<table border="1" style="center">';
echo "</table>";
/*----------------------------------Dati Opzionali------------------------------------------*/
echo "<br><br><b><big> Dati Facoltativi </big></b><br><br>";
echo "<form action='index.php'"." method='post'>".'<table border="1" style="center">';
echo '<tr><th>NicKName</th><th><input type="text" pattern="[a-zA-Z0-9]+" name="nick" value="'.$lista["nick"].'"/></th></tr>';
echo '<tr><th>Indirizzo</th><th><input type="text" pattern="[a-zA-Z0-9 ]+" name="indirizzo" value="'.$lista["indirizzo"].'"/></th></tr>';
/*------------------------------Città----------------------------------------------*/
echo  '<tr><th>Città</th><th><select name="city"  style="width: 240px;">';
option($city_option,"city");
echo "</select></th></tr>";
/*---------------------------------Provincia-------------------------------------------*/
echo  '<tr><th>Provincia</th><th><select name="provincia" style="width: 240px;" >';
option($provincia_option,"provincia");
echo "</select></th></tr>";
echo '<tr><th>CAP</th><th><input type="text" pattern="[5][0-9]+" name="cap" value="'.$lista["cap"].'"/></th></tr>';
echo '<tr><th>Responsabile</th><th><input type="text" pattern="[a-zA-Z0-9àèìòù ]+" name="responsabile" value="'.$lista["responsabile"].'"/></th></tr>';
echo '<tr><th>Telefono</th><th><input type="text" pattern="[03][0-9]+" name="telefono" value="'.$lista["telefono"].'"/></th></tr>';
echo '<tr><th>email</th><th><input  name="email" required="" type="email" value="'.$lista["email"].'"/></th></tr>';
echo "</table><br>";
echo '<input type="hidden" name="esegui" value="anagrafica" />';
echo '<input type="submit" value="Salva Anagrafica" />';
echo "</form>";
/*----------------------------------Dati email------------------------------------------*/
echo "<br><br><b><big> Rapporto Giornaliero </big></b><br><br>";
echo "<form action='index.php'"." method='post'>".'<table border="1" style="center">';
echo '<tr><th>Invia Rapporto</th>';
$checked="";
if  ($lista["emailsend"]=="yes"){$checked="checked";}
echo '<th align="center"><input type="radio" name="emailsend" value="yes" '.$checked.'>Si';
$checked="";
if  ($lista["emailsend"]=="no"){$checked="checked";}
echo '<input type="radio" name="emailsend" value="no" '.$checked.'>No<br></th></tr>';
echo '<tr><th>SMTP Server</th><th><input type="text" pattern="[a-zA-Z]+.[a-zA-Z]+.[a-zA-Z]+" name="smtp" value="'.$lista["smtp"].'"/></th></tr>';
/*----------------------------------------------------------------------------*/
echo '<tr><th>Account</th><th><input  name="account" required="" type="email" value="'.$lista["account"].'"/></th></tr>';
echo '<tr><th>Password</th><th><input  name="passwd"  type="password" value="'.$lista["passwd"].'"/></th></tr>';
echo '<tr><th>Port (default 0)</th><th><input  name="port"  pattern="[0-9]+" value="'.$lista["port"].'"/></th></tr>';
echo '<tr><th>Inviare a</th><th><input  name="sendto" required="" type="email" value="'.$lista["sendto"].'"/></th></tr>';
echo '<tr><th>Inviata da</th><th><input  name="sentfrom" required="" type="email" value="'.$lista["sentfrom"].'"/></th></tr>';
echo "</table><br>";
/*--------------------------Save and Refresh--------------------------------------------------*/
echo '<input type="hidden" name="esegui" value="rapporto" />';
echo '<input type="submit" value="Salva" />';
echo "</form>";
echo "<form action='index.php'><br>";
echo '<input type="submit" value="Refresh" />';
echo "</form>";
echo "<form action='show.html'><br>";
echo '<input type="submit" value="Control Panel" />';
echo "</form>";
echo "</table><br>";
?>
</td>
</tr>
</table>
<center> <font color = "#b0b0b0">
</html>
