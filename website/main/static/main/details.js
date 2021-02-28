var ctx = document.getElementById('detailsChart').getContext('2d');
var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'line',

    // The data for our dataset
    data: {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
        datasets: [{
            label: 'My First dataset',
            data: [0, 10, 5, 2, 20, 30, 45],
            fill: false,
            borderColor: "#FC9F41",
            pointBorderColor: "transparent",
            pointBackgroundColor: "transparent",
            pointRadius: 10,
            lineTension: 0,
        }]
    },

    // Configuration options go here
    options: {
        maintainAspectRatio: false,
            legend: {
                display: false,
            },
            scales: {
                yAxes: [{
                    gridLines: {
                        color: "#12254a",
                    },
                    ticks: {
                        beginAtZero: false,
                        fontColor: "#91ade4",
                    }
                }],
                xAxes: [{
                    gridLines: {
                        color: "#12254a",
                    },
                    ticks: {
                        display: true,
                        fontColor: "#91ade4"
                    }
                }],
            },
    }
});

let utc_times = document.querySelectorAll(".card-text-date");

utc_times.forEach((element) => {
    element.innerHTML = new Date(parseInt(element.innerHTML) * 1000);
});