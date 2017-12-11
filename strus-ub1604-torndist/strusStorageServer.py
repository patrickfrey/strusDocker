#!/usr/bin/python3
import tornado.ioloop
import tornado.web
import tornado.gen
import tornado.iostream
import os
import sys
import struct
import collections
import optparse
import strusMessage
import binascii
import strusIR

# Information retrieval engine:
backend = None
# Port of the global statistics server:
statserver = "localhost:7183"
# IO loop:
pubstats = False
# Strus client connection factory:
msgclient = strusMessage.RequestClient()

# Call of the statustics server to publish the statistics of this storage on insert:
@tornado.gen.coroutine
def publishStatistics( itr):
    # Open connection to statistics server:
    try:
        ri = statserver.rindex(':')
        host,port = statserver[:ri],int( statserver[ri+1:])
        conn = yield msgclient.connect( host, port)
    except IOError as e:
        raise Exception( "connection to statistics server %s failed (%s)" % (statserver, e))

    for msg in itr:
        try:
            reply = yield msgclient.issueRequest( conn, b"P" + msg)
            if (reply[0] == ord('E')):
                raise Exception( "error in statistics server: %s" % reply[ 1:].decode('utf-8'))
            elif (reply[0] != ord('Y')):
                raise Exception( "protocol error publishing statistics")
        except tornado.iostream.StreamClosedError:
            raise Exception( "unexpected close of statistics server")

# Pack a message with its length (processCommand protocol)
def packedMessage( msg):
    return struct.pack( ">H%ds" % len(msg), len(msg), msg.encode('utf-8'))

# Server callback function that intepretes the client message sent,
# executes the command and packs the result for the client
@tornado.gen.coroutine
def processCommand( message):
    rt = b"Y"
    try:
        messagesize = len(message)
        messageofs = 1
        if (message[0] == ord('I')):
            # INSERT:
            # Insert documents:
            docblob = message[ 1:]
            nofDocuments = backend.insertDocuments( docblob)
            # Publish statistic updates:
            if (pubstats):
                itr = backend.getUpdateStatisticsIterator()
                yield publishStatistics( itr)
            rt += struct.pack( ">I", nofDocuments)
        elif (message[0] == ord('Q')):
            # QUERY:
            Term = collections.namedtuple('Term', ['type', 'value', 'df'])
            nofranks = 20
            collectionsize = 0
            firstrank = 0
            terms = []
            # Build query to evaluate from the request:
            messagesize = len(message)
            messageofs = 1
            while (messageofs < messagesize):
                if (message[ messageofs] == ord('I')):
                    (firstrank,) = struct.unpack_from( ">H", message, messageofs+1)
                    messageofs += struct.calcsize( ">H") + 1
                elif (message[ messageofs] == ord('N')):
                    (nofranks,) = struct.unpack_from( ">H", message, messageofs+1)
                    messageofs += struct.calcsize( ">H") + 1
                elif (message[ messageofs] == ord('S')):
                    (collectionsize,) = struct.unpack_from( ">q", message, messageofs+1)
                    messageofs += struct.calcsize( ">q") + 1
                elif (message[ messageofs] == ord('T')):
                    (df,typesize,valuesize) = struct.unpack_from( ">qHH", message, messageofs+1)
                    messageofs += struct.calcsize( ">qHH") + 1
                    (type,value) = struct.unpack_from( "%ds%ds" % (typesize,valuesize), message, messageofs)
                    messageofs += typesize + valuesize
                    terms.append( Term( type, value, df))
                else:
                    raise tornado.gen.Return( b"Eunknown parameter")
            # Evaluate query with BM25 (Okapi):
            results = backend.evaluateQuery( terms, collectionsize, firstrank, nofranks)
            # Build the result and pack it into the reply message for the client:
            for result in results:
                rt += b'_D'
                rt += struct.pack( ">I", result['docno'])
                rt += b'W'
                rt += struct.pack( ">f", result['weight'])
                rt += b'I'
                rt += packedMessage( result['docid'])
                rt += b'T'
                rt += packedMessage( result['title'])
                rt += b'A'
                rt += packedMessage( result['abstract'])
        else:
            raise Exception( "unknown command")
    except Exception as e:
        raise tornado.gen.Return( b"E" + str(e).encode('utf-8'))
    raise tornado.gen.Return( rt)

# Shutdown function that sends the negative statistics to the statistics server (unsubscribe):
def processShutdown():
    if (pubstats):
        publishStatistics( backend.getDoneStatisticsIterator())

# Server main:
if __name__ == "__main__":
    try:
        # Parse arguments:
        defaultconfig = "path=storage; cache=512M; statsproc=default"
        parser = optparse.OptionParser()
        parser.add_option("-p", "--port", dest="port", default=7184,
                          help="Specify the port of this server as PORT (default %u)" % 7184,
                          metavar="PORT")
        parser.add_option("-c", "--config", dest="config", default=defaultconfig,
                          help="Specify the storage path as CONF (default '%s')" % defaultconfig,
                          metavar="CONF")
        parser.add_option("-s", "--statserver", dest="statserver", default=statserver,
                          help="Specify the address of the statistics server as ADDR (default %s" % statserver,
                          metavar="ADDR")
        parser.add_option("-P", "--publish-stats", action="store_true", dest="do_publish_stats", default=False,
                          help="Tell the node to publish the own storage statistics "
                               "to the statistics server at startup")

        (options, args) = parser.parse_args()
        if len(args) > 0:
            parser.error("no arguments expected")
            parser.print_help()

        myport = int(options.port)
        pubstats = options.do_publish_stats
        statserver = options.statserver
        backend = strusIR.Backend( options.config)

        if (statserver[0:].isdigit()):
            statserver = '{}:{}'.format( 'localhost', statserver)

        if (pubstats):
            # Start publish local statistics:
            print( "Load local statistics to publish ...\n")
            publishStatistics( backend.getInitStatisticsIterator())

        # Start server:
        print( "Starting server ...")
        server = strusMessage.RequestServer( processCommand, processShutdown)
        server.start( myport)
        print( "Terminated\n")
    except Exception as e:
        print( e)


