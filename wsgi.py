#!/usr/bin/env python
import os

def page(start_response):
    response_body = '''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
  <title>Welcome to OpenShift</title>

</head>
<body>
<h1>Server Running!</h1>
</body>
</html>'''
    response_body = response_body.encode('utf-8')

    status = '200 OK'
    response_headers = [('Content-Type', 'text/html'), ('Content-Length', str(len(response_body)))]
    start_response(status, response_headers)
    #return [response_body ]


def runServer():
    print("RUNSERVER")
    import socket
    import os
    environ = os.environ
    serversocket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
    
    host = environ["OPENSHIFT_PYTHON_IP"]
    port = environ["OPENSHIFT_PYTHON_PORT"]
    print((host, port))
    serversocket.bind((host, int(9384)))
    testvar = "Started server on ", str(host) + ":" + str(port)
    #testvar = (host, port)
    serversocket.listen(2)
    
    clients = {}
    devID = '1'
    clients[devID],addr = serversocket.accept()      
    print("Got a connection from %s" % str(addr))
    clients[devID].send(str(devID).encode('ascii'))

def appliction(enviro, start_response):
    try:
        page(start_response)
        runServer()
    except Exception as e:
        print("SERVER ERROR: ", e)
    