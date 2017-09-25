from flask import Flask, request
from os import environ, path

SC_PATH = environ.get('SC_PATH')
if not SC_PATH:
    print 'You need to set $SC_PATH.'
    exit(1)

app = Flask(__name__, root_path=path.join(SC_PATH, 'sc/'), static_url_path="/static")

with open(path.join(SC_PATH, "secret_token"), 'r') as f:
    secret_token = f.readline()

#########################################
# ENDPOINTS
#########################################

@app.route('/set', methods=['POST'])
def set():
    global secret_token
    req = request.get_json()
    try:
        token = req['token']
    except:
        return '[ERROR] Did not pass token.'
    if token != secret_token:
        return '[ERROR] Token is incorrect.'

    try:
        value = req['value']
    except:
        return '[ERROR] Did not pass value.'
    if not value:
        return '[ERROR] Value is blank.'

    with open(path.join(SC_PATH, "sc/data.txt"), 'a') as f:
        f.write(value + '\n')
    return value

@app.route('/get', methods=['POST'])
def get():
    global secret_token
    req = request.get_json()
    try:
        token = req['token']
    except:
        return '[ERROR] Did not pass token.'
    if token != secret_token:
        return '[ERROR] Token is incorrect.'

    try:
        idx = int(req['idx'])
    except:
        idx = 0
    i = -1 - idx

    with open(path.join(SC_PATH, "sc/data.txt"), 'r') as f:
        lines = f.readlines()
        if len(lines) < idx:
            value = '[ERROR] Index does not exist.'
        else:
            value = lines[i].rstrip('\n')
    return value

@app.route('/list', methods=['POST'])
def list():
    global secret_token
    req = request.get_json()
    try:
        token = req['token']
    except:
        return '[ERROR] Did not pass token.'
    if token != secret_token:
        return '[ERROR] Token is incorrect.'

    try:
        n = int(req['n'])
    except:
        n = 10

    with open(path.join(SC_PATH, "sc/data.txt"), 'r') as f:
        lines = f.readlines()
        if len(lines) < n:
            n = len(lines)
        value = ''
        for i in range(n):
            value += str(i) + ': ' + lines[-1 - i]
    return value

#########################################
# MAIN ENTRY POINT OF FLASK APP
#########################################

if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)
