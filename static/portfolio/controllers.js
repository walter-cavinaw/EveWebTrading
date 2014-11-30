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