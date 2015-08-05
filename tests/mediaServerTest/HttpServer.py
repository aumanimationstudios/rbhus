#!/usr/bin/env python

# This code is written by Stephen C Phillips.
# It is in the public domain, so you can do what you like with it
# but a link to http://scphillips.com would be nice.

import socket
import re

# Standard socket stuff:
host = '' # do we need socket.gethostname() ?
port = 80
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen(1) # don't queue up any requests

# Loop forever, listening for requests:
while True:
    csock, caddr = sock.accept()
    print "Connection from: " + `caddr`
    req = csock.recv(1024) # get the request, 1kB max
    print req
    # Look in the first line of the request for a move command
    # A move command should be e.g. 'http://server/move?a=90'
    match = re.match('GET /move\?a=(\d+)\sHTTP/1', req)
    if match:
        angle = match.group(1)
        print "ANGLE: " + angle + "\n"
        csock.sendall("""HTTP/1.0 200 OK
Content-Type: text/html

<html>
<head>
<title>Success</title>
</head>
<body>
Damn . its a Success!
</body>
</html>
""")
    else:
        # If there was no recognised command then return a 404 (page not found)
        print "Returning 404"
        csock.sendall("""HTTP/1.0 404 NOTFOUND
Content-Type: text/html

<html>
<head>
<title>Success</title>
</head>
<body>
Failed!
</body>
</html>
""")
    csock.close()