class QueryNode:
    def __init__(self, inverted_index):
        """
        Keeps a list of variables to be used in child classes
        """
    
    def score(self, doc):
        """
        Returns a Dirichlet smoothed query likelihood score for a document given a query term
        Summation for all query terms is done in the retrieval algorithm
        str query_term: Query Term to calculate the doc score for
        class doc: Instance of Posting to be scored
        """

    def get_documents(self, count=10):
        """
        Returns a list of count number of scored documents
        """


class BeliefNode(QueryNode):
    def __init__(self, child_nodes):
        """
        Initializes the Query Node parent class
        """
    
    def has_more(self):
        """
        Returns a boolean value describing whether there are more documents present
        """
    
    def next_candidate(self):
        """
        Returns the next candidate document
        """
    
    def skip_to(self, doc_id):
        """
        Skips to the given doc ID
        """


class NotNode(BeliefNode):
    def __init__(self, child_nodes):
        """
        Initializes the Belief Node parent class
        """
    
    def score(self, doc_id):
        """
        Scores the document using the NOT operator
        """


class OrNode(BeliefNode):
    def __init__(self, child_nodes):
        """
        Initializes the Belief Node parent class
        """
    
    def score(self, doc_id):
        """
        Scores the document using the OR operator
        """


class WeightedAndNode(BeliefNode):
    def __init__(self, child_nodes, weights):
        """
        Initializes the Belief Node parent class
        """
    
    def score(self, doc_id):
        """
        Scores the document using the WAND operator
        """


class AndNode(WeightedAndNode):
    def __init__(self, child_nodes):
        """
        Initializes the WeightedAnd Node parent class
        It's a weighted and with all weights as 1
        """


class WeightedSumNode(BeliefNode):
    def __init__(self, child_nodes, weights):
        """
        Initializes the Belief Node parent class
        """
    
    def score(self, doc_id):
        """
        Scores the document using the WSUM operator
        """


class SumNode(WeightedSumNode):
    def __init__(self, child_nodes):
        """
        Initializes the WeightedSum Node parent class
        It's a weighted sum with all weights as 1
        """


class MaxNode(BeliefNode):
    def __init__(self, child_nodes):
        """
        Initializes the Belief Node parent class
        """
    
    def score(self, doc_id):
        """
        Scores the document using the MAX operator
        """
    

class ProximityNode(QueryNode):
    def __init__(self, inverted_index):
        """
        Initializes the Query Node parent class
        """
    
    def has_more(self):
        """
        Returns a boolean value describing whether there are more documents present
        """
    
    def next_candidate(self):
        # When the posting list pointer is moved to a new doc id
        # it is possible that the pointer moves past the end of the postings list
        # When it does, return a doc id of -1 because there is no corresponding
        # doc id at that position in the postings list
        """
        Returns the next candidate document
        """
    
    def skip_to(self, doc_id):
        """
        Skips to the given doc ID
        """
    
    def get_postings(self):
        """
        Get a list of postings for this node
        """
    
    def get_positions(self):
        """
        Get a list of positions at the current posting index for this node
        """


class TermNode(ProximityNode):
    def __init__(self, inverted_index, term):
        """
        Initializes the Proximity Node parent class
        """
    
    def get_inverted_list(self):
        """
        Get the inverted list for the term for this term node
        """


class WindowNode(ProximityNode):
    def __init__(self, inverted_index, term_nodes, window_size):
        """
        Initializes the Proximity Node parent class
        Uses a list of term nodes to define the window
        Uses the window size for calculating windows
        """
    
    def all_terms_have_more(self):
        """
        Check if all terms have more postings left in their respective postings lists
        """
    
    def all_terms_on_same_doc(self, doc_id):
        """
        Check if all terms are on the same doc id
        """
    
    def get_window_positions(self):
        """
        Returns a map of {doc_id: [positions]}
        doc_id: Doc in which all the query terms are present in the given window size
        positions: Starting positions of the windows in the doc with given doc_id
        """

    def get_inverted_list(self):
        """
        Get the inverted list for the window for this node
        """


class OrderedWindowNode(WindowNode):
    def __init__(self, inverted_index, term_nodes, window_size):
        """
        Initializes the Window Node parent class
        """
    
    def get_window_start_positions(self, term_positions):
        """
        Get the ordered windows for this node given a list of term positions
        """


class UnorderedWindowNode(WindowNode):
    def __init__(self, inverted_index, term_nodes, window_size):
        """
        Initializes the Window Node parent class
        """
    
    def get_window_start_positions(self, term_positions):
        """
        Get the unordered windows for this node given a list of term positions
        """


class BooleanAndNode(UnorderedWindowNode):
    def __init__(self, inverted_index, term_nodes):
        """
        Initializes the UnorderedWindow Node parent class
        Instead of getting lengths of each document for the window size
        we can just set the window size to a very large number
        """


class FilterNode(QueryNode):
    def __init__(self, inverted_index, query_node, proximity_node):
        """
        Initializes the Query Node parent class
        Uses query node to get the query term
        Uses the proximity node to get the terms in the window around query term
        """
    
    def skip_to(self, doc_id):
        """
        Skips both the query and proximity nodes to the given doc ID
        """


class FilterRequire(FilterNode):
    def __init__(self, inverted_index, query_node, proximity_node):
        """
        Initializes the Filter Node parent class
        """
    
    def has_more(self):
        """
        Returns a boolean value describing whether there are more documents present
        """
    
    def next_candidate(self):
        """
        Returns the next candidate document
        """
    
    def score(self, doc_id):
        """
        Score the document with the given doc_id
        """


class FilterReject(FilterNode):
    def __init__(self, inverted_index, query_node, proximity_node):
        """
        Initializes the Filter Node parent class
        """
    
    def has_more(self):
        """
        Returns a boolean value describing whether there are more documents present
        """
    
    def next_candidate(self):
        """
        Returns the next candidate document
        """
    
    def score(self, doc_id):
        """
        Score the document with the given doc_id
        """
