from QueryNode import *

class InferenceNetwork:
    def __init__(self, inverted_index):
        super().__init__()

        self.inverted_index = inverted_index
    
    def get_operator(self, query_string, structured_query_operator, window_size):
        network_operator = None
        terms = query_string.split()
        term_nodes = []
        for term in terms:
            term_node = TermNode(self.inverted_index, term)
            term_nodes.append(term_node)
        
        if structured_query_operator == 'OrderedWindow':
            network_operator = OrderedWindowNode(self.inverted_index, term_nodes, window_size)
        elif structured_query_operator == 'UnorderedWindow':
            network_operator = UnorderedWindowNode(self.inverted_index, term_nodes, window_size)
        elif structured_query_operator == 'BooleanAnd':
            network_operator = BooleanAndNode(self.inverted_index, term_nodes)
        
        return network_operator
