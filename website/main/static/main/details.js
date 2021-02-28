let ticker = document.querySelector(".detail-topic").innerHTML.toUpperCase();
console.log(ticker);

let utc_times = document.querySelectorAll(".card-text-date");

utc_times.forEach((element) => {
    element.innerHTML = new Date(parseInt(element.innerHTML) * 1000);
});

let dates = [];
let ticker_prices = [];
console.log("hi")
Object.keys(prices[ticker]).forEach((date) => {
    dates.unshift(date);
    ticker_prices.unshift(parseFloat(prices[ticker][date]));
});

dates.reverse();
ticker_prices.reverse();

console.log(dates);
console.log(ticker_prices);

var ctx = document.getElementById('detailsChart').getContext('2d');
var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'line',

    // The data for our dataset
    data: {
        labels: dates,
        datasets: [{
            label: 'Price',
            data: ticker_prices,
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
                        fontColor: "#91ade4",
                        maxTicksLimit: 10,
                    }
                }],
            },
    }
});

