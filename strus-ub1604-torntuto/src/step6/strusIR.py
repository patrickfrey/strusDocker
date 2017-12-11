class Backend:
    # Constructor creating a local Strus context with the storage configuration 
    # string passed as argument:
    def __init__(self, config):
        pass

    # Insert a multipart document as described in step 1 (doing nothing for the moment):
    def insertDocuments( self, content):
        return 0

    # Query evaluation scheme for a classical information retrieval query
    # with BM25 (returning a dummy ranked list with one element for now):
    def evaluateQueryText( self, querystr, firstrank, nofranks):
        rt = []
        rt.append( {
            'docno': 1,
            'title': "test document",
            'weight': 1.0,
            'abstract': "Neque porro quisquam est qui dolorem ipsum ..."
        })
        return rt

    # Query evaluation method that builds a ranked list from the best weighted entities
    # extracted from sentences with matches (returning an dummy list for with
    # one element now):
    def evaluateQueryEntities( self, querystr, firstrank, nofranks):
        rt = []
        rt.append( {
            'title': "test document",
            'weight': 1.0
        })
        return rt
