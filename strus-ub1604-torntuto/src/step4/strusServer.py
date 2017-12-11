#!/usr/bin/python3
import tornado.ioloop
import tornado.web
import os
import sys

# [1] Request handlers:
class InsertHandler(tornado.web.RequestHandler):
    def post(self):
        pass;
        #... insert handler implementation

class QueryHandler(tornado.web.RequestHandler):
    def get(self):
        pass;
        #... query handler implementation

# [2] Dispatcher:
application = tornado.web.Application([
    # /insert in the URL triggers the handler for inserting documents:
    (r"/insert", InsertHandler),
    # /query in the URL triggers the handler for answering queries:
    (r"/query", QueryHandler),
    # /static in the URL triggers the handler for accessing static 
    # files like images referenced in tornado templates:
    (r"/static/(.*)",tornado.web.StaticFileHandler,
        {"path": os.path.dirname(os.path.realpath(sys.argv[0]))},)
])

# [3] Server main:
if __name__ == "__main__":
    try:
        print( "Starting server ...\n");
        application.listen(80)
        print( "Listening on port 80\n");
        tornado.ioloop.IOLoop.current().start()
        print( "Terminated\n");
    except Exception as e:
        print( e);
