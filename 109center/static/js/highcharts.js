var chart;

/**
 * Request data from the server, add it to the graph and set a timeout
 * to request again
 */
function requestData() {
    $.ajax({
        url: '/live-data',
        success: function(point) {
            var series = chart.series[0],
                shift = series.data.length > 12; // shift if the series is
                                                 // longer than 20
            // add the point
            chart.series[0].addPoint(point, true, shift);

            // call it again after one second
            setTimeout(requestData, 10000);
        },
        cache: false
    });
}

const timezone = new Date().getTimezoneOffset()

Highcharts.setOptions({
    global: {
        timezoneOffset: timezone
    }
});
$(document).ready(function() {
    
    
    chart = new Highcharts.Chart({
        credits: {
            enabled: false
        },
        colors:['#FF9655'],
        chart: {
            renderTo: 'data-container',
            defaultSeriesType: 'spline',
            events: {
                load: requestData
            }
        },
        title: {
            text: '실시간 활동량'
        },
        xAxis: {
            type: 'datetime',
            tickPixelInterval: 200,
            gridLineWidth: 1,
            maxZoom: 20 * 1000,
            
        },
        yAxis: {
            
            title : '활동량',
            gridLineWidth: 1,
            minPadding: 0.2,
            maxPadding: 0.2,
            max:100,
            min:0
        },
        
        series: [{
            name: '활동량',
            data: []
        }]
    });
    
});
// var chart1 = new Highcharts.Chart(config);
// chart1.reflow(); //해결방법 