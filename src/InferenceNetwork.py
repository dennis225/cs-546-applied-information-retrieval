from QueryNode import *

class InferenceNetwork:
    def __init__(self, inverted_index):
        super().__init__()

        self.inverted_index = inverted_index
        self.network_operator = None
    
    def get_operator(self, query_string, structured_query_operator, window_size):
        self.network_operator = None
        self.query_string = query_string
        terms = query_string.split()
        term_nodes = []
        for term in terms:
            term_node = TermNode(self.inverted_index, term)
            term_nodes.append(term_node)
        
        if structured_query_operator == 'OrderedWindow':
            self.network_operator = OrderedWindowNode(self.inverted_index, term_nodes, window_size)
        elif structured_query_operator == 'UnorderedWindow':
            self.network_operator = UnorderedWindowNode(self.inverted_index, term_nodes, window_size)
        elif structured_query_operator == 'BooleanAnd':
            self.network_operator = BooleanAndNode(self.inverted_index, term_nodes)
        elif structured_query_operator == 'Sum':
            self.network_operator = SumNode(self.inverted_index, term_nodes)
        elif structured_query_operator == 'And':
            self.network_operator = AndNode(self.inverted_index, term_nodes)
        elif structured_query_operator == 'Or':
            self.network_operator = OrNode(self.inverted_index, term_nodes)
        elif structured_query_operator == 'Max':
            self.network_operator = MaxNode(self.inverted_index, term_nodes)
        
        return self.network_operator
    
    # def get_documents(self, count=10):
    #     scores = defaultdict(int)
    #     results = []

    #     print(self.query_string)

    #     while self.network_operator.has_more():
    #         doc = self.network_operator.next_candidate()
    #         doc_id = doc.get_doc_id()
    #         self.network_operator.skip_to(doc_id)
    #         score = self.network_operator.score(doc)
    #         if score:
    #             scores[doc_id] = score
        
    #     scores_list = scores.items()
    #     sorted_scores_list = sorted(scores_list, key=lambda x: (x[1], x[0]), reverse=True)

    #     # Return the meta info of the top count number of documents
    #     for score in sorted_scores_list[:count]:
    #         doc_id = score[0]
    #         doc_meta = deepcopy(self.inverted_index.get_doc_meta(doc_id))
    #         doc_meta['score'] = score[1]
    #         results.append(doc_meta)
    #     return results
