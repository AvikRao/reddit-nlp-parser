var ctx = document.getElementById('myChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ["3:55 PM", "3:56 PM", "3:57 PM", "3:58 PM", "3:59 PM", "4:00 PM"],
        datasets: [{
            label: "Price",
            data: [110.32,112.19,109.47,109.09,110.63,111.25],
            fill: false,
            borderColor: "#FC9F41",
            pointBorderColor: "transparent",
            pointBackgroundColor: "transparent",
            pointRadius: 10,
            lineTension: 0,
            border: {
                width: 1
            }
        }]
    },
    options: {
        legend: {
            display: false,
        },
        scales: {
            yAxes: [{
                gridLines: {
                    color: "#12254a",
                    zeroLineColor: "#12254a",
                },
                ticks: {
                    beginAtZero: false,
                    fontColor: "#91ade4",
                    beginAtZero: false,
                    maxTicksLimit: 5,
                }
            }],
            xAxes: [{
                gridLines: {
                    color: "transparent",
                    zeroLineColor: "#12254a",
                },
                ticks: {
                    display: true,
                    maxTicksLimit: 3,
                    fontColor: "#91ade4"
                }
            }],
        },
        
    }
});

var ctx2 = document.getElementById('myChart2').getContext('2d');
var myChart2 = new Chart(ctx2, {
    type: 'line',
    data: {
        labels: ["3:55 PM", "3:56 PM", "3:57 PM", "3:58 PM", "3:59 PM", "4:00 PM"],
        datasets: [{
            label: "Price",
            data: [698.00, 695.12, 689.54, 690.11, 686.55, 683.21],
            fill: false,
            borderColor: "#FC9F41",
            pointBorderColor: "transparent",
            pointBackgroundColor: "transparent",
            pointRadius: 10,
            lineTension: 0,
            border: {
                width: 1
            }
        }]
    },
    options: {
        legend: {
            display: false,
        },
        scales: {
            yAxes: [{
                gridLines: {
                    color: "#12254a",
                    zeroLineColor: "#12254a",
                },
                ticks: {
                    beginAtZero: false,
                    fontColor: "#91ade4",
                    beginAtZero: false,
                    maxTicksLimit: 5,
                }
            }],
            xAxes: [{
                gridLines: {
                    color: "transparent",
                    zeroLineColor: "#12254a",
                },
                ticks: {
                    display: true,
                    maxTicksLimit: 3,
                    fontColor: "#91ade4"
                }
            }],
        },

    }
});