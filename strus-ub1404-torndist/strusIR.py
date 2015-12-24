import strus
import itertools
import heapq
import re

class Backend:
    # Create the document analyzer for our test collection:
    # Create the document analyzer for our test collection:
    def createDocumentAnalyzer(self):
        rt = self.context.createDocumentAnalyzer()
        # Define the sections that define a document (for multipart documents):
        rt.defineDocument( "doc", "/list/item")

        # Define the terms to search for (inverted index or search index):
        rt.addSearchIndexFeature( "word", "/list/item/title()",
                                  "word", ("lc",("stem","en"),("convdia","en")))
        rt.addSearchIndexFeature( "word", "/list/item/artist()",
                                  "word", ("lc",("stem","en"),("convdia","en")))
        rt.addSearchIndexFeature( "word", "/list/item/note()",
                                  "word", ("lc",("stem","en"),("convdia","en")))

        # Define the terms to search for (inverted index or search index):
        rt.addForwardIndexFeature( "orig", "/list/item/title()", "split", "orig")
        rt.addForwardIndexFeature( "orig", "/list/item/artist()", "split", "orig")
        rt.addForwardIndexFeature( "orig", "/list/item/note()", "split", "orig")

        # Define the document attributes:
        rt.defineAttribute( "docid", "/list/item/id()", "content", "text")
        rt.defineAttribute( "title", "/list/item/title()", "content", "text")
        rt.defineAttribute( "upc", "/list/item/upc()", "content", "text")
        rt.defineAttribute( "note", "/list/item/note()", "content", "text")

        # Define the document meta data:
        rt.defineMetaData( "date", "/list/item/date()", "content", [("date2int", "d 1877-01-01", "%Y-%m-%d %H:%M:%s *")]);

        # Define the doclen attribute needed by BM25:
        rt.defineAggregatedMetaData( "doclen",("count", "word"))
        return rt

    # Create the query analyzer according to the document analyzer configuration:
    def createQueryAnalyzer(self):
        rt = self.context.createQueryAnalyzer()
        rt.definePhraseType(
            "text", "word", "word", 
            ["lc", ["stem", "en"], ["convdia", "en"]]
        )
        return rt

    # Create a simple BM25 query evaluation scheme with fixed
    # a,b,k1 and avg document lenght and title with abstract
    # as summarization attributes:
    def createQueryEvalBM25(self):
        rt = self.context.createQueryEval()
        # Declare the sentence marker feature needed for abstracting:
        rt.addTerm( "sentence", "sent", "")
        # Declare the feature used for selecting result candidates:
        rt.addSelectionFeature( "selfeat")
        # Query evaluation scheme:
        rt.addWeightingFunction( 1.0, "BM25", {
                     "k1": 0.75, "b": 2.1, "avgdoclen": 20, ".match": "docfeat" })
        # Summarizer for getting the document title:
        rt.addSummarizer( "DOCID", "attribute", { "name": "docid" })
        rt.addSummarizer( "TITLE", "attribute", { "name": "title" })
        # Summarizer for abstracting:
        rt.addSummarizer( "CONTENT", "matchphrase", {
                  "type": "orig", "len": 40, "nof": 3,
                  "mark": '<b>$</b>', ".match": "docfeat" })
        return rt

    # Constructor. Initializes the query evaluation schemes and the query and document analyzers:
    def __init__(self, config):
        # Open local storage on file with configuration specified:
        self.context = strus.Context()
        self.context.defineStatisticsProcessor( "standard");
        self.storage = self.context.createStorageClient( config )
        self.queryAnalyzer = self.createQueryAnalyzer()
        self.documentAnalyzer = self.createDocumentAnalyzer()
        self.queryeval = self.createQueryEvalBM25()

    # Insert a multipart document:
    def insertDocuments( self, content):
        rt = 0
        docqueue = self.documentAnalyzer.createQueue()
        docqueue.push( content)
        transaction = self.storage.createTransaction()
        while (docqueue.hasMore()):
            doc = docqueue.fetch()
            transaction.insertDocument( doc.docid(), doc)
            rt += 1
        transaction.commit()
        return rt

    # Query evaluation scheme for a classical information retrieval query with BM25:
    def evaluateQuery( self, terms, collectionsize, firstrank, nofranks):
        queryeval = self.queryeval
        query = queryeval.createQuery( self.storage)
        if len( terms) == 0:
            # Return empty result for empty query:
            return []

        selexpr = ["contains"]
        for term in terms:
            selexpr.append( [term.type, term.value] )
            query.defineFeature( "docfeat", [term.type, term.value], 1.0)
            query.defineTermStatistics( term.type, term.value, {'df' : int(term.df)} )
        query.defineFeature( "selfeat", selexpr, 1.0 )
        query.setMaxNofRanks( nofranks)
        query.setMinRank( firstrank)
        query.defineGlobalStatistics( {'nofdocs' : int(collectionsize)} )
        # Evaluate the query:
        results = query.evaluate()
        # Rewrite the results:
        rt = []
        for result in results:
            content = ""
            title = ""
            docid = ""
            for attribute in result.attributes():
                if attribute.name() == 'CONTENT':
                    if content != "":
                        content += ' ... '
                    content += attribute.value()
                elif attribute.name() == 'DOCID':
                        docid = attribute.value()
                elif attribute.name() == 'TITLE':
                        title = attribute.value()
            rt.append( {
                   'docno':result.docno(),
                   'docid':docid,
                   'title':title,
                   'weight':result.weight(),
                   'abstract':content })
        return rt

    # Get an iterator on all absolute statistics of the local storage
    def getInitStatisticsIterator( self):
        return self.storage.createInitStatisticsIterator( True)

    # Get an iterator on all absolute statistics of the local storage
    def getDoneStatisticsIterator( self):
        return self.storage.createInitPeerMessageIterator( False)
    
    # Get an iterator on updates to be sent to peers
    def getUpdateStatisticsIterator( self):
        return self.storage.createUpdateStatisticsIterator()


