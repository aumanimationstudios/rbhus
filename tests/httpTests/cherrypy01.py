import cherrypy



class Root1(object):
  @cherrypy.expose
  def index(self):
    return "THIS IS ROOT1"

  @cherrypy.expose
  def testing(self):
    return "THIS IS TESTING FROM ROOT1"


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