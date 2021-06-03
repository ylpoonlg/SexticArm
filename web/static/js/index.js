const msgText = document.getElementById('msg-text');
const cmdInput = document.getElementById('cmd-input');

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


httpGET('/get_output', (data, status) => {
    msgText.innerText = data;
});

function refreshConsole() {
    httpGET('/get_output', (data, status) => {
        msgText.innerText = data;
    });
}

function onSendCommand(e) {
    console.log('send command: '+cmdInput.value);
    httpPOST('/send_cmd', cmdInput.value, (response) => {
        console.log(response);
    });
}

function onClearConsole(e) {
    httpPOST('/clear_output', null, ()=>{});
}

setInterval(() => {
    refreshConsole();
}, 1000)