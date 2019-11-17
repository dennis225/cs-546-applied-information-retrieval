# Import built-in libraries
import sys
import math
from collections import defaultdict
from copy import deepcopy

# Import src files
from InvertedList import InvertedList


class QueryNode:
    def __init__(self, inverted_index):
        super().__init__()

        self.ctf = 0
        self.inverted_index = inverted_index
        self.inverted_list = None
        self.mu = 2000
    
    def score(self, doc):
        """
        Returns a Dirichlet smoothed query likelihood score for a document given a query term
        Summation for all query terms is done in the retrieval algorithm
        str query_term: Query Term to calculate the doc score for
        class doc: Instance of Posting to be scored
        """
        # Frequency of term/window in the document (document term/window frequency - dtf)
        fqiD = doc.get_dtf()
        # Length of the document
        dl = self.inverted_index.get_doc_length(doc.get_doc_id())
        # Frequency of term/window in the collection (collection term/window frequency - ctf)
        cqi = self.ctf
        # Total length of all documents in the collection
        cl = self.inverted_index.get_collection_length()
        
        score = math.log((fqiD + (self.mu * (cqi / cl))) / (dl + self.mu))
        return score

    def get_documents(self, count=10):
        scores = defaultdict(int)
        results = []
        
        postings = self.inverted_list.get_postings()
        for posting in postings:
            doc_id = posting.get_doc_id()
            score = self.score(posting)
            scores[doc_id] = score
        
        scores_list = scores.items()
        sorted_scores_list = sorted(scores_list, key=lambda x: (x[1], x[0]), reverse=True)

        # Return the meta info of the top count number of documents
        for score in sorted_scores_list[:count]:
            doc_id = score[0]
            doc_meta = deepcopy(self.inverted_index.get_doc_meta(doc_id))
            doc_meta['score'] = score[1]
            results.append(doc_meta)
        return results


class BeliefNode(QueryNode):
    def __init__(self, child_nodes):
        self.child_nodes = child_nodes
        super().__init__()
    
    def has_more(self):
        return any(child_node.has_more() for child_node in self.child_nodes)
    
    def next_candidate(self):
        return min(child_node.next_candidate() for child_node in self.child_nodes)
    
    def skip_to(self, doc_id):
        for child_node in self.child_nodes:
            child_node.skip_to(doc_id)


class NotNode(BeliefNode):
    def __init__(self, child_nodes):
        super().__init__(child_nodes)
    
    def score(self, doc_id):
        child_node = self.child_nodes[0]
        probability = math.exp(child_node.score(doc_id))
        score = math.log(1 - probability)
        return score


class OrNode(BeliefNode):
    def __init__(self, child_nodes):
        super().__init__(child_nodes)
    
    def score(self, doc_id):
        total_probability = 0
        for child_node in self.child_nodes:
            probability = math.log(1 - math.exp(child_node.score(doc_id)))
            total_probability += probability
        return math.log(1 - math.exp(total_probability))


class WeightedAndNode(BeliefNode):
    def __init__(self, child_nodes, weights):
        self.weights = weights
        super().__init__(child_nodes)
    
    def score(self, doc_id):
        total_probability = 0
        for i, child_node in enumerate(self.child_nodes):
            weight = self.weights[i]
            probability = weight * child_node.score(doc_id)
            total_probability += probability
        return total_probability


class AndNode(WeightedAndNode):
    def __init__(self, child_nodes):
        weights = [1] * len(child_nodes)
        super().__init__(child_nodes, weights)


class WeightedSumNode(BeliefNode):
    def __init__(self, child_nodes, weights):
        self.weights = weights
        super().__init__(child_nodes)
    
    def score(self, doc_id):
        total_probability = 0
        total_weight = 0
        for i, child_node in enumerate(self.child_nodes):
            weight = self.weights[i]
            probability = weight * math.exp(child_node.score(doc_id))
            total_probability += probability
            total_weight += weight
        return math.log(total_probability / total_weight)


class SumNode(WeightedSumNode):
    def __init__(self, child_nodes):
        weights = [1] * len(child_nodes)
        super().__init__(child_nodes, weights)


class MaxNode(BeliefNode):
    def __init__(self, child_nodes):
        super().__init__(child_nodes)
    
    def score(self, doc_id):
        probabilities = [child_node.score(doc_id) for child_node in self.child_nodes]
        return max(probabilities)
    

class ProximityNode(QueryNode):
    def __init__(self, inverted_index):
        super().__init__(inverted_index)
        self.inverted_list = self.get_inverted_list()
        self.postings = self.get_postings()
        self.posting_index = 0
    
    def has_more(self):
        return self.posting_index < len(self.postings)
    
    def next_candidate(self):
        # When the posting list pointer is moved to a new doc id
        # it is possible that the pointer moves past the end of the postings list
        # When it does, return a doc id of -1 because there is no corresponding
        # doc id at that position in the postings list
        if self.posting_index < len(self.postings):
            return self.postings[self.posting_index].get_doc_id()
        return -1
    
    def skip_to(self, doc_id):
        while self.posting_index < len(self.postings) and self.next_candidate() < doc_id:
            self.posting_index += 1
    
    def get_postings(self):
        return self.inverted_list.get_postings()
    
    def get_positions(self):
        return self.postings[self.posting_index].get_term_positions()


class TermNode(ProximityNode):
    def __init__(self, inverted_index, term):
        self.term = term
        super().__init__(inverted_index)
    
    def get_inverted_list(self):
        return self.inverted_index.get_inverted_list(self.term)


class WindowNode(ProximityNode):
    def __init__(self, inverted_index, term_nodes, window_size):
        self.term_nodes = term_nodes
        self.window_size = window_size
        super().__init__(inverted_index)
    
    def all_terms_have_more(self):
        # Check if all terms have more postings left in their respective postings lists
        return all(term_node.has_more() for term_node in self.term_nodes)
    
    def all_terms_on_same_doc(self, doc_id):
        return all(term_node.next_candidate() == doc_id for term_node in self.term_nodes)
    
    def get_window_positions(self):
        # Get a map of {doc_id: [positions]}
        # doc_id: Doc in which all the query terms are present in the given window size
        # positions: Starting positions of the windows in the doc with given doc_id
        doc_window_positions = {}
        while self.all_terms_have_more():
            # Get current doc_id for each term
            doc_id_for_each_term = [term_node.next_candidate() for term_node in self.term_nodes]
            
            # Find the max doc_id as its corresponding term is not present in any lower numbered doc
            # So, the lower numbered docs can be ignored
            max_doc_id = max(doc_id_for_each_term)

            # Move the postings lists of all terms to the max_doc_id if possible
            for term_node in self.term_nodes:
                term_node.skip_to(max_doc_id)
            all_term_nodes_on_same_doc = self.all_terms_on_same_doc(max_doc_id)
            
            # Check if all terms are on the same doc
            if all_term_nodes_on_same_doc:
                # Get all term positions in the doc
                term_positions = [term_node.get_positions() for term_node in self.term_nodes]
                
                # Find the window start positions (there could be multiple windows with all query terms)
                window_start_positions = self.get_window_start_positions(term_positions)

                # Add the window start positions to the doc_window_positions for the query
                doc_window_positions[max_doc_id] = window_start_positions
            
            # Move all term nodes to the next doc after max_doc_id if possible
            next_doc_id = max_doc_id + 1
            for term_node in self.term_nodes:
                term_node.skip_to(next_doc_id)
        
        return doc_window_positions

    def get_inverted_list(self):
        inverted_list = InvertedList()
        doc_window_positions = self.get_window_positions()
        for doc_id, positions in doc_window_positions.items():
            if positions:
                inverted_list.add_posting_with_positions(doc_id, positions)
                self.ctf += len(positions)
        return inverted_list


class OrderedWindowNode(WindowNode):
    def __init__(self, inverted_index, term_nodes, window_size):
        super().__init__(inverted_index, term_nodes, window_size)
    
    def get_window_start_positions(self, term_positions):
        window_start_positions = list()

        num_terms = len(term_positions)
        if num_terms == 1:
            return term_positions[0]
        
        term_positions_pointers = [0] * num_terms
        current_term = 0

        for window_start_position in term_positions[current_term]:
            # Set the previous term position as the start of the window
            prev_term_position = window_start_position
            # Move the pointer of the first term by one
            term_positions_pointers[current_term] += 1
            # Move to the next term for looping again
            current_term = 1
            # While we haven't reached the end of terms and while there are more positions in the current term's positions list
            while current_term < num_terms and term_positions_pointers[current_term] < len(term_positions[current_term]):
                # Get the current term's current position pointer
                current_term_pointer = term_positions_pointers[current_term]
                # Move the current term's pointer either inside the window of the previous term or beyond it
                while current_term_pointer < len(term_positions[current_term]) and term_positions[current_term][current_term_pointer] < prev_term_position + self.window_size:
                    current_term_pointer += 1
                # If the pointer hasn't reached the end of the current term's positions list, continue
                if current_term_pointer < len(term_positions[current_term]):
                    term_positions_pointers[current_term] = current_term_pointer
                    # If the current term's current position is outside the window
                    if term_positions[current_term][current_term_pointer] - prev_term_position > self.window_size:
                        # Go back to the previous term and do this again
                        current_term -= 1
                        # If the current term is not the first term, continue
                        if current_term != 0:
                            current_term_pointer = term_positions_pointers[current_term]
                            prev_term_position = term_positions[current_term][current_term_pointer]
                        # If it is the first term, break to get a new window
                        else:
                            break
                    # If the current term's current position is inside the window, continue
                    else:
                        # Check if this is the last term
                        # If yes, we have found a window with all words in it
                        if current_term == num_terms - 1:
                            # Add this window to the window_start_positions list
                            window_start_positions.append(window_start_position)
                            # Reset the current term to the first term
                            current_term = 0
                            break
                        # If this is not the last term, move the window to the current term's current position
                        # And then move to the next term and do this again
                        else:
                            prev_term_position = term_positions[current_term][current_term_pointer]
                            current_term += 1
                # Otherwise break out of the loop as it's not possible for the following words to be in this window as well
                # And return an empty list
                else:
                    current_term = 0
                    break
        return window_start_positions


class UnorderedWindowNode(WindowNode):
    def __init__(self, inverted_index, term_nodes, window_size):
        super().__init__(inverted_index, term_nodes, window_size)
    
    def get_window_start_positions(self, term_positions):
        positions = list()

        if len(term_positions) == 1:
            return term_positions[0]

        term_positions.sort(key=lambda x: x[0])

        final_term_positions = []

        # Optimization to fix bug (to be or not to be) and make processing faster
        # The gist is that repeating words in the queries have duplicate repeating positions and we can discard
        # half (alternate) of the positions from each duplicate position list to make things faster
        # This can handle two or even more occurrences of the query word
        idx = 0
        while idx < len(term_positions):
            shortlist = [term_positions[idx]]
            idx_2 = idx + 1
            while idx_2 < len(term_positions):
                if term_positions[idx_2][0] == term_positions[idx][0]:
                    shortlist.append(term_positions[idx_2])
                    idx_2 += 1
                else:
                    break
            if len(shortlist) == 1:
                final_term_positions.append(shortlist[0])
            else:
                for i in range(len(shortlist)):
                    final_term_positions.append(shortlist[0][i % 2::2])
            idx = idx_2
        term_positions = final_term_positions

        while all(len(l) > 0 for l in term_positions):
            term_positions.sort(key=lambda x: x[0])
            left = term_positions[0].pop(0)
            prev = left
            for l in term_positions[1:]:
                if prev < l[0] < left + self.window_size:
                    prev = l[0]
                else:
                    if l[0] == prev:
                        l.pop(0)
                    break
            else:
                positions.append(left)

        return positions


class BooleanAndNode(UnorderedWindowNode):
    def __init__(self, inverted_index, term_nodes):
        super().__init__(inverted_index, term_nodes, window_size=sys.maxsize)


class FilterNode(QueryNode):
    def __init__(self, inverted_index, query_node, proximity_node):
        self.query_node = query_node
        self.proximity_node = proximity_node
        super().__init__(inverted_index)
    
    def skip_to(self, doc_id):
        self.query_node.skip_to(doc_id)
        self.proximity_node.skip_to(doc_id)


class FilterRequire(FilterNode):
    def __init__(self, inverted_index, query_node, proximity_node):
        super().__init__(inverted_index, query_node, proximity_node)
    
    def has_more(self):
        return self.query_node.has_more() and self.proximity_node.has_more()
    
    def next_candidate(self):
        return max(self.query_node.next_candidate(), self.proximity_node.next_candidate())
    
    def score(self, doc_id):
        # Move the proximity node to the given doc_id
        self.proximity_node.skip_to(doc_id)

        # Check if the proximity node was able to move to the given doc_id
        # If yes, score the document
        if self.proximity_node.next_candidate() == doc_id:
            return self.query_node.score(doc_id)
        # Otherwise return a score of 0
        return 0


class FilterReject(FilterNode):
    def __init__(self, inverted_index, query_node, proximity_node):
        super().__init__(inverted_index, query_node, proximity_node)
    
    def has_more(self):
        return self.query_node.has_more()
    
    def next_candidate(self):
        return self.query_node.next_candidate()
    
    def score(self, doc_id):
        # Move the proximity node to the given doc_id
        self.proximity_node.skip_to(doc_id)

        # Check if the proximity node was able to move to the given doc_id
        # If yes, return a score of 0
        if self.proximity_node.next_candidate() == doc_id:
            return 0
        # Otherwise score the document
        return self.query_node.score(doc_id)
