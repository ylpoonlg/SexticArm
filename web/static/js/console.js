const outputText = document.getElementById('output-text');
const cmdInput = document.getElementById('cmd-input');

let consoleInterval = setInterval(() => {
    refreshConsole();
}, 1000)

function refreshConsole() {
    //console.log('serverStatus = '+JSON.stringify(serverStatus));
    httpGET('/get_output', (data) => {
        outputText.innerText = data;
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


// Server Timeout
setTimeout(() => {
    clearInterval(consoleInterval);
}, SERVER_TIMEOUT);