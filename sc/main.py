from flask import Flask, request

SC_PATH = environ.get('SC_PATH')
if not SC_PATH:
    print 'You need to set $SC_PATH.'
    exit(1)

app = Flask(__name__, root_path=path.join(SC_PATH, 'sc/'), static_url_path="/static")

with open(path.join(SC_PATH, "sc/secret_token"), 'r') as f:
    secret_token = secret_key_file.readline()

#########################################
# ENDPOINTS
#########################################

@app.route('/set', methods=['POST'])
def set():
    global secret_token
    token = request.args.get('token', '')
    if not token:
        return 'bad'
    if token != secret_token:
        return 'bad'
    value = request.args.get('value', '')
    if not value:
        return 'bad'
    with open(path.join(SC_PATH, "sc/data.txt"), 'a') as f:
        f.write(value + '\n')
    return ''

@app.route('/get')
def get():
    global secret_token
    token = request.args.get('token', '')
    if not token:
        return 'bad'
    if token != secret_token:
        return 'bad'
    index = request.args.get('index', '')
    if index:
        idx = int(index)
    else:
        idx = 0
    i = -1 - idx
    with open(path.join(SC_PATH, "sc/data.txt"), 'r') as f:
        lines = f.readlines()
        if len(lines) < idx:
            value = 'bad'
        else:
            value = lines[i].rstrip('\n')
    return value

@app.route('/list')
def list():
    global secret_token
    token = request.args.get('token', '')
    if not token:
        return 'bad'
    if token != secret_token:
        return 'bad'
    num = request.args.get('n', '')
    if num:
        n = int(num)
    else:
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
