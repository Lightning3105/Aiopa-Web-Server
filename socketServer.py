import socket

def startServer():
    serversocket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM) 
    
    # get local machine name
    host = socket.gethostname()     
    #host = "80.42.171.141"          
    #host = "192.168.1.1"         
    
    port = 31055                                           
    # bind to the port
    serversocket.bind((host, port))                                  
    print("Started server on ", str(host) + ":" + str(port))
    # queue up to 5 requests
    serversocket.listen(1)
    
    clients = {}
    devID = "1"
    # establish a connection
    clients[devID],addr = serversocket.accept()      
    print("Got a connection from %s" % str(addr))
    clients[devID].send(str(devID).encode('ascii'))