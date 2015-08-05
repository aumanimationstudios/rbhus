import SimpleHTTPServer
import SocketServer

PORT = 8089
clientsAllowed = ["127.0.0.1","192.168.1.243"]

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
  pass

class httpHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
      print("IN THE CLIENT THREAD")
      print(self.headers['user-agent'])
      if(self.client_address[0] not in clientsAllowed):
        print("CLIENT : "+ str(self.client_address[0]) +" : NOT ALLOWED")
        return(0)
      print(dir(SimpleHTTPServer.SimpleHTTPRequestHandler))
      SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

Handler = httpHandler

httpd = ThreadedTCPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()