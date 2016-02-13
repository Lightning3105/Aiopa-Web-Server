#
# IMPORTANT: Put any additional includes below this line.  If placed above this
# line, it's possible required libraries won't be in your searchable path
#
import socketServer
from flaskServer import app as application
print("AFTER APP RUN")
#try:
socketServer.startServer()
#except Exception as e:
    #print("SOCKET ERROR: ", e)

#
# Below for testing only
#