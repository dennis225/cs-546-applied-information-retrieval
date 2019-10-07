class Query:
    """
    Class which exposes APIs to query an inverted index using various modes and scoring models
    """
    def __init__(self, config, inverted_index, retrieval_model='raw_counts', mode='term', count=10):
        """
        class config: Instance of the configuration of the active inverted index
        class inverted_index: The inverted index to use for querying
        str retrieval_model: Scoring model to be used for querying
        str mode: Type of querying algorithm to use
        int count: Number of documents to retrieve
        """
    
    def get_documents(self, query_string):
        """
        Returns a sorted list of documents from the index given a query
        str query_string: A query of arbitrary number of terms
        """
    
    def term_at_a_time_retrieval(self, query_string):
        """
        Returns documents using the term-at-a-time retrieval algorithm
        str query_string: A query of arbitrary number of terms
        """

    def document_at_a_time_retrieval(self, query_string):
        """
        Returns documents using the document-at-a-time retrieval algorithm
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
