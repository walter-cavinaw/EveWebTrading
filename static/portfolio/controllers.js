var portfolio = angular.module("portfolio", ['ui.bootstrap']);

portfolio.controller("StockController", function($scope, $http){

    $scope.init_data = function() {
        var currentDate = new Date();
        var currentDateString = currentDate.getFullYear() + "-" + ("0" + (currentDate.getMonth() + 1)).slice(-2) + "-" + ("0" + currentDate.getDate()).slice(-2);
        var previousDate = new Date();
        var previousDate = new Date(previousDate.setMonth(currentDate.getMonth() - 3));
        var previousDateString = previousDate.getFullYear() + "-" + ("0" + (previousDate.getMonth() + 1)).slice(-2) + "-" + ("0" + previousDate.getDate()).slice(-2);

        var main = "http://www.quandl.com/api/v1/datasets/" + $scope.stock.dataset + ".json";
        var params = "?&trim_start=" + previousDateString + "&trim_end=" + currentDateString;
        var auth = "&auth_token=sok7xuv8xDR_9LooZmaZ";
        var url = main + params + auth;
        $http.get(url).success(function (response) {
            var parseDate = d3.time.format("%Y-%m-%d").parse;
            $scope.stock.data = (response.data).map(function (d) {
                return {
                    date: parseDate(d[0]),
                    open: +d[1],
                    high: +d[2],
                    low: +d[3],
                    close: +d[4],
                    volume: +d[5]
                };
            });
            var data = $scope.stock.data;
            // array of all price data
            var recentData = data[data.length - 1];

            var closePrice = recentData.close;
            var changePrice = Number(recentData.close) - Number(recentData.open);
            changePrice = changePrice.toFixed(2);

            $scope.stock.closePrice = closePrice;
            $scope.stock.changePrice = changePrice;

            if (changePrice < 0) {
                $scope.stock.changePriceColor = "#CC0000";
            } else {
                $scope.stock.changePriceColor = "#00CC00";
            }
        });
    };
    $scope.init_data();
});

portfolio.controller('ListController', function($scope, $http){
    $scope.selected = undefined;
    $scope.init = function(stocks) {
       $scope.stocks = stocks;
   };

   $scope.add_stock = function(stock, $http){
       $scope.stocks.push(stock);
       $http.post('/add')
   };

   $scope.getLocation = function(val) {
    console.log('in get Location');
    return $http.get('http://localhost:8888/search_api', {
      params: {
        matching: val
      }
    }).then(function(response){
      return response.data.map(function(item){
        return item.name;
      });
    });
  };
});

portfolio.directive('stockChart', function(){
    return {
        restrict: 'EA',
        scope: {
            ticker: '@',
            data:'='
        },
        link: function (scope, element){
            var margin = {top: 20, right: 20, bottom: 30, left: 50};
            var width = element[0].getBoundingClientRect().width - margin.left - margin.right;
            var height = element[0].getBoundingClientRect().height - margin.top - margin.bottom;

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
            var accessor = close.accessor();
            scope.$watch('data', function(newVal){
                if (newVal) {
                    newVal.sort(function (a, b) {
                        return d3.ascending(accessor.d(a), accessor.d(b));
                    });

                    x.domain(newVal.map(accessor.d));
                    y.domain(techan.scale.plot.ohlc(newVal, accessor).domain());

                    svg.append("g")
                        .datum(newVal)
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
                }
            });
        }
    }
});