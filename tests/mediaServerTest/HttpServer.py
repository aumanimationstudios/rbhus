import SimpleHTTPServer
import SocketServer

PORT = 8089

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
  pass

class httpHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
      if()

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = ThreadedTCPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()