from flask import Flask
import flask
import pickle
import os
import json
import hashlib

app = Flask(__name__)
accdab = os.path.join(os.path.dirname(__file__),'accounts.dab')

def startServer():
    app.debug = True
    app.run()

@app.route('/createaccount/', methods=['GET', 'POST'])
def createaccount():
    if flask.request.method == 'GET':
        print("GET")
        return flask.render_template('form_submit.html')
    if flask.request.method == 'POST':
        print("POST")
        username=flask.request.form['username']
        password=flask.request.form['password']
        redo = False
        unerr = ""
        pwerr = ""
        checkDatabase()
        accfile = open(accdab, 'rb')
        acc = pickle.load(accfile)
        print(acc)
        if username in acc.keys():
            username = ""
        if username == "":
            unerr = "Username is invalid or already exists"
            redo = True
        if password == "":
            pwerr = "Password is too short"
            redo = True
        if redo:
            return flask.render_template('form_submit.html', unerror=unerr, pwerror=pwerr, uname=username)
        else:
            return flask.redirect(flask.url_for('accountcreated'), code=307)

def checkDatabase():
    print("CHECK DATABASE")
    #try:
    try:
        f = open(os.path.join(os.path.dirname(__file__),'accounts.dab'), 'rb')
    except FileNotFoundError:
        f = open(os.path.join(os.path.dirname(__file__),'accounts.dab'), 'wb')
        f.close()
    try:
        with open(accdab, 'rb') as f: 
            pickle.load(f)
    except EOFError as e:
        print(e)
        f.close()
        with open(accdab, 'wb') as f: 
            pickle.dump({}, f)
    print("POST CHECK DATABASE")
    #except IOError:
        #f = open('accounts.dab', 'wb')
        #pickle.dump({}, f)
        #f.close()

@app.route('/accounts/')
def server():

    print("ACCOUNTS")
    checkDatabase()
    f = open(os.path.join(os.path.dirname(__file__),'accounts.dab'), 'rb')
    print("FILE:")
    out = f.read()
    acc = pickle.loads(out)
    f.close()
    print(acc)
    for k, v in acc.items():
        hash_object = hashlib.md5(v['password'].encode())
        print(hash_object.hexdigest())
        v['password'] = hash_object.hexdigest()
    out = pickle.dumps(acc)
    print(out)
    print(out)
    return out


@app.route('/senddata/', methods=['GET', 'POST'])
def getter():
    from ast import literal_eval
    data = flask.request.data
    print("PRE STRING")
    data = data.decode("utf-8")
    """data = str(data)
    data = data[2:]
    data = data[:-1]"""
    print("POST STRING")
    
    import json
    data = json.loads(data)
    print("POST LOAD")
    data = literal_eval(data)
    checkDatabase()
    try:
        un = data['username']
        pw = data['password']
        with open(accdab, 'rb') as acc:
            adict = pickle.load(acc)
            print(adict)
        with open(accdab, 'wb') as acc:
            hash_object = hashlib.md5(adict[un]["password"].encode())
            hash_object = hash_object.hexdigest()
            if hash_object == pw:
                del data['username']
                del data['password']
                adict[un].update(data)
            pickle.dump(adict, acc)
    except Exception as e:
        print("SEND DATA EXCEPTION", e)
    return "DATA RECEIVED: " + str(data)
    

@app.route('/')
def root():
    return flask.redirect(flask.url_for('createaccount'), code=302)

# Define a route for the action of the form, for example '/hello/'
# We are also defining which type of requests this route is 
# accepting: POST requests in this case
@app.route('/accountcreated/', methods=['POST'])
def accountcreated():
    username=flask.request.form['username']
    password=flask.request.form['password']
    with open(accdab, 'rb') as acc:
        adict = pickle.load(acc)
    with open(accdab, 'wb') as acc:
        adict[username] = {}
        adict[username]["password"] = password
        pickle.dump(adict, acc)
        print(adict)
    return flask.render_template('form_action.html', username=username, password=password)

if __name__ == "__main__":
    startServer()