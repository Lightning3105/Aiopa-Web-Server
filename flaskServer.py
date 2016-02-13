from flask import Flask
import flask

app = Flask(__name__)

def startServer(own=False):
    if own:
        app.debug = True
    if __name__ == 'flaskServer':
        app.run(threaded=True)

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
        if username == "":
            unerr = "Username is invalid or alread exists"
            redo = True
        if password == "":
            pwerr = "Password is too short"
            redo = True
        if redo:
            print("REDO")
            return flask.render_template('form_submit.html', unerror=unerr, pwerror=pwerr, uname=username)
        else:
            print("REDIRECT")
            return flask.redirect(flask.url_for('accountcreated'), code=307)

@app.route('/')
def root():
    return flask.redirect(flask.url_for('createaccount'), code=302)

# Define a route for the action of the form, for example '/hello/'
# We are also defining which type of requests this route is 
# accepting: POST requests in this case
@app.route('/accountcreated/', methods=['POST'])
def accountcreated():
    print("ACCOUNT CREATED")
    username=flask.request.form['username']
    password=flask.request.form['password']
    return flask.render_template('form_action.html', username=username, password=password)