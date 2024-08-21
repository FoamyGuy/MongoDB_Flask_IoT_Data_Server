const URL_BASE = "http://localhost:5000/temperature?device_id=test_device_002";

const $time_ago_value_input = document.querySelector("#time_ago_value_input");
const $time_ago_unit_select = document.querySelector("#time_ago_unit_select");
const $chartContainer = document.querySelector("#chart_container");

async function fetchData() {
    console.log("time ago val: " + $time_ago_value_input.value);
    let fetch_url;
    if ($time_ago_value_input.value !== "") {
        fetch_url = URL_BASE +
            "&time_ago_value=" + $time_ago_value_input.value +
            "&time_ago_unit=" + $time_ago_unit_select.value;
    } else {
        fetch_url = URL_BASE;
    }


    const response = await fetch(fetch_url);
    const temperature_data = await response.json();
    //console.log(todos);
    return temperature_data
}


function loadChart() {
    let times = [];
    let temperature_values = [];
    $chartContainer.innerHTML = "";
    fetchData().then(function (temperature_data) {
        console.log("inside then() temperature_data: " + temperature_data)
        for (let i = 0; i < temperature_data.length; i++) {
            let curTemperatureData = temperature_data[i];
            console.log(curTemperatureData);
            // let $newLi = document.createElement("li")
            // $newLi.innerText = curItem.done ? "[x]: " : "[ ]: " + curItem.task;
            // $todosList.append($newLi);
            temperature_values.push(curTemperatureData.temperature);
            times.push(curTemperatureData.timestamp["$date"]);
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

}

loadChart();


$time_ago_value_input.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        loadChart();

    }
});