import SimpleHTTPServer
import SocketServer
import re

PORT = 80
clientsAllowed = {}

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
  pass

class httpHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
  def __init__(self, *args):
    # print("----------------------#################")
    # f = open("d:/gitHub/rbhus/tests/mediaServerTest/get","w")
    # f.write(args[0].recv(4096))
    # f.flush()
    # f.close()
    # print("----------------------#################")
    SimpleHTTPServer.SimpleHTTPRequestHandler.__init__(self,*args)

  def do_GET(self):
    print(str(self.client_address[0]) +" : IN THE CLIENT THREAD")
    print("----------------------")
    print(str(self.client_address[0]) +" : CLIENT CONNECTING")
    print("----------------------")
    print(str(self.client_address[0]) +" : "+ self.headers['user-agent'])
    print("----------------------")
    print(str(self.client_address[0]) +" : "+ self.path)
    print("----------------------")
    if(re.search('[v,V][l,L][c,C]',self.headers['user-agent'])):
      print(str(self.client_address[0]) +" : FOUND VLC REQUEST")
      print("----------------------")
      if(self.client_address[0] not in clientsAllowed.keys()):
        print(str(self.client_address[0]) +" : CLIENT NOT ALLOWED")
        return(0)
    else:
      if(re.search('^/REGISTER',self.path)):
        print(str(self.client_address[0]) +" : TRYING TO REGISTER")
        print("----------------------")
        clientsAllowed[str(self.client_address[0])] = 1
        print(str(self.client_address[0]) +" : REGISTERING DONE")
        return(1)
      else:
        if(self.client_address[0] not in clientsAllowed.keys()):
          print(str(self.client_address[0]) +" : CLIENT NOT REGISTERED")
          print("----------------------")
          return(0)
    print(str(self.client_address[0]) +" : CLIENT CONNECTED")
    print("----------------------")
    # print(dir(SimpleHTTPServer.SimpleHTTPRequestHandler))
    SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

  def do_REGISTER(self):
    print("IN BIG METHOD")

Handler = httpHandler

httpd = ThreadedTCPServer(("", PORT), Handler)

print "serving at port", PORT
print("server timeouts : "+ str(httpd.timeout))
httpd.serve_forever()