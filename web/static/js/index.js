//==========================DOM============================
const statusText = document.getElementById('status-text');
const stepperAngles = document.getElementById('stepper-angles');


//==========================STATUS============================
let statusInterval = setInterval(() => {
    refreshStatus();
}, 1000)

var statusTimeout;
function refreshStatus() {
    httpGET('/get_status', (data) => {
        //console.log('status: '+JSON.stringify(data));
        serverStatus = data;

        statusText.innerText = 'Connected'
        statusText.style.color = '#00ff00';
        clearTimeout(statusTimeout);

        let DEC_PLACE = 4;
        stepperAngles.innerHTML = `
            <li> a1 = ${data.A1.toFixed(DEC_PLACE)} </li>
            <li> a2 = ${data.A2.toFixed(DEC_PLACE)} </li>
            <li> a3 = ${data.A3.toFixed(DEC_PLACE)} </li>
            <li> a4 = ${data.A4.toFixed(DEC_PLACE)} </li>
            <li> a5 = ${data.A5.toFixed(DEC_PLACE)} </li>
            <li> a6 = ${data.A6.toFixed(DEC_PLACE)} </li>
        `;
    });
    statusTimeout = setTimeout(() => {
        statusText.innerText = 'No Connection';
        statusText.style.color = '#ff0000';
    }, 3000);
}

setTimeout(() => {
    clearInterval(statusInterval);
    statusText.innerText = 'Timed out';
    statusText.style.color = '#ffaa00';
}, SERVER_TIMEOUT);
