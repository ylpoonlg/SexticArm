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
$('#'+defaultTab).show();

$('#position-btn').click(() => {
    hideAllTabs();
    $('#position-tab').show();
    saveDefaultTab('position-tab');
});

$('#angle-btn').click(() => {
    hideAllTabs();
    $('#angle-tab').show();
    saveDefaultTab('angle-tab');
});

$('#file-btn').click(() => {
    hideAllTabs();
    $('#file-tab').show();
    saveDefaultTab('file-tab');
});

function hideAllTabs() {
    $('#position-tab').hide();
    $('#angle-tab').hide();
    $('#file-tab').hide();
}

function saveDefaultTab(tab) {
    let settings = JSON.parse(localStorage.sextic_settings);
    settings['control.defaultTab'] = tab;
    localStorage.sextic_settings = JSON.stringify(settings);
}


// --------FILE----------
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