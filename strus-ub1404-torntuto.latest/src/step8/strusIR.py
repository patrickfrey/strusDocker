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
        rt.defineDocument( "doc", "/list/doc")
        # Define the terms to search for (inverted index or search index):
        rt.addSearchIndexFeature( "word", "/list/doc//()",
                                  "word", ("lc",("stem","en"),("convdia","en")))
        # Define the end of sentence markers:
        rt.addSearchIndexFeature( "sent", "/list/doc//()",
                                  ("punctuation","en","."), "empty")
        # Define the placeholders that are referencable by variables:
        rt.addSearchIndexFeature( "continent_var", "/list/doc/continent@id",
                                  "content", "empty", "BindPosSucc")
        # Define the original terms in the document used for abstraction:
        rt.addForwardIndexFeature( "orig", "/list/doc//()", "split", "orig")
        # Define the contents that extracted by variables:
        rt.addForwardIndexFeature( "continent", "/list/doc/continent@id",
                                   "content", "text", "BindPosSucc")
        # Define the document identifier:
        rt.defineAttribute( "docid", "/list/doc@id", "content", "text")
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
        rt.addSummarizer( "TITLE", "attribute", { "name": "docid" })
        # Summarizer for abstracting:
        rt.addSummarizer( "CONTENT", "matchphrase", {
                  "type": "orig", "len": 40, "nof": 3, "structseek": 30,
                  "mark": '<b>$</b>', ".struct": "sentence", ".match": "docfeat" })
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
        rt.addWeightingFunction( 1.0, "BM25", {
                 "k1": 0.75, "b": 2.1, "avgdoclen": 500, ".match": "docfeat" })
        # Summarizer to extract the weighted entities:
        rt.addSummarizer(
            "ENTITY", "accuvariable",
                 { ".match": "sumfeat", "var": "CONTINENT", "type": "continent" })
        return rt

    # Constructor. Initializes the query evaluation schemes and the query and document analyzers:
    def __init__(self, config):
        if isinstance( config, ( int, long ) ):
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
        docqueue = self.documentAnalyzer.createQueue()
        docqueue.push( content)
        while (docqueue.hasMore()):
            doc = docqueue.fetch()
            self.storage.insertDocument( doc.docid(), doc)
            rt += 1
        self.storage.flush()
        return rt

    # Query evaluation scheme for a classical information retrieval query with BM25:
    def evaluateQueryText( self, querystr, firstrank, nofranks):
        queryeval = self.queryeval[ "BM25"]
        query = queryeval.createQuery( self.storage)
        terms = self.queryAnalyzer.analyzePhrase( "text", querystr)
        if len( terms) == 0:
            # Return empty result for empty query:
            return []

        selexpr = ["contains"]
        for term in terms:
            selexpr.append( [term.type(), term.value()] )
            query.defineFeature( "docfeat", [term.type(), term.value()], 1.0)
        query.defineFeature( "selfeat", selexpr, 1.0 )
        query.setMaxNofRanks( nofranks)
        query.setMinRank( firstrank)
        # Evaluate the query:
        results = query.evaluate()
        # Rewrite the results:
        rt = []
        for result in results:
            content = ""
            title = ""
            for attribute in result.attributes():
                if attribute.name() == 'CONTENT':
                    if content != "":
                        content += ' ... '
                    content += attribute.value()
                elif attribute.name() == 'TITLE':
                    title = attribute.value()
            rt.append( {
                   'docno':result.docno(),
                   'title':title,
                   'weight':result.weight(),
                   'abstract':content })
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
                [ "sequence_struct", 3,
                    ["sent"],
                    [term1.type(), term1.value()],
                    [term2.type(), term2.value()]
                ],
                [ "sequence_struct", 3,
                    ["sent"],
                    [term2.type(), term2.value()],
                    [term1.type(), term1.value()]
                ],
                [ "within_struct", 5,
                    ["sent"],
                    [term1.type(), term1.value()],
                    [term2.type(), term2.value()]
                ],
                [ "within_struct", 20,
                    ["sent"],
                    [term1.type(), term1.value()],
                    [term2.type(), term2.value()]
                ]
        ]
        weight = [ 3.0, 2.0, 2.0, 1.5 ]
        ii = 0
        while ii < 4:
            # The summarization expression attaches a variable referencing an
            # the entity to extract.
            # CONTINENT ("=CONTINENT") to continents (terms of type 'continent_var'):
            sumexpr = [ "chain_struct", 50, ["sent"],
                          ["=CONTINENT", "continent_var"],
                          expr[ ii] ]
            query.defineFeature( "sumfeat", sumexpr, weight[ ii] )
            sumexpr = [ "sequence_struct", -50, ["sent"],
                          expr[ ii],
                          ["=CONTINENT", "continent_var"],
                      ]
            query.defineFeature( "sumfeat", sumexpr, weight[ ii] )
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
                [ "within_struct", 5,
                    ["sent"],
                    [term1.type(), term1.value()],
                    [term2.type(), term2.value()]
                ],
                [ "within_struct", 20,
                    ["sent"],
                    [term1.type(), term1.value()],
                    [term2.type(), term2.value()]
                ]
        ]
        weight = [ 1.6, 1.2 ]
        ii = 0
        while ii < 2:
            # The summarization expression attaches a variable referencing
            # the entity to extract.
            # CONTINENT ("=CONTINENT") to continents (terms of type 'continent_var'):
            sumexpr = [ "chain_struct", 50, ["sent"],
                              ["=CONTINENT", "continent_var"],
                              expr[ ii] ]
            query.defineFeature( "sumfeat", sumexpr, weight[ ii] )
            sumexpr = [ "sequence_struct", -50, ["sent"],
                              expr[ ii],
                              ["=CONTINENT", "continent_var"]
                      ]
            query.defineFeature( "sumfeat", sumexpr, weight[ ii] )
            ii += 1

    # Helper method to define the query features created from a single
    # term query:
    def __defineSingleTermQueryFeatures( self, query, term):
        # Single term query:
        expr = [ term.type(), term.value() ]
        # The summarization expression attaches a variable referencing an
        # the entity to extract.
        # CONTINENT ("=CONTINENT") to continents (terms of type 'continent_var'):
        sumexpr = [ "chain_struct", 50, ["sent"],
                      ["=CONTINENT", "continent_var"],
                      expr ]
        query.defineFeature( "sumfeat", sumexpr, 1.0 )
        sumexpr = [ "sequence_struct", -50, ["sent"],
                      expr,
                      ["=CONTINENT", "continent_var"]
                  ]
        query.defineFeature( "sumfeat", sumexpr, 1.0 )

    # Query evaluation method that builds a ranked list from the best weighted entities
    # extracted from sentences with matches:
    def evaluateQueryEntities( self, querystr, firstrank, nofranks):
        queryeval = self.queryeval[ "NBLNK"]
        query = queryeval.createQuery( self.storage)
        terms = self.queryAnalyzer.analyzePhrase( "text", querystr)
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
        selexpr = ["contains"]
        for term in terms:
            selexpr.append( [term.type(), term.value()] )
            query.defineFeature( "docfeat", [term.type(), term.value()], 1.0 )
        query.defineFeature( "selfeat", selexpr, 1.0 )
        # Evaluate the ranked list for getting the documents to inspect for entities close to matches:
        query.setMaxNofRanks( 300)
        query.setMinRank( 0)
        results = query.evaluate()
        # Build the table of all entities with weight of the top ranked documents:
        entitytab = {}
        for result in results:
            for attribute in result.attributes():
                if attribute.name() == 'ENTITY':
                    weight = 0.0
                    if attribute.value() in entitytab:
                        weight = entitytab[ attribute.value()]
                    entitytab[ attribute.value()] = weight + attribute.weight()
        # Extract the top weighted documents in entitytab as result:
        heap = []
        for key, value in entitytab.iteritems():
            heapq.heappush( heap, {'entity':key, 'weight':value})
        topEntities = heapq.nlargest( firstrank + nofranks, heap, lambda k: k['weight'])
        rt = []
        idx = 0
        maxrank = firstrank + nofranks
        for elem in topEntities[firstrank:maxrank]:
            rt.append({
                'title':elem['entity'],
                'weight':elem['weight']
            })
        return rt

