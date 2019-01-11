var ctx = document.getElementById('scatter');
var cty = document.getElementById('trend');
var ctz = document.getElementById('spettro');
//regressione=eval("[{x:11.47,y:5.75},{x:103.80,y:125.79}]");
//regressione=eval("[{x:6.62,y:2.69},{x:70.50,y:92.13}]");
//dispersione=eval("[{x: 7.12,y:30.30},{x: 6.62,y:18.35},{x: 6.93,y:11.62},{x: 7.73,y: 8.72},{x: 9.24,y: 6.99},{x:12.77,y: 5.54},{x:14.10,y: 4.84},{x:15.23,y: 5.05},{x:15.24,y: 5.25},{x:15.77,y: 7.84},{x:13.60,y: 8.49},{x:13.19,y: 8.21},{x:12.22,y: 8.13},{x:10.51,y: 7.20},{x:10.65,y: 6.43},{x: 9.64,y: 6.01},{x: 8.53,y: 5.65},{x:12.10,y: 5.34},{x:38.54,y: 5.65},{x:12.47,y: 5.96},{x:12.37,y:15.82},{x:11.43,y:36.34},{x:10.42,y:142.26},{x:12.06,y:138.89},{x:12.03,y:73.27},{x:11.25,y:43.92},{x:11.32,y:29.88},{x: 9.95,y:20.68},{x: 9.00,y:15.44},{x:10.40,y:11.22},{x:13.20,y: 8.07},{x:14.12,y: 6.53},{x:16.09,y: 6.08},{x:18.23,y: 9.65},{x:20.48,y:11.27},{x:20.49,y:12.61},{x:24.55,y:15.32},{x:30.84,y:17.52},{x:32.17,y:18.51},{x:33.01,y:17.38},{x:35.24,y:16.41},{x:45.46,y:17.02},{x:43.21,y:18.98},{x:50.09,y:36.40},{x:51.31,y:56.19},{x:53.58,y:68.33},{x:53.93,y:129.50},{x:54.99,y:135.60},{x:47.37,y:75.58},{x:46.10,y:42.99},{x:47.85,y:31.96},{x:46.97,y:27.57},{x:37.77,y:26.57},{x:34.01,y:24.83},{x:37.23,y:22.21},{x:35.54,y:19.65},{x:29.63,y:18.14},{x:24.30,y:16.40},{x:29.23,y:15.24},{x:24.18,y:14.39},{x:17.40,y:12.72},{x:16.55,y:11.70},{x:16.12,y:10.53},{x:15.45,y: 9.20},{x:14.91,y:10.68},{x:14.30,y:13.59},{x:20.00,y:15.32},{x:25.23,y:17.07},{x:27.53,y:16.73},{x:18.69,y:15.53},{x:17.89,y:13.87},{x:22.28,y:13.61},{x:21.21,y:12.64},{x:17.68,y:10.67},{x:18.41,y:10.33},{x:15.08,y: 9.41},{x:15.65,y: 9.37},{x:16.35,y: 9.23},{x:15.72,y: 8.44},{x:15.50,y: 7.79},{x:16.27,y: 8.57},{x:20.74,y: 8.96},{x:23.30,y:11.61},{x:26.18,y:14.30},{x:30.78,y:31.29},{x:31.66,y:33.44},{x:30.59,y:25.90},{x:35.32,y:22.41},{x:35.44,y:19.99},{x:41.90,y:21.68},{x:53.01,y:39.78},{x:54.99,y:59.74},{x:57.45,y:101.14},{x:52.55,y:127.82},{x:58.28,y:174.76},{x:70.50,y:173.16}]");
regressione=[];
dispersione=[];
var  spettro=[];
spettro.length=21;
spettro.fill(0);
var testo="";
var asse_tempo=[];
var trend1=[];
var trend2=[];
var staz1="";
var staz2="";
var exclude=[];
//var titolo='{ display:true, text: "PM10 Distribution" } ';
var scatterChart = new Chart(ctx, {
    type: 'line',
    data:{
      datasets:[
      {type: 'line',label:'Regressione Linenare',data:regressione,fill: "true",showline: "true",backgroundColor: "rgba(128, 128, 0, .3)", borderColor: "rgba(128, 128, 0, .3)" },
      {type: 'bubble',label: testo,backgroundColor: "rgba(255,0,0, 0.15)",borderColor: "rgba(255,0,0, .7)",dataPoints:dispersione}
    ]},
    options: {title: { display:true, text: "_____", fontSize: 20, position: 'bottom' }, scales: {xAxes:[{type: 'linear', position: 'bottom' }],events: ['clock'] }
   }
});
	
var trendChart = new Chart(cty, {
    type: 'bar',
    data: {
      labels: asse_tempo,
      datasets: [
        {
          label:staz1,
          backgroundColor: 'red',
          data: trend1,    
        }, {
          label:staz2,
          backgroundColor: "green",
          data: trend2,          

        }
      ]
    },
    options: {
      title: {
        display: true,
        text: 'Andamento Valori PM nel Periodo'
      }
    }
});
var spettroChart = new Chart(ctz, {
    type: 'bar',
    data: {
      labels: ["00-10","10-20","20-30","30-40","40-50","50-60","60-70","70-80","80-90","90-100","100-110","110-120","120-130","130-140","140-150","150-160","160-170","170-180","180-190","190-200","200>"],
      datasets: [
        {
          label:"Distribuzione Valori",
          backgroundColor: 'red',
          data: trend1,    
        }
      ]
    },
    options: {
      title: {
        display: true,
        text: 'Distribuzione tra 0 e 200 dei  Valori PM nel Periodo'
      }
    }
});

function onClick(env,a){
	consolle.log("Click");
}
function redraw_graph (chart,distr,regr,ref){
   chart.data.datasets[1].data=eval(distr);
   chart.data.datasets[0].data=eval("["+regr+"]");
   chart.data.datasets[1].label=ref;
   chart.options.title.text = ref;
   chart.update(); 
   v=eval(distr);
   trend1=[];
   trend2=[];
//   exclude=[];
   asse_tempo=[];
   spettro.fill(0);
   for (i = 0; i < v.length; i++){
//        console.log(v[i]);
	trend1.push(v[i].x);	
	trend2.push(v[i].y);	
        asse_tempo.push(i);
	if ((v[i].x < 200) && (v[i].r==3)){
		n_valori=n_valori+1;
//		console.log(parseInt(eval(v[i].x+"/10")));
		spettro[parseInt(eval(v[i].x+"/10"))]=spettro[parseInt(eval(v[i].x+"/10"))]+1;
		if (v[i].x < 50) {
			bassa=bassa+1;
		}
		else if (v[i].x >= 50 && v[i].x <100) {
			media=media+1;
		}
		else if (v[i].x >= 100 && v[i].x <200) {
			alta=alta+1;
		}
	}
	else if (v[i].r == 1) {
//		exclude.push(i);
		trend1[i]=0;
		trend2[i]=0;
	}
	else if ((v[i].x >= 200) && (v[i].r==3)) {
		spettro[20]=spettro[20]+1;
		over=over+1;
		n_valori=n_valori+1;
	}
   }
//   console.log(spettro);
   console.log(exclude);
   trendChart.data.datasets[0].data=trend1;	
   trendChart.data.datasets[1].data=trend2;	 
   trendChart.data.datasets[0].label=ref.split(" ")[1];
   trendChart.data.datasets[1].label=ref.split(" ")[3];
   trendChart.data.labels=asse_tempo;
   trendChart.update();
   spettroChart.data.datasets[0].data=spettro;
   spettroChart.update();
}

document.getElementById("scatter").onclick = function(evt){
  var activePoints = scatterChart.getElementAtEvent(evt);
//  console.log(activePoints[0]._datasetIndex);
//  console.log(activePoints[0]._index);

  // make sure click was on an actual point
  if (activePoints.length > 0) {
    var clickedDatasetIndex = activePoints[0]._datasetIndex;
    var clickedElementindex = activePoints[0]._index;
    var label = scatterChart.data.labels[clickedElementindex];
    var x = scatterChart.data.datasets[clickedDatasetIndex].data[clickedElementindex].x;
    var y = scatterChart.data.datasets[clickedDatasetIndex].data[clickedElementindex].y;
    if ( !exclude.includes(clickedElementindex)){
    	exclude.push(clickedElementindex);
    	scatterChart.data.datasets[clickedDatasetIndex].data[clickedElementindex].r=1;
    	trendChart.data.datasets[0].data[clickedElementindex]=0;
    	trendChart.data.datasets[1].data[clickedElementindex]=0;
    }
    else {
    	exclude.splice(exclude.indexOf(clickedElementindex),1);
    	scatterChart.data.datasets[clickedDatasetIndex].data[clickedElementindex].r=3;
    	trendChart.data.datasets[0].data[clickedElementindex]=x;
    	trendChart.data.datasets[1].data[clickedElementindex]=y;
    }
//    console.log(exclude);
    scatterChart.update(); 
    trendChart.update();
//    alert("Clicked: index: "+clickedElementindex + " x : "+x+" y: "+y);
  }
};

