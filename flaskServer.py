from flask import Flask
import flask

app = Flask(__name__)

def startServer(own=False):
    if own:
        app.debug = True
    if __name__ == '__main__':
        app.run(threaded=True)

@app.route('/')
def form():
    return flask.render_template('form_submit.html')

# Define a route for the action of the form, for example '/hello/'
# We are also defining which type of requests this route is 
# accepting: POST requests in this case
@app.route('/accountcreated/', methods=['POST'])
def accountcreated():
    username=flask.request.form['username']
    password=flask.request.form['password']
    if username == "":
        return flask.render_template('form_submit.html', unerror="Username is invalid or alread exists")
    return flask.render_template('form_action.html', username=username, password=password)