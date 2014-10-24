$(document).ready(function() {
    $("#messageform").on("submit", function() {
        newMessage($(this));
        return false;
    });
    $("#messageform").on("keypress", function(e) {
        if (e.keyCode == 13) {
            newMessage($(this));
            return false;
        }
    });
    $("#message").select();
    userUpdater.start();
    chartUpdater.start();
    // TEMPORARY, wait 2 seconds for socket to establish itself before sending request
    // Make this a callback for when the socket is established
    window.setTimeout(function(){
    	chartUpdater.socket.send(JSON.stringify({ticker: "AAPL"}))
    }, 2000);
});

function newMessage(form) {
    var message = form.formToDict();
    if (message != null) {
    		console.log(message);
        userUpdater.socket.send(JSON.stringify(message));
    }
}

jQuery.fn.formToDict = function() {
    var fields = this.serializeArray();
    var json = {};
    var isEmpty = false;
    for (var i = 0; i < fields.length; i++) {
        if (fields[i].value == '') isEmpty = true;
        json[fields[i].name] = fields[i].value;
    }
    if (json.next) delete json.next;
    if (isEmpty) return null;
    return json;
};

var userUpdater = {
    socket: null,

    start: function() {
        var url = "ws://" + location.host + "/usersocket";
        userUpdater.socket = new WebSocket(url);
        userUpdater.socket.onmessage = function(event) {
            userUpdater.showMessage(JSON.parse(event.data));
        };
    },

    showMessage: function(message) {
    		console.log(message);
        if (message.type == 'notification'){
		        var node = $(message.html);
		        node.hide();
		        $("#footer").empty();
		        $("#footer").append(node);
		        node.slideDown();
      	}
    }
};

var chartUpdater = {
    socket: null,

    start: function() {
        var url = "ws://" + location.host + "/chartsocket";
        chartUpdater.socket = new WebSocket(url);
        chartUpdater.socket.onmessage = function(event) {
            chartUpdater.showMessage(JSON.parse(event.data));
        };
    },

    showMessage: function(message) {
            var datum = {
                date: parseDate(message.date),
                open: message.open,
                high: message.high,
                low: message.low,
                close: message.close,
                volume: message.volume
            };
            console.log(JSON.stringify(datum));
            data.push(datum);
            redraw();
    }
};

function checkOrder(select){
    var limit = $('#limit');
    if (select.value == 'Market'){
        limit.prop('disabled', true);
        limit.attr('placeholder', 'Limit Not Available');
    } else {
        limit.prop('disabled', false);
        limit.attr('placeholder', "Enter Limit");
    }
}
