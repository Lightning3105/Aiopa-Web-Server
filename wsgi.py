#!/usr/bin/env python
import os

def application(environ, start_response):
    pr = (environ, start_response)
    global environment
    environment = environ

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
    return [response_body ]

if __name__ == "__main__":
    try:
        import socket
        serversocket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
        
        host = environment["OPENSHIFT_PYTHON_IP"]
        port = environment["OPENSHIFT_PYTHON_PORT"]
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
    except Exception as e:
        print("SERVER ERROR: ", e)
    