from flask import Flask, render_template, request
import sys, os
import firmware as fw
from firmware.functions import *

app = Flask(__name__)

machine = fw.lgcode.lgcodeReader()
#machine.connectSerial('/dev/ttyACM0')

# --------ROUTE--------
@app.route('/')
def index():
    return render_template('console.html')

@app.route('/control')
def control():
    return render_template('control.html')

@app.route('/preview')
def preview():
    return render_template('preview.html')

# --------REUESTS--------
@app.route('/get_status', methods=['GET'])
def get_status():
    global machine
    status = machine.getStatus()
    if request.method == 'GET':
        return status

    return 'Invalid Request Method'

# Console
@app.route('/get_output', methods=['GET'])
def get_output():
    if request.method == 'GET':
        output = fw.functions.getConsole()
        return output

    return 'Invalid Request Method'

@app.route('/send_cmd', methods=['POST'])
def send_cmd():
    global machine
    cmd = str(request.data)[2:-1]
    if request.method == 'POST':
        machine.pushCommand(cmd)
        return f'Command Received: {cmd}'

    return 'Invalid Request Method'

@app.route('/clear_output', methods=['POST'])
def clear_output():
    if request.method == 'POST':
        fw.functions.clearConsole()
        return 'Cleared'
    return 'Invalid Request Method'

# File
@app.route('/upload_file', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['lgcodeFile']
        fileName = file.filename
        if (fileName == ''):
            return 'No file Selected'
        
        print( 'File Uploaded: '+fileName )
        newFile = open(fw.config.SCRIPT_FOLDER_PATH+fileName, 'w')
        for line in file:
            stripped = str(line)[2:-3]
            newFile.write(stripped+'\n')

        newFile.close()
        return 'Uploaded Successfully'

    return 'Invalid Request Method'

@app.route('/del_file', methods=['POST'])
def del_file():
    if request.method == 'POST':
        fileName = str(request.data)[2:-1]
        file = fw.config.SCRIPT_FOLDER_PATH+fileName
        print(file)
        if os.path.exists(file):
            os.remove(file)
            return 'Deleted'
        return 'File not found'
    
    return 'Invalid Request Method'

@app.route('/get_files', methods=['GET'])
def get_files():
    if request.method == 'GET':
        files = os.listdir(fw.config.SCRIPT_FOLDER_PATH)
        return str(files)
    
    return 'Invalid Request Method'

@app.route('/run_file', methods=['POST'])
def run_file():
    if request.method == 'POST':
        fileName = str(request.data)[2:-1]
        filePath = fw.config.SCRIPT_FOLDER_PATH + fileName
        machine.readFile(filePath)
        print('Finished running file')
        return 'Finished running'

    return 'Invalid Request Method'

if __name__ == '__main__':
    app.run(debug=True)