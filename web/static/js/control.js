const infoBox = document.getElementById('info-box');
const curFileText = document.getElementById('cur-file-text');
const delSelButton = document.getElementById('desel-btn');
const fileButton = document.getElementById('select-file-btn');
const fileInput = document.getElementById('select-file-input');
const runButton = document.getElementById('run-file-btn');
const stopButton = document.getElementById('stop-file-btn');
const myfilesList = document.getElementById('myfiles-ls');

fileInput.value = '';
var curFile = '';

//-----------------Info box----------------------
let controlInfoInterval = setInterval(() => {
    refreshControlInfo();
}, 1000);

function refreshControlInfo() {
    let DEC_PLACE = 4;
    infoBox.innerHTML = `
        <div class="data-mono row container">
            <div class="col-6">
                <h5 style="word-wrap: break-word;">Position/Rotation</h5>
                <div> X = ${serverStatus.X.toFixed(DEC_PLACE)} </div>
                <div> Y = ${serverStatus.Y.toFixed(DEC_PLACE)} </div>
                <div> Z = ${serverStatus.Z.toFixed(DEC_PLACE)} </div>
                <div> P = ${serverStatus.P.toFixed(DEC_PLACE)} </div>
                <div> E = ${serverStatus.E.toFixed(DEC_PLACE)} </div>
                <div> R = ${serverStatus.R.toFixed(DEC_PLACE)} </div>
            </div>
            <div class="col-6">
                <h5>Steppers</h5>
                <div> a1 = ${serverStatus.A1.toFixed(DEC_PLACE)} </div>
                <div> a2 = ${serverStatus.A2.toFixed(DEC_PLACE)} </div>
                <div> a3 = ${serverStatus.A3.toFixed(DEC_PLACE)} </div>
                <div> a4 = ${serverStatus.A4.toFixed(DEC_PLACE)} </div>
                <div> a5 = ${serverStatus.A5.toFixed(DEC_PLACE)} </div>
                <div> a6 = ${serverStatus.A6.toFixed(DEC_PLACE)} </div>
            </div>
        </div>
    `;
}

setTimeout(() => {
    clearInterval(controlInfoInterval);
}, SERVER_TIMEOUT);


//--------TABS---------
hideAllTabs();
const defaultTab = JSON.parse(localStorage.sextic_settings)['control.defaultTab'];
$('#'+defaultTab+'-tab').show();
$('#'+defaultTab+'-btn').addClass('active');

$('#position-btn').click(() => {
    hideAllTabs();
    $('#position-tab').show();
    $('#position-btn').addClass('active');
    saveDefaultTab('position');
});

$('#angle-btn').click(() => {
    hideAllTabs();
    $('#angle-tab').show();
    $('#angle-btn').addClass('active');
    saveDefaultTab('angle');
});

$('#file-btn').click(() => {
    hideAllTabs();
    $('#file-tab').show();
    $('#file-btn').addClass('active');
    saveDefaultTab('file');
});

function hideAllTabs() {
    $('#position-tab').hide();
    $('#angle-tab').hide();
    $('#file-tab').hide();
    $('#position-btn').removeClass('active');
    $('#angle-btn').removeClass('active');
    $('#file-btn').removeClass('active');
}

function saveDefaultTab(tab) {
    let settings = JSON.parse(localStorage.sextic_settings);
    settings['control.defaultTab'] = tab;
    localStorage.sextic_settings = JSON.stringify(settings);
}



//---------POSITION----------
function sendControl(btn) {
    const STEP = 10;
    const STEP_DEG = 10;
    let newPos = serverStatus;
    switch (btn) {
        case 'L1':
            newPos.Z += STEP;
            break;
        case 'L2':
            newPos.Y += STEP;
            break;
        case 'L3':
            newPos.Z -= STEP;
            break;

        case 'L4':
            newPos.X -= STEP;
            break;
        case 'L5': // Home
            httpPOST('/send_cmd', 'G10', (response) => {
                console.log(response);
            });
            return;
        case 'L6':
            newPos.X += STEP;
            break;
        case 'L8':
            newPos.Y -= STEP;
            break;
        
        // Rotation
        case 'R1':
            newPos.R -= STEP_DEG;
            break;
        case 'R2':
            newPos.E += STEP_DEG;
            break;
        case 'R3':
            newPos.R += STEP_DEG;
            break;
        case 'R4':
            newPos.P += STEP_DEG;
            break;
        case 'R6':
            newPos.P -= STEP_DEG;
            break;
        case 'R8':
            newPos.E -= STEP_DEG;
            break;
    }

    serverStatus = newPos;

    let cmd = `G1 X${newPos.X} Y${newPos.Y} Z${newPos.Z} P${newPos.P} E${newPos.E} R${newPos.R} F3`;

    httpPOST('/send_cmd', cmd, (response) => {
        console.log(response);
    });
}




//----------ANGLE-----------

$('#submit-angles-btn').click(() => {
    let a1 = $('input[name=a1]').val();
    let a2 = $('input[name=a2]').val();
    let a3 = $('input[name=a3]').val();
    let a4 = $('input[name=a4]').val();
    let a5 = $('input[name=a5]').val();
    let a6 = $('input[name=a6]').val();

    const cmd = `G0 A1${a1} A2${a2} A3${a3} A4${a4} A5${a5} A6${a6}`;
    httpPOST('/send_cmd', cmd, (response) => {
        console.log(response);
    });
});

function changeAngle(stepper, dir=1) {
    const amt = 10;

    let inputBox = $(`input[name=${stepper}]`);
    let oldVal = parseFloat(inputBox.val());
    inputBox.val( oldVal + amt * dir );

    // Run directly after pressing
    $('#submit-angles-btn').click();
}



//--------FILE----------
function onSelectBtnClick() {
    fileInput.click();
}

function onSelectFile() {
    let fileName = fileInput.value;
    fileName = fileName.match(/[\/\\]([\w\d\s\.\-\(\)]+)$/)[1];
    fileButton.innerText = fileName;
}

function onUploadFile() {
    if (!fileInput.value) {
        console.log('Please select a file...');
        fileButton.innerText = 'Please select a file';
        return;
    }

    let file = fileInput.files[0];

    let formData = new FormData();
    formData.append('lgcodeFile', file);

    const xhr = new XMLHttpRequest();
    xhr.open('post', '/upload_file');
    xhr.send(formData);

    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            //location.reload();
            refreshFileList();
            fileButton.innerText = 'Select a .lgcode file';
            fileInput.value = '';
        }
    }
}

//-------------List Files----------------
function refreshFileList() {
    httpGET('/get_files', (data) => {
        data = data.replace(/'/g, '"');
        let files = JSON.parse(data);
        let displayList = '';

        for (let i=0; i<files.length; i++) {
            displayList += '<div class="myfiles-ls-item row" onclick="onFileClick(\''+files[i]+'\');">';
            displayList += '<div class="col-10"><span class="myfiles-ls-text">';
            displayList += files[i];
            displayList += '</span></div>';
            displayList += '<div class="col-2">';
            const delBtnClasses = 'btn btn-sm btn-outline-danger myfiles-ls-del-btn';
            displayList += '<button class="'+delBtnClasses+'" onclick="onDelFile(event, \''+files[i]+'\');">';
            displayList += '<i class="bi bi-file-earmark-x"></i></button>';
            displayList += '</div>';
            displayList += '</div>';
        }

        myfilesList.innerHTML = displayList;
    });

}
refreshFileList();

function onFileClick(fileName) {
    console.log(fileName + ' selected');
    curFile = fileName;
    curFileText.innerText = 'File selected: ' + fileName;
    runButton.removeAttribute('disabled');
    delSelButton.removeAttribute('hidden');
}

function onDeselectFile() {
    curFile = '';
    curFileText.innerText = 'No file is selected...';
    runButton.setAttribute('disabled', '');
    delSelButton.setAttribute('hidden', '');
}

function onDelFile(event, fileName) {
    event.stopPropagation();

    if (confirm('Do you really want to delete '+fileName+' from the server?')) {
        console.log('Deleting '+fileName);
        httpPOST('/del_file', fileName, ()=>{
            refreshFileList();
        });
    }
}


function runFile() {
    runButton.setAttribute('disabled', '');
    stopButton.removeAttribute('disabled');

    httpPOST('/run_file', curFile, (response) => {
        console.log('Run File Response: '+response);
        runButton.removeAttribute('disabled');
        stopButton.setAttribute('disabled', '');    
    })
    console.log('Continue after run file');
}

function stopFile() {
    runButton.removeAttribute('disabled');
    stopButton.setAttribute('disabled', '');
}



// Keyboard Control
document.onkeydown = (e) => {
    let key = e.key;

    let tab = JSON.parse(localStorage.sextic_settings)['control.defaultTab'];
    if (tab == 'position') {

    } else if (tab == 'angle') {
        if (key == 'Enter') {
            $('#submit-angles-btn').click();
        }
    } else if (tab == 'file') {

    }
}