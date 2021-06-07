const outputText = document.getElementById('output-text');
const cmdInput = document.getElementById('cmd-input');

var outputCache = '';
if (!sessionStorage.sextic_cmd) sessionStorage.sextic_cmd = '[]';
var currentCmd = -1;
cmdInput.value = '';

let consoleInterval = setInterval(() => {
    refreshConsole();
}, 1000)

function refreshConsole() {
    //console.log('serverStatus = '+JSON.stringify(serverStatus));
    httpGET('/get_output', (data) => {
        if (data != outputCache) {
            outputText.innerText = data;
            outputCache = data;
        }
    });
}

function onSendCommand(e) {
    console.log('send command: '+cmdInput.value);
    httpPOST('/send_cmd', cmdInput.value, (response) => {
        console.log(response);
    });

    // Store cmd to sessionStorage
    const maxCmdCache = 50;
    let commandCache = JSON.parse(sessionStorage.sextic_cmd);
    commandCache.unshift(cmdInput.value);
    if (commandCache.length > maxCmdCache) commandCache.pop();
    sessionStorage.sextic_cmd = JSON.stringify(commandCache);

    cmdInput.value = '';
}

function onClearConsole(e) {
    httpPOST('/clear_output', null, ()=>{});
}


document.onkeydown = (e) => {
    let key = e.key;

    // Command Input
    if ($('#cmd-input').is(':focus')) {
        let commandCache = JSON.parse(sessionStorage.sextic_cmd);
        if (key == "ArrowUp") {
            if (currentCmd < commandCache.length-1) {
                currentCmd++;
                cmdInput.value = commandCache[currentCmd];
            }
        } else if (key == "ArrowDown") {
            if (currentCmd > 0) {
                currentCmd--;
                cmdInput.value = commandCache[currentCmd];
            } else if (currentCmd == 0) {
                currentCmd--;
                cmdInput.value = '';
            }
        } else if (key == "Enter") {
            onSendCommand();
        }
    }
}


// Server Timeout
setTimeout(() => {
    clearInterval(consoleInterval);
}, SERVER_TIMEOUT);