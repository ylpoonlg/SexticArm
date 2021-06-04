//==========================DOM============================
const outputText = document.getElementById('output-text');
const cmdInput = document.getElementById('cmd-input');
const statusText = document.getElementById('status-text');

//==========================INIT============================
setInterval(() => {
    refreshConsole();
}, 1000)

var statusTimeout;
function refreshConsole() {
    httpGET('/get_output', (data) => {
        try {
            statusText.innerText = 'Connected'
            statusText.style.color = '#00ff00';
            outputText.innerText = data;
        } catch {
            
        }

        clearTimeout(statusTimeout);
    });
    statusTimeout = setTimeout(() => {
        statusText.innerText = 'No Connection';
        statusText.style.color = '#ff0000';
    }, 3000);
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