const fileButton = document.getElementById('select-file-btn');
const fileInput = document.getElementById('select-file-input');
const myfilesList = document.getElementById('myfiles-ls');

fileInput.value = '';

function onSelectBtnClick() {
    fileInput.click();
}

function onSelectFile() {
    let fileName = fileInput.value;
    fileName = fileName.match(/[\/\\]([\w\d\s\.\-\(\)]+)$/)[1];
    fileButton.innerText = fileName + ' selected';
}

function onUploadFile() {
    if (!fileInput.value) {
        console.log('Please select a file...');
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
            location.reload();
        }
    }
}

//-------------List Files----------------
function refreshFileList() {
    httpGET('/get_files', (data) => {
        data = data.replace(/'/g, '"');
        console.log('Files: '+data);
        let files = JSON.parse(data);
        let displayList = '';

        for (let i=0; i<files.length; i++) {
            displayList += '<div class="myfiles-ls-item row" onclick="onFileClick(\''+files[i]+'\');">';
            displayList += '<div class="col-10"><span class="myfiles-ls-text">';
            displayList += files[i];
            displayList += '</span></div>';
            displayList += '<div class="col-2">';
            const delBtnClasses = 'btn btn-sm rounded-circle btn-danger myfiles-ls-del-btn';
            displayList += '<button class="'+delBtnClasses+'" onclick="onDelFile(event, \''+files[i]+'\');">';
            displayList += '<span class="bi bi-x-circle"></span></button>';
            displayList += '</div>';
            displayList += '</div>';
        }

        myfilesList.innerHTML = displayList;
    });

}
refreshFileList();

function onFileClick(fileName) {
    console.log(fileName + ' selected');
}

function onDelFile(event, fileName) {
    event.stopPropagation();
    console.log('Deleting '+fileName);
}