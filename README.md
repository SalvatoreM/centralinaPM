
> # Centralina per misura particolato PM10 e PM2.5

Applicativi Python e PHP per la realizzazione di una centralina di misura della qualità dell'aria.

Il progetto nasce da una iniziativa del comitato MammeNoInceneritore (Sesto Fiorentino-Firenze) per arginare e contrastare la costruzione di un nuovo inceneritore nella zona nord di Firenze già soggetta a sorgenti inquinati della atmosfera quali Autostrada, Aereporto,Discarica e diverse altre attività commerciali.  
Vista la latenza delle istituzioni a eseguire un monitoraggio oggettivo e trasparente della qualità dell'aria nella zona, il comitato MNI ha deciso di costruire delle stazioni di monitoraggio e di installarle in maniera diffusa nelle zona interessata e in quelle limitrofe. 
E' per questo che è stato lanciato il progetto "Che Aria Tira"  (http://www.cheariatira.it) che ha trovato sostenitori e finanziatori tra i cittadini di Firenze e comuni adiacenti e tra le associazioni tra cui Ninux ( http://firenze.ninux.org) , FabLabdi Firenze   (..)  e volontari. 

Il progetto è completamente aperto: 

I dati raccolti sono accessibili e scaricabili da web ( http://db.cheariatira.it e http://salvatorehost.no-ip.org/aria/pm_menu.php )  
 I dettagli di installazione e costruzione di una centralina sono lo scopo di questa publicazione.
In questo contesto vengono qui pubblicati i sorgenti che controllano la stazione di misura e le procedure per installarlo e costruirsi così la propria Stazione di Monitoraggio.
Ogni centralina costruita per essere ammessa al circuito ufficilale di CheAriaTira necessita di una procedura di calibrazione. Tale operazione può essere richiesta facendo riferimento ai contatti presenti sul portale  http://www.cheariatira.it 

### Elenco Materiali per realizzazione Hw

Qui di seguito la lista dei componenti necessari alla costruzione della Centralina:

| Descrizione | Sigla    | Quantità |
| --------|---------|-------|
|Scatola  | Gewiss GW44207   |1   |
| Separatore| Disegno .. | 1  |
| Viti testa cilindrica in Bronzo|  M2x15 | 4  |
| Dado  esagonale in bronzo | M2  | 8|
| Viti Testa cilindrica acciaio| M3x8 | 3  |
| Distanziali esagonali in plastica | M3x10| 3 |
| Scheda |Raspberry PI3 | 1|
|Sensore |SDS011 | 1|
|Adattatore Seriale |SDS011_USB2TTL_004|1|
|Scheda Memoria| Micro SD 16GB| 1|
|Alimentatore| 5V 2500 mA - Connettore micro USB| 1|
|Tubo gomma | 8x11 |300 mm|
|Termo restringente | diametro interno 6 mm | 10 mm|

### Montaggio meccanico dei componenti

Osserva il video :
https://www.youtube.com/watch?v=Vy7fzqIddpE


### Preparazione Scheda MicroSD
*  Scaricare il file .zip immagine Raspbian Raspbian Stretch Lite da https://downloads.raspberrypi.org/raspbian_lite_latest
*  Scompattare file .zip (unzip per  Linux) per ottenere .img di circa 4GB
*  Copiare il file.img su Sd card 
>  dd bs=4M if=2017-11-29-raspbian-stretch.img of=/dev/sdX conv=fsync


Inserire la scheda SD nella RaspBerry ed avviare.
Collegarsi alla shell via ssh  
> ssh pi@raspberry_ip_add

Nota: Ricordarsi di abilitare il server ssh creando un file ssh (anche vuoto) nella partizione boot

### Preparazione Ambiente Operativo 
 Il software della centralina ha dipendenze verso i seguenti pacchetti che devono essere installati
prima di installare il software python e php della Centralina

I pacchetti sono i seguenti:
*  Web server Apache e PHP

> sudo apt-get install apache2 -y

> sudo apt-get install php libapache2-mod-php -y

* Cattura eventi su file e cartelle
> sudo apt-get install incron

> echo root >> /etc/incron.allow

Generare trigger di cattura evento

> sudo incrontab -e

quindi aggiungere :

 /var/www/html/alfetta/comandi/ IN_CLOSE_WRITE /var/www/html/alfetta/comandi/proxycom.sh

salvare e chiudere l'editor

* Libreria per applicativi python

> sudo apt-get install python-serial

 * Wifi monitor (non neccessario dall versione 4.3.x.x.x)
 > sudo apt-get install wavemon
 
 * VPN client per connessione alla rete di monitoragggio e manutanzione remota (opzionale)
 
 > sudo apt-get install openvpn
 
 > sudo systemctl enable openvpn
 
 >  sudo  sed -i  's/#AUTOSTART=\"all\"/AUTOSTART=\"all\"/' /etc/default/openvpn
 
 * Procedura di attivazione del sistema di auto predispozione HostSpot in mancanza di connessione Wifi o connessione via cavo Ethernet (per una comprensione più dettagliata rifersirsi a http://www.raspberryconnect.com/network/item/330-raspberry-pi-auto-wifi-hotspot-switch-internet
 > sudo apt-get install hostapd
 
 > sudo systemctl disable hostapd
 
 > sudo sed -i  's/#DAEMON_CONF=\"\"/DAEMON_CONF=\"\/etc\/hostapd\/hostapd.conf\"/' /etc/default/hostapd
 
> $>sudo sed -i  's/^DAEMON_OPTS=\"\"/#DAEMON_OPTS=\"\"/' /etc/default/hostapd

> $>sudo apt-get install dnsmasq

> $>systemctl disable dnsmasq

> $>sudo echo -e  '# Ip statico di fallback\nprofile ipstatic-eth0\nstatic ip_address=192.168.100.50/24\ninterface eth0\nfallback ipstatic-eth0\nnohook wpa_supplicant\n'  >> /etc/dhcpcd.conf


### Installazione Files Applicativi
A questo punto l'infrastruttura operativa per il sistema Centralina è completo. 
Devono essere solo installati i file  operativi .py .php .html ecc..
Per questo scaricare il file .zip  da questo repository e spacchettarlo in una cartella oppure utilizzando gli strumenti di git.
La struttura del pacchetto prevede già la allocazione dei file nel filesyetm di raspbian.
Una procedura automatica di installazione è possibile  :

> cd path/dovehocopiatoifiles/

> sudo ./install.sh 

Se avete dimenticato qualche dipendenza questa verrà installata.

Se tutto è andato bene e senza errori  spegnete la RaspBerry , sconnetete il cavo ethernet e riavviatela. 
Vedrete comparire AP WiFi con SSID : CentralinaPM connettetevi con la password:"1234567890"  vi sarà assegnato un indirizzo sulla rete 192.168.100.xxx.
L'indirizzo della Centralina è 192.168.100.5
Attraverso il vostro browser (evitate come la peste  MS Explorer)  http://192.168.100.5/alfetta e comparitrà la maschera di configurazione dalla quale potrete configurare la connessione Wifi al vostro router ed inoltre potrete scoprire tutte le funzionalità della centralina.
### Buon Lavoro
Buon divertimento e Buon Aria ........

Per accidenti , imprecazioni e ...  complimenti a
 salvatoremoretti@tiscali.it
