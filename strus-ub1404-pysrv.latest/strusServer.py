#!/usr/bin/python

import tornado.ioloop
import tornado.web
import time
import strusIR

backend = strusIR.Backend( "path=storage; cache=512M")

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("Hello, world")

class QueryHandler(tornado.web.RequestHandler):
	def get(self):
		try:
			querystr = self.get_argument("q", None)
			firstrank = self.get_argument("i", 0)
			nofranks = self.get_argument("n", 20)
			scheme = self.get_argument("s", "BM25")
			starttime = time.clock()
			results = backend.evaluateQuery( querystr, firstrank, nofranks)
			endtime = time.clock()
			self.render("search.html", scheme=scheme, querystr=querystr, firstrank=firstrank, nofranks=nofranks, results=results, exectime=(endtime-starttime))
		except Exception as e:
			self.render("search_error.html", message=e, scheme=scheme, querystr=querystr, firstrank=firstrank, nofranks=nofranks)

application = tornado.web.Application([
	(r"/", MainHandler),
	(r"/query", QueryHandler),
	(r"/static/(.*)",tornado.web.StaticFileHandler, {"path": "./"},)
])


if __name__ == "__main__":
	application.listen(80)
	tornado.ioloop.IOLoop.current().start()


