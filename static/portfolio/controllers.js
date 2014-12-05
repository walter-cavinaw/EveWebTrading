var portfolio = angular.module("portfolio", []);

portfolio.controller("stockController", function($scope, $http){

    $scope.init = function(stocks){
        $scope.stocks = stocks;

        console.log(stocks);

        for(stock of stocks){
            console.log(stock.ticker);

            var currentDate = new Date();
            var currentDateString = currentDate.getFullYear() + "-" + ("0" + (currentDate.getMonth() + 1)).slice(-2) + "-" + ("0" + currentDate.getDate()).slice(-2);
            var previousDate = new Date();
            var previousDate = new Date(previousDate.setMonth(currentDate.getMonth() - 3));
            var previousDateString = previousDate.getFullYear() + "-" + ("0" + (previousDate.getMonth() + 1)).slice(-2) + "-" + ("0" + previousDate.getDate()).slice(-2);

            var main = "http://www.quandl.com/api/v1/datasets/WIKI/" + stock.ticker + ".json";
            var params = "?&trim_start=" + previousDateString + "&trim_end=" + currentDateString;
            var auth = "&auth_token=sok7xuv8xDR_9LooZmaZ";
            var url = main+params+auth;

            (function(stock){$http.get(url).success(function(response){

                stock.response = response;

                var data = response.data;

                var closeIndex = response.column_names.indexOf("Close");
                var openIndex = response.column_names.indexOf("Open");

                // array of all price data
                var recentData = data[data.length-1];

                var closePrice = recentData[closeIndex];
                console.log(closePrice);
                var changePrice = Number(recentData[closeIndex]) - Number(recentData[openIndex]);
                changePrice = changePrice.toFixed(2);
                console.log(changePrice);

                stock.closePrice = closePrice;
                stock.changePrice = changePrice;

                if(changePrice < 0){
                    stock.changePriceColor = "#CC0000";
                } else{
                    stock.changePriceColor = "#00CC00";
                }
            })})(stock);
        }

    };

});

portfolio.controller('ListController', function($scope){
   $scope.init = function(stocks){
       $scope.stocks = stocks;
   }
});

portfolio.directive('stockChart', function(){
    return {
        restrict: 'EA',
        scope: {
            ticker: '@'
        },
        link: function (scope, element, attrs){
            var margin = {top: 20, right: 20, bottom: 30, left: 50};
            var width = element[0].getBoundingClientRect().width - margin.left - margin.right;
            var height = element[0].getBoundingClientRect().height - margin.top - margin.bottom;
            var currentDate = new Date;
            var currentDateString = currentDate.getFullYear() + "-" + ("0" + (currentDate.getMonth() + 1)).slice(-2) + "-" + ("0" + currentDate.getDate()).slice(-2);
            var previousDate = new Date;
            var previousDate = new Date(previousDate.setMonth(currentDate.getMonth() - 3));
            var previousDateString = previousDate.getFullYear() + "-" + ("0" + (previousDate.getMonth() + 1)).slice(-2) + "-" + ("0" + previousDate.getDate()).slice(-2);
            var query = "http://www.quandl.com/api/v1/datasets/WIKI/" + scope.ticker + ".json";
            var params = "?&trim_start=" + previousDateString + "&trim_end=" + currentDateString;
            var auth = "&auth_token=sok7xuv8xDR_9LooZmaZ";
            var url = query+params+auth;
            var svg = d3.select(element[0]).append("svg")   // this needs to be fixed
                    .attr("width", width + margin.left + margin.right)
                    .attr("height", height + margin.top + margin.bottom)
                    .append("g")
                    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
            var parseDate = d3.time.format("%Y-%m-%d").parse;

            var x = techan.scale.financetime()
                .range([0, width])
                .outerPadding(0);

            var y = d3.scale.linear()
                .range([height, 0]);

            var close = techan.plot.close()
                .xScale(x)
                .yScale(y);

            var xAxis = d3.svg.axis()
                .scale(x)
                .orient("bottom");

            var yAxis = d3.svg.axis()
                .scale(y)
                .orient("left");
            d3.json(url, function (error, data) {
                var accessor = close.accessor();
                data = data.data;
                data = data.map(function (d) {
                    return {
                        date: parseDate(d[0]),
                        open: +d[1],
                        high: +d[2],
                        low: +d[3],
                        close: +d[4],
                        volume: +d[5]
                    };
                }).sort(function (a, b) {
                    return d3.ascending(accessor.d(a), accessor.d(b));
                });

                x.domain(data.map(accessor.d));
                y.domain(techan.scale.plot.ohlc(data, accessor).domain());

                svg.append("g")
                    .datum(data)
                    .attr("class", "close")
                    .call(close);

                svg.append("g")
                    .attr("class", "x axis")
                    .attr("transform", "translate(0," + height + ")")
                    .call(xAxis);

                svg.append("g")
                    .attr("class", "y axis")
                    .call(yAxis)
                    .append("text")
                    .attr("transform", "rotate(-90)")
                    .attr("y", 6)
                    .attr("dy", ".71em")
                    .style("text-anchor", "end")
                    .text("Price ($)");
            });
        }
    }
});