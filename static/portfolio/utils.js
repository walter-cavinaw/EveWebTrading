var margin = {top: 20, right: 20, bottom: 30, left: 50}

var drawChartFromTicker = function(ticker, row) {

    var chartId = ticker + "chart";
    var elem = '#' + chartId;

    var chartElement = $(elem);
    var summaryElement = row.find(".summary");
    var newsElement = row.find(".news");

    // var url = "http://query.yahooapis.com/v1/public/yql?q=";

    var currentDate = new Date();
    var currentDateString = currentDate.getFullYear() + "-" + ("0" + (currentDate.getMonth() + 1)).slice(-2) + "-" + ("0" + currentDate.getDate()).slice(-2);
    var previousDate = new Date();
    ;
    var previousDate = new Date(previousDate.setMonth(currentDate.getMonth() - 3));
    var previousDateString = previousDate.getFullYear() + "-" + ("0" + (previousDate.getMonth() + 1)).slice(-2) + "-" + ("0" + previousDate.getDate()).slice(-2);

    /*
     // Previous query from yahoo finance
     var query = 'select * from yahoo.finance.historicaldata where symbol = "'
     + ticker
     + '" and startDate = "'
     + date6MonthsAgoString
     + '" and endDate = "'
     + currentDateString
     + '"';
     query = query + "&format=json&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback=";
     */

    var query = "http://www.quandl.com/api/v1/datasets/WIKI/" + ticker + ".json";
    var params = "?&trim_start=" + previousDateString + "&trim_end=" + currentDateString;
    var auth = "&auth_token=sok7xuv8xDR_9LooZmaZ";
    var url = query+params+auth;
    var chart_width = document.getElementById(ticker+"chart").clientWidth;
    console.log(chart_width);


    var width = document.getElementById(chartId).getBoundingClientRect().width - margin.left - margin.right;
    var height = document.getElementById(chartId).getBoundingClientRect().height - margin.top - margin.bottom;

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
    var svg = d3.select(elem).append("svg")   // this needs to be fixed
             .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    d3.json(url, function (error, data) {
        var accessor = close.accessor();
        data = data.data;
        data = data.map(function(d) {
            return {
                date: parseDate(d[0]),
                open: +d[1],
                high: +d[2],
                low: +d[3],
                close: +d[4],
                volume: +d[5]
            };
        }).sort(function(a, b) { return d3.ascending(accessor.d(a), accessor.d(b)); });

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
    var recentData = data[data.length-1];
    var closePrice = recentData.close;
	var changePrice = Number(recentData.close) - Number(recentData.open);
	changePrice = changePrice.toFixed(2);

	summaryElement.append("<strong style='font-size: 200%'>" + closePrice + "</strong>");
	summaryElement.append($("<br>"));
	if(changePrice == 0){
		summaryElement.append("<strong style='font-size: 200%; color: black'>" + changePrice + "</strong>");
	}	else if(changePrice < 0){
		summaryElement.append("<strong style='font-size: 200%; color: #CC0000'>" + changePrice + "</strong>");
	} else{
		summaryElement.append("<strong style='font-size: 200%; color: #00CC00'>" + changePrice + "</strong>");
	}
    });
};

var updateChart = function(init, ticker){
    var id = ticker + "chart";
    var width = document.getElementById(id).getBoundingClientRect().width - margin.left - margin.right;
    var height = document.getElementById(id).getBoundingClientRect().height - margin.top - margin.bottom;
    console.log(width+","+height);
    var elem = "#" + id;
    var svg = d3.select(elem).select('svg');
    svg.attr("height", height + margin.top + margin.bottom);
    svg.attr('width', width + margin.left + margin.right);

    var x = techan.scale.financetime()
               .range([0, width])
               .outerPadding(0);
    var y = d3.scale.linear()
             .range([height, 0]);
    x.range([0, width]);
    y.range([height, 0]);
    var close = techan.plot.close()
             .xScale(x)
             .yScale(y);
    var xAxis = d3.svg.axis()
             .scale(x)
             .orient("bottom");
    var yAxis = d3.svg.axis()
             .scale(y)
             .orient("left");

    svg.select('.close')
        .call(close);
    svg.select('.x.axis')
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);
    svg.select('.y.axis')
        .call(yAxis);
};

$('.update').on('shown.bs.collapse', function (){
    var ticker = $(this).parent().attr('id');
    updateChart(false, ticker);
});
