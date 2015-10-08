from twisted.web.server import Site
from twisted.web.static import File
from twisted.internet import reactor
from twisted.web.resource import Resource
import re
import inspect

clientsAllowed = {}

class Registered(Resource):
  isLeaf = True
  def render_GET(self, request):
    return "<html>REGISTERED!</html>"

class NotRegistered(Resource):
  isLeaf = True
  def render_GET(self, request):
    return "<html>NOT REGISTERED!</html>"


class myfile(File):
  def __init__(self,*args):

    # try:
    print("in myfile : "+ str(args))
    # except:
    #   pass
    File.__init__(self,*args)


  def getChild(self, name, request):
    print("in getChild : "+ str(name) +":"+ str(request))
    # print(dir(request))
    print(request.URLPath())
    print(request.getClientIP())
    if(request.getClientIP() in clientsAllowed.keys()):
      test = File.getChild(self,name,request)
      print(test)
      return(test)
    elif(re.search('^/REGISTER',request.uri)):
      clientsAllowed[request.getClientIP()] = 1
      return(Registered())
    else:
      return(NotRegistered())


    
  


  def render_GET(self,request):
    # 
    print("----------------------")
    print(request.getClientIP() +" : HEADERS")
    print("----------------------")
    print(request.getAllHeaders())
    # for x in request.headers.keys():
    #   print(x +" : "+ request.headers[x])
    print("----------------------")
    return File.render_GET(self,request)

# resource = File('./')

res = myfile("./")   
# print(dir(res))
factory = Site(res)
reactor.listenTCP(80, factory)
reactor.run()