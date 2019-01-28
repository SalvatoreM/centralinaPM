#!/bin/bash
apt-get update
apt-get upgrade
dpkg -l > installato
# formato linea:
# nome pacchetto:operazione:istr1
while read -r l;do
#        echo -e "linea completa "$l"\n"
	if   ! echo $l |grep '^#' >/dev/null  ; then
		pack=$(echo $l | cut -d ":" -f 1)
		opt=$(echo $l | cut -d ":" -f 2)
      istr=$(echo $l | cut -d ":" --fields 3-)
#                echo $pack2""$opt" "$istr
		if ! grep $pack installato &> /dev/null  ; then
			case $opt in
				apt) 
					echo "-----------------------------------"
					echo "Installo  pachetto  "$pack
					echo "-----------------------------------"
					apt-get install $pack -y
					;;
				exe)
					echo "-----------------------------------"
					echo "Configuro  pachetto  "$pack
					echo "-----------------------------------"
					eval $istr
                                        ;;
			esac
 		else
			echo
			echo "-----------------------------------"
			echo "Pachetto "$pack" gia installato"
			echo "-----------------------------------"
			echo
		fi
	fi
done < installa 
