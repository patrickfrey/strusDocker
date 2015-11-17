#!/usr/bin/python

import tornado.ioloop
import tornado.web
import os
import sys
import time
import strusIR

# Declare the information retrieval engine
backend = strusIR.Backend( "path=storage; cache=512M")

# Declare the root request handler:
class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("Welcome to tornado with strus")

# Declare the information retrieval query request handler:
class QueryHandler(tornado.web.RequestHandler):
	def get(self):
		try:
			# q = query terms:
			querystr = self.get_argument("q", None)
			# i = first rank of the result to display (for scrolling):
			firstrank = int( self.get_argument("i", 0))
			# n = maximum number of ranks of the result to display on one page:
			nofranks = int( self.get_argument("n", 20))
			# c = query evaluation scheme to use:
			scheme = self.get_argument("s", "BM25")
			if scheme == "BM25":
				# The evaluation scheme is a classical BM25 (Okapi):
				results = backend.evaluateQueryText( querystr, firstrank, nofranks)
				self.render("search_html.tpl", scheme=scheme, querystr=querystr, firstrank=firstrank, nofranks=nofranks, results=results)
			elif scheme == "NBLNK":
				# The evaluation scheme is weighting the links of matching sentences:
				results = backend.evaluateQueryLinks( querystr, firstrank, nofranks, "CONTINENT")
				self.render("searchlink_html.tpl", scheme=scheme, querystr=querystr, firstrank=firstrank, nofranks=nofranks, results=results)
			else:
				raise Exception( "unknown query evaluation scheme", scheme)
		except Exception as e:
			self.render("search_error_html.tpl", message=e, scheme=scheme, querystr=querystr, firstrank=firstrank, nofranks=nofranks)


application = tornado.web.Application([
	(r"/", MainHandler),
	(r"/query", QueryHandler),
	(r"/static/(.*)",tornado.web.StaticFileHandler, {"path": os.path.dirname(os.path.realpath(sys.argv[0]))},)
])


if __name__ == "__main__":
	try:
		print( "Starting server ...\n");
		application.listen(80)
		print( "Listening on port 80\n");
		tornado.ioloop.IOLoop.current().start()
		print( "Terminated\n");
	except Exception as e:
		print( e);



