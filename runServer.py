import flaskServer

def run(e1, e2):
    #t1 = threading.Thread(target=flaskServer.startServer)
    #t1.start()
    #socketServer.startServer()
    #flaskServer.startServer(e1, e2, own=True)
    with open("environ", "w") as env:
        env.write(e1)
    flsk = flaskServer.app.__call__(e1, e2)
    print(flsk)
    return flsk

if __name__ == "__main__":
    flaskServer.startServer(own=True)