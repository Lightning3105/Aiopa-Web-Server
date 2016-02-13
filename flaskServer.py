from flask import Flask
import flask
import pickle
import os

app = Flask(__name__)
accdab = os.path.join(os.path.dirname(__file__),'accounts.dab')

def startServer(e1, e2, own=False):
    if own:
        app.debug = True
    #if __name__ == 'flaskServer':
    app.run(threaded=True, host=os.environ["OPENSHIFT_PYTHON_IP"])

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
    f = open(os.path.join(os.path.dirname(__file__),'accounts.dab'), 'rb')
    print("POST CHECK DATABASE")
    #except IOError:
        #f = open('accounts.dab', 'wb')
        #pickle.dump({}, f)
        #f.close()



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