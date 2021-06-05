setInterval(() => {
    refreshConsole();
}, 1000)

function refreshConsole() {
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