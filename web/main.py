from flask import Flask, render_template, request
import sys
import firmware as fw

app = Flask(__name__)

msg = ''

@app.route("/")
def index():
    global msg
    return render_template('index.html')

@app.route("/mokka", methods=['POST', 'GET'])
def mokka():
    if request.method == 'POST':
        global msg
        msg += 'mokka '
        print(msg)
        return 'post'
    elif request.method == 'GET':
        return msg

    return 'Invalid Request Method'

@app.route("/get_output", methods=['GET'])
def get_output():
    if request.method == 'GET':
        output = fw.functions.getConsole()
        # print('the output is:')
        # print(output)
        return output

    return 'Invalid Request Method'

@app.route("/send_cmd", methods=['POST'])
def send_cmd():
    cmd = str(request.data)[2:-1]
    if request.method == 'POST':
        reader = fw.lgcode.lgcodeReader()
        reader.decExeCommand(cmd)
        return 'Command Sent'

    return 'Invalid Request Method'

@app.route("/clear_output", methods=['POST'])
def clear_output():
    if request.method == 'POST':
        fw.functions.clearConsole()
        return 'Cleared'
    return 'Invalid Request Method'

if __name__ == '__main__':
    app.run(debug=True)