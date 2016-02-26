from flask import Flask
import flask
import pickle
import os
import json
import hashlib

app = Flask(__name__)
accdab = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "data/accounts.dab"))
statdab = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "data/stats.dab"))

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

@app.route("/ip")
def clientip():
    import os
    openip = os.environ("HTTP_X_CLIENT_IP") 
    flaskip = flask.request.environ.get('HTTP_X_REAL_IP', flask.request.remote_addr)
    return "OPEN IP:\n" + openip + "\nFLASK IP:\n" + flaskip


def checkDatabase():
    print("CHECK DATABASE")
    try:
        f = open(accdab, 'rb')
    except FileNotFoundError:
        print("FILE NOT FOUND")
        f = open(accdab, 'wb')
        f.close()
    try:
        with open(accdab, 'rb') as f: 
            pickle.load(f)
    except EOFError as e:
        print("EOFERROR")
        print(e)
        f.close()
        with open(accdab, 'wb') as f: 
            pickle.dump({}, f)
    print("POST CHECK DATABASE")
    
    #Statistics Database
    print("CHECK STATS")
    try:
        f = open(statdab, 'rb')
    except FileNotFoundError:
        print("FILE NOT FOUND")
        f = open(statdab, 'wb')
        f.close()
    try:
        with open(statdab, 'rb') as f: 
            pickle.load(f)
    except EOFError as e:
        print("EOFERROR")
        print(e)
        f.close()
        with open(statdab, 'wb') as f: 
            pickle.dump({"calltimes": [], "crashes": []}, f)
    print("POST CHECK STATS")

@app.route('/accounts/')
def server():

    print("ACCOUNTS")
    checkDatabase()
    f = open(accdab, 'rb')
    print("FILE:")
    out = f.read()
    acc = pickle.loads(out)
    f.close()
    print(acc)
    """for k, v in acc.items():
        hash_object = hashlib.md5(v['password'].encode())
        print(hash_object.hexdigest())
        v['password'] = hash_object.hexdigest()"""
    out = pickle.dumps(acc)
    print(out)
    print(out)
    return out

@app.route('/leaderboard')
def leaderboard():
    checkDatabase()
    with open(accdab, "rb") as acc:
        accs = pickle.load(acc)
    
    for k, v in accs.items():
        print("USER:", k)
        for k, v in v.items():
            print(k, v)
    #names = [k for k in accs.keys() if "xp" in accs[k].keys()]
    names = accs.keys()
    print(names)
    table = {}
    for n in names:
        if "xp" in accs[n].keys():
            table[n] = accs[n]["xp"]
        else:
            table[n] = 0
    #table = {"Borris": 5, "John": 10, "James": 9485, "Tim": 1, "Fred": 456}
    order = sorted(table, key=table.__getitem__, reverse=True)
    return flask.render_template('leaderboard.html', tout=table, korder=order, num=1)

@app.route('/calltimes/')
def calltimes():
    from collections import Counter
    checkDatabase()
    with open(statdab, "rb") as sf:
        stats = pickle.load(sf)
        stats = stats["calltimes"]
        total = Counter({})
        for s in stats:
            a = Counter(s)
            total = total + a
        #total = dict(total)
        for k, v in total.items():
            total[k] = v / len(stats)
            total[k] = round(total[k], 4)
        print(total)
    
    order = sorted(total, key=total.__getitem__, reverse=True)
    return flask.render_template('calltimes.html', korder=order, tout=total)


@app.route('/senddata/', methods=['GET', 'POST'])
def getter():
    from ast import literal_eval
    data = flask.request.data
    data = data.decode("utf-8")
    data = json.loads(data)
    data = literal_eval(data)
    checkDatabase()
    #Statistics and crashes
    try:
        if 'calltimes' in data.keys():
            ct = data["calltimes"]
            with open(statdab, 'rb') as acc:
                sdict = pickle.load(acc)
                print(sdict)
            with open(statdab, 'wb') as acc:
                sdict["calltimes"].append(ct)
                pickle.dump(sdict, acc)
    except Exception as e:
        print("SEND DATA EXCEPTION", e)
        
    
    #userdata
    try:
        un = data['username']
        pw = data['password']
        with open(accdab, 'rb') as acc:
            adict = pickle.load(acc)
            print(adict)
        with open(accdab, 'wb') as acc:
            if adict[un]["password"] == pw:
                del data['username']
                del data['password']
                adict[un].update(data)
            pickle.dump(adict, acc)
    except Exception as e:
        print("SEND DATA EXCEPTION", e)
    return "DATA RECEIVED: " + str(data)
    

@app.route('/')
def root():
    #return flask.redirect(flask.url_for('createaccount'), code=302)
    return flask.render_template('home.html')

@app.route('/accountcreated/', methods=['POST'])
def accountcreated():
    username=flask.request.form['username']
    password=flask.request.form['password']
    with open(accdab, 'rb') as acc:
        adict = pickle.load(acc)
    with open(accdab, 'wb') as acc:
        adict[username] = {}
        hash_object = hashlib.md5(password.encode())
        hash_object = hash_object.hexdigest()
        adict[username]["password"] = hash_object
        pickle.dump(adict, acc)
        print(adict)
    return flask.render_template('form_action.html', username=username, password=password)

if __name__ == "__main__":
    accdab = os.path.join(os.path.dirname(__file__),'accounts.dab')
    startServer()