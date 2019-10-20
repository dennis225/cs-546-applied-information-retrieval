class RetrievalModels():
    """
    Class which exposes APIs to query an inverted index using various modes and scoring models
    """
    def __init__(self,
                 query_terms,
                 inverted_index,
                 retrieval_model='dirichlet',
                 k1=1.2,
                 k2=100,
                 b=0.75,
                 alphaD=0.1,
                 mu=1500):
        """
        list query_terms: List of terms in the query string
        class inverted_index: The inverted index to use for querying
        str retrieval_model: Scoring model to be used for querying
        int k1: Parameter used in BM25
        int k2: Parameter used in BM25
        int b: Parameter used in BM25
        int alphaD: Parameter used in Jelinek-Mercer Smoothing
        int mu: Parameter used in Dirichlet Smoothing
        """

    def get_score(self, query_term, doc):
        """
        Runs a scoring model and returns the score for a doc for a given query term
        str query_term: Query Term to calculate the doc score for
        class doc: Instance of Posting to be scored
        """

    def raw_counts(self, query_term, doc):
        """
        Returns a raw count score for a document - the dtf of the document
        str query_term: Query Term to calculate the doc score for
        class doc: Instance of Posting to be scored
        """

    def bm25(self, query_term, doc):
        """
        Returns a BM25 score for a document given a query term
        Summation for all query terms is done in the retrieval algorithm
        R and ri are set to 0 as there is no relevance information available
        str query_term: Query Term to calculate the doc score for
        class doc: Instance of Posting to be scored
        """

    def jelinek_mercer(self, query_term, doc):
        """
        Returns a Jelinek-Mercer smoothed query likelihood score for a document given a query term
        Summation for all query terms is done in the retrieval algorithm
        str query_term: Query Term to calculate the doc score for
        class doc: Instance of Posting to be scored
        """

    def dirichlet(self, query_term, doc):
        """
        Returns a Dirichlet smoothed query likelihood score for a document given a query term
        Summation for all query terms is done in the retrieval algorithm
        str query_term: Query Term to calculate the doc score for
        class doc: Instance of Posting to be scored
        """
