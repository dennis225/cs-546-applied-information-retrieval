from QueryNode import *


class InferenceNetwork:
    def __init__(self, inverted_index, query_string, structured_query_operator, window_size):
        self.inverted_index = inverted_index
        self.query_string = query_string
        self.structured_query_operator = structured_query_operator
        self.window_size = window_size
        self.network_operator = self.get_operator()

    def get_operator(self):
        terms = self.query_string.split()
        term_nodes = []
        for term in terms:
            term_node = TermNode(self.inverted_index, term)
            term_nodes.append(term_node)

        if self.structured_query_operator == 'OrderedWindow':
            return OrderedWindowNode(self.inverted_index, term_nodes, self.window_size)
        elif self.structured_query_operator == 'UnorderedWindow':
            return UnorderedWindowNode(self.inverted_index, term_nodes, self.window_size)
        elif self.structured_query_operator == 'BooleanAnd':
            return BooleanAndNode(self.inverted_index, term_nodes)
        elif self.structured_query_operator == 'Sum':
            return SumNode(self.inverted_index, term_nodes)
        elif self.structured_query_operator == 'And':
            return AndNode(self.inverted_index, term_nodes)
        elif self.structured_query_operator == 'Or':
            return OrNode(self.inverted_index, term_nodes)
        elif self.structured_query_operator == 'Max':
            return MaxNode(self.inverted_index, term_nodes)

    def get_documents(self, count=10):
        scores = defaultdict(int)
        results = []

        if self.network_operator.has_anything():
            while self.network_operator.has_more():
                doc = self.network_operator.next_candidate()
                doc_id = doc.get_doc_id()
                score = self.network_operator.score(doc)
                if score:
                    scores[doc_id] = score
                self.network_operator.skip_to(doc_id + 1)

        scores_list = scores.items()
        sorted_scores_list = sorted(
            scores_list, key=lambda x: (x[1], x[0]), reverse=True)

        # Return the meta info of the top count number of documents
        for score in sorted_scores_list[:count]:
            doc_id = score[0]
            doc_meta = deepcopy(self.inverted_index.get_doc_meta(doc_id))
            doc_meta['score'] = score[1]
            results.append(doc_meta)
        return results
