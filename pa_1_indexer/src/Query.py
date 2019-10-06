# Import built-in libraries
from collections import defaultdict
from copy import deepcopy


class Query:
    def __init__(self, config, inverted_index, retrieval_model='raw_counts', sort_results=True, mode='term', count=10):
        self.config = config
        self.inverted_index = inverted_index
        self.retrieval_model = retrieval_model
        self.sort_results = sort_results
        self.mode = mode
        self.count = count
    
    def get_documents(self, query_string):
        if self.mode == 'term':
            return self.term_at_a_time_retrieval(query_string)
        elif self.mode == 'doc':
            return self.document_at_a_time_retrieval(query_string)
        elif self.mode == 'conj_term':
            return self.conjunctive_term_at_a_time_retrieval(query_string)
        elif self.mode == 'conj_doc':
            return self.conjunctive_document_at_a_time_retrieval(query_string)
    
    def term_at_a_time_retrieval(self, query_string):
        scores = defaultdict(int)
        query_terms = query_string.split()
        results = []
        for term in query_terms:
            inverted_list = self.inverted_index.get_inverted_list(term)
            postings = inverted_list.get_postings()
            for posting in postings:
                doc_id = posting.get_doc_id()
                dtf = posting.get_dtf()
                if self.retrieval_model == 'raw_counts':
                    scores[doc_id] += dtf
        scores_list = scores.items()
        # https://stackoverflow.com/a/613218/6492944 - Sorting a list of tuples by second element in descending order
        sorted_scores_list = sorted(scores_list, key=lambda x: x[1], reverse=True)
        # Return the meta info of the top self.count number of documents
        for score in sorted_scores_list[:self.count]:
            doc_id = str(score[0])
            doc_meta = deepcopy(self.inverted_index.get_doc_meta(doc_id))
            doc_meta['score'] = score[1]
            results.append(doc_meta)
        return results

    def document_at_a_time_retrieval(self, query_string):
        pass
    
    def conjunctive_term_at_a_time_retrieval(self, query_string):
        pass

    def conjunctive_document_at_a_time_retrieval(self, query_string):
        pass
