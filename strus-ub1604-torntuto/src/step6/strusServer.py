#!/usr/bin/python3
import tornado.ioloop
import tornado.web
import os
import sys
import strusIR

# Declare the information retrieval engine:
backend = strusIR.Backend( "path=storage; cache=512M")

# [1] Request handlers:
# Declare the insert document handler (POST request with the multipart document as body):
class InsertHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            content = self.request.body
            nofDocuments = backend.insertDocuments( content)
            self.write( "OK %u\n" % (nofDocuments))
        except Exception as e:
            self.write( "ERR %s\n" % (e))

# Declare the query request handler:
class QueryHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            # q = query terms:
            querystr = self.get_argument( "q", None)
            # i = first rank of the result to display (for scrolling):
            firstrank = int( self.get_argument( "i", 0))
            # n = maximum number of ranks of the result to display on one page:
            nofranks = int( self.get_argument( "n", 20))
            # c = query evaluation scheme to use:
            scheme = self.get_argument( "s", "BM25")
            if scheme == "BM25":
                # The evaluation scheme is a classical BM25 (Okapi):
                results = backend.evaluateQueryText( querystr, firstrank, nofranks)
                self.render( "search_bm25_html.tpl",
                             scheme=scheme, querystr=querystr,
                             firstrank=firstrank, nofranks=nofranks, results=results)
            elif scheme == "NBLNK":
                # The evaluation scheme is weighting the entities in the matching documents:
                results = backend.evaluateQueryEntities( querystr, firstrank, nofranks)
                self.render( "search_nblnk_html.tpl",
                             scheme=scheme, querystr=querystr,
                             firstrank=firstrank, nofranks=nofranks, results=results)
            else:
                raise Exception( "unknown query evaluation scheme", scheme)
        except Exception as e:
            self.render( "search_error_html.tpl", 
                         message=e, scheme=scheme, querystr=querystr,
                         firstrank=firstrank, nofranks=nofranks)

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


