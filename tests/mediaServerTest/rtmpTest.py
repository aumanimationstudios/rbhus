import sys

from twisted.internet import reactor
from twisted.python import log

from rtmpy import server

app = server.Application()

reactor.listenTCP(1935, server.ServerFactory({
    'live': app
}))

log.startLogging(sys.stdout)

reactor.run()
