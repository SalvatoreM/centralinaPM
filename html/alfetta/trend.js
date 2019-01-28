label_on="None";
mn1=newtime(0);
n=0;
newtred=false;
var lab=[];
var vect=[];
var vect_med=[];
var vect_min=[];
var vect_max=[];
var wifi_lab=[];
var wifi_vect_sig=[];
var wifi_vect_qual=[];
var wifi_vect_min=[];
var wifi_vect_max=[];
for (i=0;i<32;i++) {
   vect[i]=0;
   vect_med[i]=0;
   vect_min[i]=0;
   vect_max[i]=0;
	lab[i]= i //newDate(-i);
}
//--------------------------------------------------------------------------------
for (i=0;i<20;i++) {
   wifi_vect_sig[i]=0;
   wifi_vect_qual[i]=0;
   wifi_lab[i]=i;
}
var wifi_sig = {
   label:"signal (nW)",
   data: [wifi_vect_sig],
        borderColor: "rgba(255,0,0,0.5)",
//        backgroundColor: "rgba(255,0,0,1)"
  };
var wifi_qual = {
   label:"quality (%)",
   data: [wifi_vect_qual],
        borderColor: "rgba(0,255,0,0.5)",
//        backgroundColor: "rgba(255,0,0,1)"
  };

  var config_wifi = {
    type: 'line',
    data: {
     labels:wifi_lab,
     datasets: [wifi_sig,wifi_qual],
    },
    options: {
//      animation:false,
      scales: {
        xAxes: [{
          type: 'category',      // "time",
/*          time: {
            unit: 'minute',
            round: 'minute',
            displayFormats: {
                  minute: 'HH:mm'
            }
          }*/
        }],
        yAxes: [{
          ticks:{
            beginAtZero: true
          }
        }]
      }
    }
  }

function graph_wifi_on(){
   nome="wifitrend";
   var ctx = document.getElementById(nome).getContext("2d");
   window.wifi = new Chart(ctx, config_wifi);
}
//------------------------------------------------------------------------;
function newDate(minutes) {
        m=moment().add(minutes, 'm');
//	console.log(m.format("HH:mm"));
        return m;
}
function newtime(minute) {
        m=moment().add(minute, 'm');
//	console.log(m.format("m"));
        return parseInt(m.format("m"));
}
  var value = {
	label:label_on,
	data: [vect],
        borderColor: "rgba(255,0,0,0.5)",
//        backgroundColor: "rgba(255,0,0,1)"
  };
  var value_med = {
	label:label_on+" Avg",
	data: [vect_med],
        borderColor: "rgba(0,255,0,0.5)",
//        backgroundColor: "rgba(255,0,0,1)"
  };
  var value_min = {
	label:label_on+" Min",
	data: [vect_min],
        borderColor: "rgba(255,255,0,0.5)",
//        backgroundColor: "rgba(255,0,0,1)"
  };
  var value_max = {
	label:label_on+" Max",
	data: [vect_max],
        borderColor: "rgba(0,0,255,0.5)",
//        backgroundColor: "rgba(255,0,0,1)"
  };

  var config = {
    type: 'line',
    data: {
     labels: lab,
     datasets: [value,value_med,value_max,value_min],
    },
    options: {
//      animation:false,
      scales: {
        xAxes: [{
          type: 'category',      // "time",
/*          time: {
            unit: 'minute',
            round: 'minute',
            displayFormats: {
              		minute: 'HH:mm'
            }
          }*/
        }],
        yAxes: [{
          ticks:{
            beginAtZero: true
          }
        }]
      }
    }
  }
function graph_on(){
	nome="trend";
	var ctx = document.getElementById(nome).getContext("2d");
	window.myLine = new Chart(ctx, config);
}

function update_value(val,valmed,valmax,valmin,x){
	l=vect.length-1;
/*	vect_min[l] = parseFloat(val),
	vect_med[l] = parseFloat(valmed);
   vect_max[l] = parseFloat(valmax),
   vect_min[l]=  parseFloat(val);*/
   vect.shift();
   vect.push(val);
   vect_min.push(valmin);
	vect_min.shift();
   vect_max.push(valmax);
	vect_max.shift();
   vect_med.push(valmed);
	vect_med.shift();
   lab.shift();
   lab.push(x);
   n=0;
	myLine.data.datasets[0].data = vect;
	myLine.data.datasets[1].data = vect_med;
	myLine.data.datasets[2].data = vect_min;
	myLine.data.datasets[3].data = vect_max;
	myLine.data.labels=lab;
	myLine.update();
//	console.log(vect_min[l],vect[l],vect_max[l]);
}

function new_trend(label){
/*	for (i=vect.length;i >0;i--){
		vect[i-1]=0;
		vect_min[i-1]=0;
		vect_max[i-1]=0;
	}
	n=0;*/
	label_on=label;
	newtrend=true;
	myLine.data.datasets[0].data = vect ;
	myLine.data.datasets[1].data = vect_med ;
	myLine.data.datasets[2].data = vect_min ;
	myLine.data.datasets[3].data = vect_max ;
	myLine.data.datasets[0].label=label;
	myLine.data.datasets[1].label=label+" Avg";
	myLine.data.datasets[2].label=label+" Min";
	myLine.data.datasets[3].label=label+" Max";
	myLine.data.labels=lab;
	myLine.update();
}

function wifi_trend(){
 for (i=wifi_vect_sig.length;i >0;i--){
      wifi_vect_sig[i-1]=0;
      wifi_vect_qual[i-1]=0;
   }
   n=0;
   wifi.data.datasets[0].data = wifi_vect_sig ;
   wifi.data.datasets[1].data = wifi_vect_qual ;
/*   wifi.data.datasets[0].label=;
   wifi.data.datasets[2].label=label+" Min";
   wifi.data.datasets[3].label=label+" Max";
   wifi.data.labels=wifi_lab;*/
   wifi.update();
}

function update_wifi(quality,signal,unity){
   l=wifi_vect_sig.length-1;
   wifi_vect_sig.shift();
   wifi_vect_sig.push(signal);
   wifi_vect_qual.push(quality);
   wifi_vect_qual.shift();
   wifi.data.datasets[0].label ="signal ("+unity+")" ;
   wifi.data.datasets[0].data = wifi_vect_sig;
   wifi.data.datasets[1].data = wifi_vect_qual;
   wifi.update();
}

