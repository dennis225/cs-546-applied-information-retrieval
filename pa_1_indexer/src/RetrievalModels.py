import math


class RetrievalModels():
    def __init__(self,
                 query_terms,
                 inverted_index,
                 retrieval_model='raw_counts',
                 k1=1.2,
                 k2=100,
                 b=0.75,
                 alphaD=0.1,
                 mu=1500):
        self.query_terms = query_terms
        self.inverted_index = inverted_index
        self.retrieval_model = retrieval_model
        self.k1 = k1
        self.k2 = k2
        self.b = b
        self.alphaD = alphaD    # Coefficient controlling the probability assigned to unseen words
        self.mu = mu

    def get_score(self, query_term, doc):
        if self.retrieval_model == 'raw_counts':
            return self.raw_counts(doc)
        elif self.retrieval_model == 'bm25':
            return self.bm25(query_term, doc)
        elif self.retrieval_model == 'jelinek_mercer':
            return self.jelinek_mercer(query_term, doc)
        elif self.retrieval_model == 'dirichlet':
            return self.dirichlet(query_term, doc)

    def raw_counts(self, doc):
        """
        Returns a raw count score for a document - the dtf of the document
        class doc: Instance of Posting to be scored
        """
        return doc.get_dtf()

    def bm25(self, query_term, doc):
        """
        Returns a BM25 score for a document given a query term
        Summation for all query terms is done in the retrieval algorithm
        R and ri are set to 0 as there is no relevance information available
        str query_term: Query Term to calculate the doc score for
        class doc: Instance of Posting to be scored
        """
        # Frequency of term in the document (document term frequency - dtf)
        fi = doc.get_dtf()
        # Frequency of term in the query
        qfi = self.query_terms.count(query_term)
        # Number of documents containing the term (document frequency - df)
        ni = self.inverted_index.get_df(query_term)
        # Number of documents in the collection
        N = self.inverted_index.get_total_docs()
        # Length of the document
        dl = self.inverted_index.get_doc_length(doc.get_doc_id())
        # Average length of a document in the collection
        avdl = self.inverted_index.get_average_doc_length()
        K = self.k1 * ((1 - self.b) + self.b * (dl / avdl))
        score = math.log((N - ni + 0.5) / ni + 0.5) * ((self.k1 + 1)
                                                       * fi / (K + fi)) * ((self.k2 + 1) * qfi / (self.k2 + qfi))
        return score

    def jelinek_mercer(self, query_term, doc):
        """
        Returns a Jelinek-Mercer smoothed query likelihood score for a document given a query term
        Summation for all query terms is done in the retrieval algorithm
        str query_term: Query Term to calculate the doc score for
        class doc: Instance of Posting to be scored
        """
        # Frequency of term in the document (document term frequency - dtf)
        fqiD = doc.get_dtf()
        # Length of the document
        dl = self.inverted_index.get_doc_length(doc.get_doc_id())
        # Frequency of term in the collection (collection term frequency - ctf)
        cqi = self.inverted_index.get_ctf(query_term)
        # Total length of all documents in the collection
        cl = self.inverted_index.get_collection_length()
        score = math.log(((1 - self.alphaD) * (fqiD / dl)) +
                         (self.alphaD * (cqi / cl)))
        return score

    def dirichlet(self, query_term, doc):
        """
        Returns a Dirichlet smoothed query likelihood score for a document given a query term
        Summation for all query terms is done in the retrieval algorithm
        str query_term: Query Term to calculate the doc score for
        class doc: Instance of Posting to be scored
        """
        # Frequency of term in the document (document term frequency - dtf)
        fqiD = doc.get_dtf()
        # Length of the document
        dl = self.inverted_index.get_doc_length(doc.get_doc_id())
        # Frequency of term in the collection (collection term frequency - ctf)
        cqi = self.inverted_index.get_ctf(query_term)
        # Total length of all documents in the collection
        cl = self.inverted_index.get_collection_length()
        score = math.log((fqiD + (self.mu * (cqi / cl))) / (dl + self.mu))
        return score
