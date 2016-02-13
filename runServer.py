import threading
import socketServer
import flaskServer

def run(e1, e2):
    #t1 = threading.Thread(target=flaskServer.startServer)
    #t1.start()
    #socketServer.startServer()
    #flaskServer.startServer(e1, e2, own=True)
    flsk = flaskServer.app.__call__(e1, e2)
    print(flsk)
    return flsk