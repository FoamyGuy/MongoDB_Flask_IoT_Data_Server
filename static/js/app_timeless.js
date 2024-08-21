async function fetchData() {
    const response = await fetch("http://localhost:5000/temperature?device_id=test_device_002");
    const temperature_data = await response.json();
    //console.log(todos);
    return temperature_data
}

let times = [];
let temperature_values = [];

const $chartContainer = document.querySelector("#chart_container");
fetchData().then(function (temperature_data) {
    console.log("inside then() temperature_data: " + temperature_data)
    for (let i = 0; i < temperature_data.length; i++) {
        let curTemperatureData = temperature_data[i];
        console.log(curTemperatureData);
        // let $newLi = document.createElement("li")
        // $newLi.innerText = curItem.done ? "[x]: " : "[ ]: " + curItem.task;
        // $todosList.append($newLi);
        temperature_values.push(curTemperatureData.temperature);
        //times.push(curTemperatureData.timestamp["$date"]);
        times.push(i)
    }
    
    
    
      var options = {
          series: [{
          name: "Temperature",
          data: temperature_values
        }],
          chart: {
          type: 'area',
          height: 350,
          zoom: {
            enabled: false
          }
        },
        dataLabels: {
          enabled: false
        },
        stroke: {
          curve: 'straight'
        },
        
        title: {
          text: 'Temperature Readings Over Time',
          align: 'left'
        },
        subtitle: {
          text: 'Temperature C',
          align: 'left'
        },
        labels: times,
        xaxis: {
          type: 'datetime',
        },
        yaxis: {
          opposite: false
        },
        legend: {
          horizontalAlign: 'left'
        }
        };

        var chart = new ApexCharts($chartContainer, options);
        chart.render();
      
      
});


      
      