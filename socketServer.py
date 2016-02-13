import socket
import os

def startServer():
    try:
        serversocket = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
        
        # get local machine name
        host = os.environ["OPENSHIFT_PYTHON_IP"]
        #host = "80.42.171.141"
        #host = "192.168.1.1"
        
        port = 31055
        # bind to the port
        serversocket.bind((host, port))
        print("Started server on ", str(host) + ":" + str(port))
        # queue up to 5 requests
        serversocket.listen(1)
        
        while True:
            #wait to accept a connection - blocking call
            conn, addr = serversocket.accept()
            print ('Connected with ' + addr[0] + ':' + str(addr[1]))
    except OSError as e:
        print("PORT ALLREAD OPEN", e)