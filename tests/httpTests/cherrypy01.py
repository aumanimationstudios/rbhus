import cherrypy
import  time
import  random
import  multiprocessing



class Root1(object):

  def __init__(self):
    self.m = 0

  @cherrypy.expose
  def index(self):
    return "THIS IS ROOT1"

  @cherrypy.expose
  def testing(self):
    # return  "testubg"
    # self.m = self.m + 1
    # s = multiprocessing.Process(target=self.multishit,args=(self.m,))
    # s.start()
    time.sleep(random.randint(10,20))
    return "testing from root1"

  def multishit(self,num):

    time.sleep(random.randint(10,20))
    return "testing multiprocessing : "+ str(num)


class Root2(object):
  @cherrypy.expose
  def index(self):
    return "THIS IS ROOT2"

  @cherrypy.expose
  def testing(self):
    return "THIS IS TESTING FROM ROOT2"


if __name__ == '__main__':
  cherrypy.tree.mount(Root1(),'/',"/home/shrinidhi/bin/gitHub/rbhus/tests/httpTests/cherry.conf")
  cherrypy.tree.mount(Root2(),'/root2')

  cherrypy.engine.start()
  cherrypy.engine.block()