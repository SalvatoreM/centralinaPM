<?php


function recover(){
    global $lista;
    $lista["host"]=array();
//    echo "Recover"."<br>";
    $af = fopen("/var/www/html/alfetta/correction.conf", "r") or die("Unable to open file!");
    while(!feof($af)) {
        $l=fgets($af);
        if (explode("=",$l)[0]=="host"){
        	array_push($lista[explode("=",$l)[0]],str_replace("\n","",explode("=",$l)[1]));
	}
	elseif (strlen($l) >5) { $lista[explode("=",$l)[0]]=str_replace("\n","",explode("=",$l)[1]); }
    }
    fclose($af);
}

//-----------------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------------
$lista=array();
recover();
echo $lista["nome"].",".$lista["kk1"]." <I>x</I><SUP>2</SUP> + ".$lista["k1"]." <I>x</I> + ".$lista["q1"].",".$lista["kk2"]." <I>x</I><SUP>2</SUP> + ".$lista["k2"]." <I>x</I> + ".$lista["q2"];
?>
