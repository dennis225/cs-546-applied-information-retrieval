class Query:
    """
    Class which exposes APIs to query an inverted index using various modes and scoring models
    """
    def __init__(self,
                 config,
                 inverted_index,
                 mode='doc',
                 retrieval_model='dirichlet',
                 count=10,
                 k1=1.2,
                 k2=100,
                 b=0.75,
                 alphaD=0.1,
                 mu=1500):
        """
        class config: Instance of the configuration of the active inverted index
        class inverted_index: The inverted index to use for querying
        str mode: Type of querying algorithm to use
        str retrieval_model: Scoring model to be used for querying
        int count: Number of documents to retrieve
        int k1: Parameter used in BM25
        int k2: Parameter used in BM25
        int b: Parameter used in BM25
        int alphaD: Parameter used in Jelinek-Mercer Smoothing
        int mu: Parameter used in Dirichlet Smoothing
        """
    
    def get_documents(self, query_string):
        """
        Returns a sorted list of documents from the index given a query
        str query_string: A query of arbitrary number of terms
        """
    
    def term_at_a_time_retrieval(self, query_string):
        """
        Returns documents using the term-at-a-time retrieval algorithm
        Look at all the documents containing a query term and update each document's score
        Do this for each query term
        str query_string: A query of arbitrary number of terms
        """

    def document_at_a_time_retrieval(self, query_string):
        """
        Returns documents using the document-at-a-time retrieval algorithm
        Look at every document in the collection
        Check if it is present in the inverted list of a query term
        Update each document's score
        str query_string: A query of arbitrary number of terms
        """
    
    def conjunctive_term_at_a_time_retrieval(self, query_string):
        """
        Returns documents using the conjunctive-term-at-a-time retrieval algorithm
        str query_string: A query of arbitrary number of terms
        """

    def conjunctive_document_at_a_time_retrieval(self, query_string):
        """
        Returns documents using the conjunctive-document-at-a-time retrieval algorithm
        str query_string: A query of arbitrary number of terms
        """
