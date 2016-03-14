from flask import Flask
import flask
import pickle
import os
import json
import hashlib
import time

app = Flask(__name__)
accdab = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "data/accounts.dab"))
statdab = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "data/stats.dab"))
serverdab = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "data/servers/"))

app.secret_key = "J\x92\x1f\x98\xbd\xf2}>\xf3\x85\x06\x9e\xc2\x99h\x99\xb5\xf9\xab\xb5\x85\xe9\x8d\x96"

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
        with open(accdab, 'rb') as accfile:
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

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        print("GET")
        return flask.render_template('form_login.html')
    if flask.request.method == 'POST':
        print("POST")
        username=flask.request.form['username']
        password=flask.request.form['password']
        redo = False
        unerr = ""
        pwerr = ""
        checkDatabase()
        with open(accdab, 'rb') as accfile:
            acc = pickle.load(accfile)
        print(acc)
        if username in acc.keys():
            password = hashlib.md5(password.encode())
            password = password.hexdigest()
            if password == acc[str(username)]["password"]:
                flask.session["username"] = username
            else:
                print(password, acc[str(username)]["password"])
                pwerr = "Incorrect password"
                redo = True
        else:
            unerr = "That username doesn't exist"
            redo = True
        if redo:
            return flask.render_template('form_login.html', unerror=unerr, pwerror=pwerr, uname=username)
        else:
            return flask.redirect(flask.url_for('root'), code=302)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    flask.session["username"] = ""
    return flask.redirect(flask.url_for('root'))


def checkDatabase():
    print("CHECK DATABASE")
    try:
        with open(accdab, 'rb') as f:
            pass
    except FileNotFoundError:
        print("FILE NOT FOUND")
        with open(accdab, 'wb') as f:
            pass
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
        with open(statdab, 'rb') as f:
            pass
    except FileNotFoundError:
        print("FILE NOT FOUND")
        with open(statdab, 'wb') as f:
            pass
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

def checkServers():
    with open(accdab, "rb") as acc:
        accounts = pickle.load(acc)
        for name, value in accounts.items():
            if "servers" in value.keys():
                for sv in value["servers"]:
                    file = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "data/servers/" + sv["name"] + ".dab"))
                    if not os.path.exists(file):
                        with open(file, "wb") as svr:
                            pickle.dump({}, svr)
                    try:
                        with open(file, 'rb') as svr: 
                            pickle.load(svr)
                    except EOFError as e:
                        with open(file, 'rb') as svr:
                            print("CHECK SERVERS EOFERROR" + str(svr.read()))
                        with open(file, 'wb') as svr: 
                            pickle.dump({}, svr)
                    with open(file, "rb") as svr:
                        dab = pickle.load(svr)
                        if not "players" in dab.keys():
                            dab["players"] = {}
                    dab["name"] = sv["name"]
                    dab["password"] = sv["password"]
                    dab["admin"] = sv["admin"]
                    try:
                        for player, value in dab["players"].items():
                            if time.time() - value["last call"] > 5:
                                dab["players"][player]["online"] = False
                    except Exception as e:
                        print(e)
                    with open(file, "wb") as sv:
                        pickle.dump(dab, sv)
                            


@app.route('/accounts/')
def accounts():
    print("ACCOUNTS")
    checkDatabase()
    with open(accdab, 'rb') as f:
        print("FILE:")
        out = f.read()
        acc = pickle.loads(out)
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

@app.route('/crashes/')
def crashes():
    """from collections import Counter
    checkDatabase()
    with open(statdab, "rb") as sf:
        stats = pickle.load(sf)
        stats = stats["crash"]
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
    return flask.render_template('calltimes.html', korder=order, tout=total)"""
    try:
        with open(statdab, "rb") as sf:
            stats = pickle.load(sf)
            stats = stats["crashes"]
            return str(stats)
    except Exception as e:
        print("EXCEPTION: " + e)


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
        if 'crash' in data.keys():
            ct = data["crash"]
            with open(statdab, 'rb') as acc:
                sdict = pickle.load(acc)
                print(sdict)
            with open(statdab, 'wb') as acc:
                sdict["crashes"].append(ct)
                pickle.dump(sdict, acc)
    except Exception as e:
        print("SEND DATA EXCEPTION", str(e))
        
    
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
    return flask.render_template('home.html')

#####
#Begin python module paths
#####
"""@app.route('/static/<path:filename>')
def serve_static(filename):
    print(filename)
    return flask.send_from_directory('static', filename)

@app.route('/game/runGame.<cache>')
def sendCache(cache):
    print("SEND CACHE")
    print('static/LOA2/output/runGame.' + str(cache))
    return flask.send_file('static/LOA2/output/runGame.' + str(cache))

@app.route('/game/\\static\\LOA2\\output\\bootstrap.js')
def sendBootstrap():
    print("send bootstrap")
    return flask.send_file('static/LOA2/output/bootstrap.js')

@app.route('/game/lib/<file>')
def sendGameLib(file):
    print("SEND Lib FILE: " + file)
    return flask.send_file('static/LOA2/output/lib/' + file)

@app.route('/game/Resources/Fonts/<file>')
def sendGameFIle(file):
    print("SEND Resource Font FILE: " + file)
    return flask.send_file('static/LOA2/Resources/Fonts/' + file)"""

@app.route('/game/<filename>')
def sendModule(filename):
    print("sendModule", filename)
    if "_pygame_" in filename:
        filename = filename.replace("_pygame_", "")
        return flask.send_file('static/pygame/' + filename)
    elif filename == "_saves_mapFile.py":
        return flask.send_file('static/LOA/Saves/__init__.py')
    elif filename == "requests.py":
        return flask.send_file('static/LOA/requests/__init__.py')
    elif not filename == "pygame.py":
        try:
            return flask.send_file('static/LOA/' + filename)
        except FileNotFoundError:
            try:
                return flask.send_file('static/pygame/' + filename)
            except FileNotFoundError:
                return flask.send_file('static/brython/Lib/site-packages/' + filename.replace(".py", "") + "/__init__.py")
    else:
        return flask.send_file('static/pygame/__init__.py')

@app.route('/Lib/<filename>')
def sendLibModule(filename):
    print("sendModule", filename)
    return flask.send_file('static/brython/Lib/' + filename)

@app.route('/Lib/<filename>/__init__.py')
def sendLibModuleInit(filename):
    print("sendModule", filename, "__init__.py")
    return flask.send_file('static/brython/Lib/' + filename + "/__init__.py")

@app.route('/Lib/<path>/<filename>')
def sendLibModuleFolder(path, filename):
    print("sendModule", filename, "__init__.py")
    return flask.send_file('static/brython/Lib/' + path + "/" + filename)

@app.route('/libs/<filename>')
def sendLibsModule(filename):
    print("sendModule", filename)
    return flask.send_file('static/brython/libs/' + filename)

#####
#End python module paths
#####

@app.route('/game/')
def game(): #{pythonpath:['/static/src']}
    return flask.render_template("game.html")
    #return flask.send_from_directory('static', "game.html")

@app.context_processor
def inject_user():
    if not "username" in flask.session:
        flask.session["username"] = ""
    return dict(user=flask.session["username"])


@app.route('/accountcreated/', methods=['POST'])
def accountcreated():
    username=flask.request.form['username']
    password=flask.request.form['password']
    with open(os.path.join(os.path.dirname(__file__), "env.txt"), "r") as env:
        ip = env.read()
    with open(accdab, 'rb') as acc:
        adict = pickle.load(acc)
    with open(accdab, 'wb') as acc:
        adict[username] = {}
        hash_object = hashlib.md5(password.encode())
        hash_object = hash_object.hexdigest()
        adict[username]["password"] = hash_object
        adict[username]["ip"] = ip
        pickle.dump(adict, acc)
        print(adict)
    flask.session["username"] = username
    return flask.render_template('form_action.html', username=username, password=password)


@app.route("/mp/<server>/manage")
def serverView(server):
    checkServers()
    return flask.render_template('view_server.html', name=server)

@app.route("/mp/<server>/get")
def serverGet(server):
    checkServers()
    file = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "data/servers/" + server + ".dab"))
    with open(file, 'rb') as svr:
        sdict = pickle.load(svr)
    return str(sdict)



@app.route("/mp/<server>", methods=['GET','POST'])
def mp(server):
    #print("SERVER:", server)
    file = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "data/servers/" + server + ".dab"))
    checkServers()
    #print("BROWSER:", flask.request.user_agent.browser)
    if flask.request.method == "GET":
        if not flask.request.user_agent.browser == None:
            return flask.redirect(flask.url_for("serverView", server=server), 302)
        with open(file, 'rb') as svr:
            sdict = pickle.load(svr)
        return str(sdict)
    
    
    if flask.request.method == "POST":
        from ast import literal_eval
        data = flask.request.data
        data = data.decode("utf-8")
        #print("DATA:", data)
        data = json.loads(data)
        data = literal_eval(data)
        
        if "connect" in data.keys():
            un = data['username']
            del data['username']
            del data["connect"]
            with open(file, 'rb') as svr:
                sdict = pickle.load(svr)
            with open(file, 'wb') as svr:
                if not un in sdict.keys():
                    sdict["players"][un] = {}
                sdict["players"][un].update(data)
                sdict["players"][un]["last call"] = time.time()
                sdict["players"][un]["online"] = True
                sdict["players"][un]["online"] = None
                pickle.dump(sdict, svr)
            return str(sdict)
        if "disconnect" in data.keys():
            with open(file, 'rb') as svr:
                sdict = pickle.load(svr)
            un = data['username']
            del sdict["players"][un]
            with open(file, "wb") as svr:
                pickle.dump(sdict, svr)
            return str(sdict)
            
        un = data['username']
        del data['username']
        with open(file, 'rb') as svr:
            sdict = pickle.load(svr)
        with open(file, 'wb') as svr:
            sdict["players"][un].update(data)
            sdict["players"][un]["last call"] = time.time()
            sdict["players"][un]["online"] = True
            pickle.dump(sdict, svr)
        
        with open(file, "rb") as svr:
            sdict = pickle.load(svr)
        for player, value in sdict["players"].items():
            if time.time() - value["last call"] > 5:
                sdict["players"][player]["online"] = False
        with open(file, "wb") as svr:
            pickle.dump(sdict, svr)
    
        return str(sdict)

@app.route("/manageservers", methods=['GET','POST'])       
def manageservers(req="POST"):
    if flask.request.method == 'GET':
        req = "GET"
    if flask.session["username"] == "":
        return flask.redirect(flask.url_for('login'))
    checkDatabase()
    servers = []
    with open(accdab, 'rb') as acc:
        accounts = pickle.load(acc)
        for name, value in accounts.items():
            if name == flask.session["username"]:
                if "servers" in value.keys():
                    servers = value["servers"]
    if req == 'GET':
        print("GET")
        return flask.render_template('manage_servers.html', servers=servers)
    
    if req == 'POST':
        print("POST")
        name=flask.request.form['name']
        oldName = name
        password=flask.request.form['password']
        redo = False
        unerr = ""
        pwerr = ""
        checkDatabase()
        with open(accdab, 'rb') as accfile:
            acc = pickle.load(accfile)
        for value in acc.values():
            print(value)
            if "servers" in value.keys():
                for svr in value["servers"]:
                    if svr["name"] == name:
                        name = ""
        if " " in list(name):
            name = ""
        if name == "":
            unerr = "Server name is invalid or already exists"
            redo = True
        if password == "":
            pwerr = "Password is too short"
            redo = True
        if redo:
            print("redo")
            return flask.render_template('manage_servers.html', unerror=unerr, pwerror=pwerr, uname=oldName, servers=servers)
        else:
            print("SERVER:", {"name": name, "password": password})
            if not "servers" in acc[flask.session["username"]]:
                acc[flask.session["username"]]["servers"] = []
            acc[flask.session["username"]]["servers"].append({"name": name, "password": password, "admin": flask.session["username"]})
            with open(accdab, 'wb') as accfile:
                pickle.dump(acc, accfile)
            print("RE MANAGE")
            return manageservers("GET")

"""@app.errorhandler(404)
def fourOhFour(error):
    return flask.render_template('Error_404.html')"""
        
if __name__ == "__main__":
    accdab = os.path.join(os.path.dirname(__file__),'accounts.dab')
    startServer()