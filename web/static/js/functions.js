//==========================FUNCTIONS============================

function httpGET(url, callback) {
    $.get(url, callback);
}

function httpPOST(url, data, callback) {
    $.ajax({
        url: url,
        type: 'POST',
        data: data,
        contentType: 'application/json; charset=utf-8',
        success: callback,
        error: callback
    }); 
}

const SERVER_TIMEOUT = 30*60*1000; // thirty minutes
var serverStatus;

httpGET('/get_status', (data) => {
serverStatus = data;
});