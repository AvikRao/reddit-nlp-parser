// obfuscate or hide later, is insecure
var API_KEY = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey=c0tlfj748v6r4maet08g'

console.log(prices);

let charts = document.querySelectorAll(".cardChart");
charts.forEach(async (ct) => {
    let ticker = ct.id.match(/(\w+)Chart/)[1].toUpperCase();
    console.log(ct.id)
    console.log(ticker);
    
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
    const myChart = new Chart(ct.getContext('2d'), {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{
                label: "Price",
                data: ticker_prices,
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
                        display: false,
                        maxTicksLimit: 3,
                        fontColor: "#91ade4"
                    }
                }],
            },

        }
    });

})