// Copyright 2009 FriendFeed
//
// Licensed under the Apache License, Version 2.0 (the "License"); you may
// not use this file except in compliance with the License. You may obtain
// a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
// WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
// License for the specific language governing permissions and limitations
// under the License.

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
    var json = {}
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
        chartUpdater.socket.onmessage = function(data) {
            chartUpdater.showMessage(data);
        };
    },

    showMessage: function(message) {
    		console.log(message);
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
