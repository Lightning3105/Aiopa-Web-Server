import threading
import socketServer
import flaskServer

def run(*args, **kwargs):
    print("ARGS", args)
    print("KWARGS", kwargs)
    #t1 = threading.Thread(target=flaskServer.startServer)
    #t1.start()
    #socketServer.startServer()
    flaskServer.startServer(own=True)