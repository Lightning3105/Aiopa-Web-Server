import flaskServer

def run(e1, e2):
    #t1 = threading.Thread(target=flaskServer.startServer)
    #t1.start()
    #socketServer.startServer()
    #flaskServer.startServer(e1, e2, own=True)
    import os
    with open(os.path.join(os.path.dirname(__file__), "env.txt"), "w") as env:
        env.write(e1['HTTP_X_CLIENT_IP'])
    flsk = flaskServer.app.__call__(e1, e2)
    return flsk

if __name__ == "__main__":
    flaskServer.startServer(own=True)