#import os
#import sys


#sys.path.insert(0, os.path.dirname(__file__))


#def application(environ, start_response):
#    start_response('200 OK', [('Content-Type', 'text/plain')])
#    message = 'Coming soon\nalnkib.com\n'
#    response = '\n'.join([message])
#    return [response.encode()]

from Safe_Driving_Web_Server.wsgi import application
