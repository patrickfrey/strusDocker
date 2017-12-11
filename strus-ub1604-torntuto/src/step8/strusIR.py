import strus
import itertools
import heapq
import re

class Backend:
    # Create the document analyzer for our test collection:
    def createDocumentAnalyzer(self):
        rt = self.context.createDocumentAnalyzer( {'mimetype':"application/xml", 'encoding':"UTF-8"} )
        # Define the sections that define a document (for multipart documents):
        rt.defineDocument( "doc", "/list/doc")
        # Define the terms to search for (inverted index or search index):
        rt.addSearchIndexFeature( "word", "/list/doc//()",
                                  "word", ("lc",("stem","en"),("convdia","en")))
        # Define the end of sentence markers:
        rt.addSearchIndexFeature( "sent", "/list/doc//()",
                                  ("punctuation","en","."), "empty")
        # Define the placeholders that are referencable by variables:
        rt.addSearchIndexFeature( "continent_var", "/list/doc/continent@id",
                                  "content", "empty", "succ")
        # Define the original terms in the document used for abstraction:
        rt.addForwardIndexFeature( "orig", "/list/doc//()", "split", "orig")
        # Define the contents that extracted by variables:
        rt.addForwardIndexFeature( "continent", "/list/doc/continent@id",
                                   "content", "text", "succ")
        # Define the document identifier:
        rt.defineAttribute( "docid", "/list/doc@id", "content", "text")
        # Define the doclen attribute needed by BM25:
        rt.defineAggregatedMetaData( "doclen",("count", "word"))
        return rt

    # Create the query analyzer according to the document analyzer configuration:
    def createQueryAnalyzer(self):
        rt = self.context.createQueryAnalyzer()
        rt.addElement(
            "word", "text", "word", 
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
        rt.addWeightingFunction( "BM25", {
                     "k1": 1.2, "b": 0.75, "avgdoclen": 20, "match": {'feature':"docfeat"} })
        # Summarizer for getting the document title:
        rt.addSummarizer( "attribute", { "name": "docid" }, {"result":"TITLE"})
        # Summarizer for abstracting:
        rt.addSummarizer( "matchphrase", {
                  "type": "orig", "windowsize": 40, "sentencesize":30,
                  "matchmark": '$<b>$</b>', "struct":{'feature':"sentence"}, "match": {'feature':"docfeat"} },
                  {"phrase":"CONTENT"})
        return rt

    # Create a simple BM25 query evaluation scheme with fixed
    # a,b,k1 and avg document lenght and the weighted extracted
    # entities in the same sentence as matches as query evaluation result:
    def createQueryEvalNBLNK(self):
        rt = self.context.createQueryEval()
        # Declare the sentence marker feature needed for the
        # summarization features extracting the entities:
        rt.addTerm( "sentence", "sent", "")
        # Declare the feature used for selecting result candidates:
        rt.addSelectionFeature( "selfeat")
        # Query evaluation scheme for entity extraction candidate selection:
        rt.addWeightingFunction( "BM25", {"k1": 1.2, "b": 0.75, "avgdoclen": 20, "match": {'feature':"docfeat"} })
        # Summarizer to extract the weighted entities:
        rt.addSummarizer( "accuvar", { "match": {'feature':"sumfeat"}, "var": "CONTINENT", "type": "continent", "result":"ENTITY" } )
        return rt

    # Constructor. Initializes the query evaluation schemes and the query and document analyzers:
    def __init__(self, config):
        if isinstance( config, ( int ) ):
            self.context = strus.Context( "localhost:%u" % config)
            self.storage = self.context.createStorageClient()
        else:
            self.context = strus.Context()
            self.context.addResourcePath("./resources")
            self.storage = self.context.createStorageClient( config )
        self.queryAnalyzer = self.createQueryAnalyzer()
        self.documentAnalyzer = self.createDocumentAnalyzer()
        self.queryeval = {}
        self.queryeval["BM25"] = self.createQueryEvalBM25()
        self.queryeval["NBLNK"] = self.createQueryEvalNBLNK()

    # Insert a multipart document:
    def insertDocuments( self, content):
        rt = 0
        transaction = self.storage.createTransaction()
        for doc in self.documentAnalyzer.analyzeMultiPart( content):
            docid = doc['attribute']['docid']
            transaction.insertDocument( docid, doc)
            rt += 1
        transaction.commit()
        return rt

    # Query evaluation scheme for a classical information retrieval query with BM25:
    def evaluateQueryText( self, querystr, firstrank, nofranks):
        queryeval = self.queryeval[ "BM25"]
        query = queryeval.createQuery( self.storage)
        terms = self.queryAnalyzer.analyzeTermExpression( [ "text", querystr ] )
        if len( terms) == 0:
            # Return empty result for empty query:
            return []

        selexpr = ["contains", 0, 1]
        for term in terms:
            selexpr.append( term )
            query.addFeature( "docfeat", term, 1.0)
        query.addFeature( "selfeat", selexpr, 1.0 )
        query.setMaxNofRanks( nofranks)
        query.setMinRank( firstrank)
        # Evaluate the query:
        results = query.evaluate()
        # Rewrite the results:
        rt = []
        for pos,result in enumerate(results['ranks']):
            content = ""
            title = ""
            for summary in result['summary']:
                if summary['name'] == 'TITLE':
                    title = summary['value']
                elif summary['name'] == 'CONTENT':
                    content = summary['value']
            rt.append( { 'docno':result['docno'], 'title':title, 'weight':result['weight'], 'abstract':content })
        return rt

    # Helper method to define the query features created from terms 
    # of the query string, that are following subsequently in the query:
    def __defineSubsequentQueryTermFeatures( self, query, term1, term2):
        # Pairs of terms appearing subsequently in the query are 
        # translated into 3 query expressions:
        #    1+2) search for sequence inside a sentence in documents,
        #        The summarizer extracts entities within 
        #        a distance of 50 in the same sentence
        #    3) search for the terms in a distance smaller than 5 inside a sentence,
        #        The summarizer extracts entities within a distance
        #        of 50 in the same sentence
        #    4) search for the terms in a distance smaller than 20 inside 
        #        The summarizer extracts entities within
        #        a distance of 50 in the same sentence
        expr = [
                [ "sequence_struct", 3, ["sent",''], term1, term2 ],
                [ "sequence_struct", 3, ["sent",''], term2, term1 ],
                [ "within_struct", 5, ["sent",''], term1, term2 ],
                [ "within_struct", 20, term1, term2 ]
        ]
        weight = [ 3.0, 2.0, 2.0, 1.5 ]
        ii = 0
        while ii < 4:
            # The summarization expression attaches a variable referencing an
            # the entity to extract.
            # CONTINENT terms of type 'continent_var':
            sumexpr = [ "chain_struct", 50, ["sent",''],
                          [{'variable':"CONTINENT"}, "continent_var", ""],
                          expr[ ii] ]
            query.addFeature( "sumfeat", sumexpr, weight[ ii] )
            sumexpr = [ "sequence_struct", -50, ["sent",''],
                          expr[ ii],
                          [{'variable':"CONTINENT"}, "continent_var", ""],
                      ]
            query.addFeature( "sumfeat", sumexpr, weight[ ii] )
            ii += 1

    # Helper method to define the query features created from terms 
    # of the query string, that are not following subsequently in the query:
    def __defineNonSubsequentQueryTermFeatures( self, query, term1, term2):
        # Pairs of terms not appearing subsequently in the query are 
        # translated into two query expressions:
        #    1) search for the terms in a distance smaller than 5 inside
        #        a sentence, weight 1.6,
        #        where d ist the distance of the terms in the query.
        #        The summarizer extracts entities within a distance
        #        of 50 in the same sentence
        #    2) search for the terms in a distance smaller than 20 inside
        #        a sentence, weight 1.2,
        #        where d ist the distance of the terms in the query.
        #        The summarizer extracts entities within a distance
        #        of 50 in the same sentence
        expr = [
                [ "within_struct", 5, ["sent",''], term1, term2 ],
                [ "within_struct", 20, ["sent",''], term1, term2 ]
        ]
        weight = [ 1.6, 1.2 ]
        ii = 0
        while ii < 2:
            # The summarization expression attaches a variable referencing
            # the entity to extract.
            # CONTINENT terms of type 'continent_var':
            sumexpr = [ "chain_struct", 50, ["sent",''],
                              [{'variable':"CONTINENT"}, "continent_var", ""],
                              expr[ ii] ]
            query.defineFeature( "sumfeat", sumexpr, weight[ ii] )
            sumexpr = [ "sequence_struct", -50, ["sent",''],
                              expr[ ii],
                              [{'variable':"CONTINENT"}, "continent_var", ""]
                      ]
            query.addFeature( "sumfeat", sumexpr, weight[ ii] )
            ii += 1

    # Helper method to define the query features created from a single
    # term query:
    def __defineSingleTermQueryFeatures( self, query, term):
        # Single term query:
        expr = [ term['type'], term['value'] ]
        # The summarization expression attaches a variable referencing an
        # the entity to extract.
        # CONTINENT terms of type 'continent_var':
        sumexpr = [ "chain_struct", 50, ["sent",''],
                      [{'variable':"CONTINENT"}, "continent_var", ""],
                      expr ]
        query.addFeature( "sumfeat", sumexpr, 1.0 )
        sumexpr = [ "sequence_struct", -50, ["sent",''],
                      expr,
                      [{'variable':"CONTINENT"}, "continent_var", ""]
                  ]
        query.addFeature( "sumfeat", sumexpr, 1.0 )

    # Query evaluation method that builds a ranked list from the best weighted entities
    # extracted from sentences with matches:
    def evaluateQueryEntities( self, querystr, firstrank, nofranks):
        queryeval = self.queryeval[ "NBLNK"]
        query = queryeval.createQuery( self.storage)
        terms = self.queryAnalyzer.analyzeTermExpression( [ "text", querystr ] )
        if len( terms) == 0:
             # Return empty result for empty query:
             return []
        # Build the weighting features. Queries with more than one term are building
        # the query features from pairs of terms:
        if len( terms) > 1:
            # Iterate on all permutation pairs of query features and creat
            # combined features for summarization:
            for pair in itertools.permutations(
                itertools.takewhile(
                        lambda x: x<len(terms), itertools.count()), 2):
                if pair[0] + 1 == pair[1]:
                    self.__defineSubsequentQueryTermFeatures( query, terms[pair[0]], terms[pair[1]])
                elif pair[0] < pair[0]:
                    self.__defineNonSubsequentQueryTermFeatures( query, terms[pair[0]], terms[pair[1]])
        else:
            self.__defineSingleTermQueryFeatures( query, terms[0] )
        # Define the selector ("selfeat") as the set of documents that contain all query terms
        # and define the single term features for weighting and candidate evaluation ("docfeat"):
        selexpr = ["contains", 0, 1]
        for term in terms:
            selexpr.append( term )
            query.addFeature( "docfeat", term, 1.0)
        query.addFeature( "selfeat", selexpr, 1.0 )

        # Evaluate the ranked list for getting the documents to inspect for entities close to matches:
        query.setMaxNofRanks( 300)
        query.setMinRank( 0)
        results = query.evaluate()
        # Build the table of all entities with weight of the top ranked documents:
        entitytab = {}
        for pos,result in enumerate(results['ranks']):
            for summary in result['summary']:
                if summary['name'] == 'ENTITY':
                    weight = 0.0
                    if summary['value'] in entitytab:
                        weight = entitytab[ summary['value'] ]
                    entitytab[ summary['value']] = weight + summary['weight']
        # Extract the top weighted documents in entitytab as result:
        heap = []
        for key, value in entitytab.items():
            heapq.heappush( heap, [value,key] )
        topEntities = heapq.nlargest( firstrank + nofranks, heap, lambda k: k[0])
        rt = []
        idx = 0
        maxrank = firstrank + nofranks
        for elem in topEntities[firstrank:maxrank]:
            rt.append({ 'weight':elem[0], 'title':elem[1] })
        return rt

