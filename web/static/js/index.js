//==========================DOM============================
const statusBtn = document.getElementById('status-btn');
const statusBar = document.getElementById('status-bar');
const statusText = document.getElementById('status-text');
const posText = document.getElementById('pos-text');


//==========================SETTINGS==============================
if (!localStorage.sextic_settings) {
    localStorage.sextic_settings = JSON.stringify({
        'base.hideStatus': true,
        'base.serial': '/dev/ttyACM0',
        'console.autoScroll': true,
        'control.defaultTab': 'position',
    });
}


//==========================STATUS============================
if (!JSON.parse(localStorage.sextic_settings)['base.hideStatus']) {
    statusBar.classList.replace('d-none', 'd-block');
}

statusBtn.onclick = () => {
    let settings = JSON.parse(localStorage.sextic_settings);
    if (statusBar.classList.contains('d-none')) {
        statusBar.classList.replace('d-none', 'd-block');
        settings['base.hideStatus'] = false;
    } else if (statusBar.classList.contains('d-block')) {
        statusBar.classList.replace('d-block', 'd-none');
        settings['base.hideStatus'] = true;
    }
    localStorage.sextic_settings = JSON.stringify(settings);
}

let statusInterval = setInterval(() => {
    refreshStatus();
}, 1000);

var statusTimeout;
function refreshStatus() {
    httpGET('/get_status', (data) => {
        //console.log('status: '+JSON.stringify(data));
        serverStatus = data;

        statusText.innerText = 'Connected'
        statusText.style.color = '#00ff00';
        clearTimeout(statusTimeout);

        if (serverStatus.serial) {
            $('#serial-status-text').text('Connected');
            $('#serial-status-text').css("color", "#00ff00");
        } else {
            $('#serial-status-text').text('Disconnected');
            $('#serial-status-text').css("color", "#ff0000");
        }

        let DEC_PLACE = 2;
        posText.innerHTML = `
            <h5><strong>Position</strong></h5>
            <div class="data-mono ms-3 mb-2">
                <div> X = ${serverStatus.X.toFixed(DEC_PLACE)} </div>
                <div> Y = ${serverStatus.Y.toFixed(DEC_PLACE)} </div>
                <div> Z = ${serverStatus.Z.toFixed(DEC_PLACE)} </div>
            </div>
            <h5><strong>Rotation</strong></h5>
            <div class="data-mono ms-3">
                <div> P = ${serverStatus.P.toFixed(DEC_PLACE)} </div>
                <div> E = ${serverStatus.E.toFixed(DEC_PLACE)} </div>
                <div> R = ${serverStatus.R.toFixed(DEC_PLACE)} </div>
            </div>
        `;
    });
    statusTimeout = setTimeout(() => {
        statusText.innerText = 'Disconnected';
        statusText.style.color = '#ff0000';
    }, 3000);
}

setTimeout(() => {
    clearInterval(statusInterval);
    statusText.innerText = 'Timed out';
    statusText.style.color = '#ffaa00';
}, SERVER_TIMEOUT);


//===================SERIAL=====================
const defaultSerialPort = JSON.parse(localStorage.sextic_settings)['base.serial'];
$('#serial-input').val(defaultSerialPort);

function reconnectSerial() {
    const serialPort = $('#serial-input').val();
    httpPOST('/send_cmd', `M0 ${serialPort}`, (response) => {
        console.log(response);
    });

    let settings = JSON.parse(localStorage.sextic_settings);
    settings['base.serial'] = serialPort;
    localStorage.sextic_settings = JSON.stringify(settings);
}