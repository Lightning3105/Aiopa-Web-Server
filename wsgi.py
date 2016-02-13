#
# IMPORTANT: Put any additional includes below this line.  If placed above this
# line, it's possible required libraries won't be in your searchable path
#
import socketServer
import threading
from flaskServer import app as application
print("AFTER APP RUN")

t1 = threading.Thread(target=socketServer.startServer)
t1.start()

#
# Below for testing only
#