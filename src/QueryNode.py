# Import built-in libraries
import sys
import math
from collections import defaultdict
from copy import deepcopy

# Import src files
from InvertedList import InvertedList
from Posting import Posting


class QueryNode:
    def __init__(self, inverted_index):
        self.mu = 1500
        self.ctf = 0
        self.inverted_index = inverted_index

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

    def get_postings(self):
        return self.inverted_list.get_postings()

    def get_positions_in_current_posting(self):
        return self.postings[self.posting_index].get_term_positions()

    def has_more(self):
        return self.posting_index < len(self.postings)

    def next_candidate(self):
        if self.posting_index < len(self.postings):
            return self.postings[self.posting_index]
        # If there are no more postings, return a posting with doc id of -1
        return Posting(-1)

    def skip_to(self, doc_id):
        while self.posting_index < len(self.postings) and self.postings[self.posting_index].get_doc_id() < doc_id:
            self.posting_index += 1


class TermNode(QueryNode):
    def __init__(self, inverted_index, term):
        super().__init__(inverted_index)
        self.term = term
        self.inverted_list = self.get_inverted_list()
        self.postings = self.get_postings()
        self.posting_index = 0

    def get_inverted_list(self):
        return self.inverted_index.get_inverted_list(self.term)


class ProximityNode(QueryNode):
    def __init__(self, inverted_index, term_nodes, window_size):
        super().__init__(inverted_index)
        self.term_nodes = term_nodes
        self.window_size = window_size
        self.inverted_list = self.get_inverted_list()
        self.postings = self.get_postings()
        self.posting_index = 0

    def all_terms_have_more(self):
        # Check if all terms have more postings left in their respective postings lists
        return all(term_node.has_more() for term_node in self.term_nodes)

    def all_terms_on_same_doc(self, doc_id):
        for term_node in self.term_nodes:
            candidate_doc_id = term_node.next_candidate().get_doc_id()
            if candidate_doc_id == -1 or candidate_doc_id != doc_id:
                return False
        return True

    def get_window_positions(self):
        # Get a map of {doc_id: [positions]}
        # doc_id: Doc in which all the term nodes are present within the given window size
        # positions: Starting positions of the windows in the doc with given doc_id
        doc_window_positions = {}
        while self.all_terms_have_more():
            # Get the next doc_id for each term node
            doc_id_for_each_term = [term_node.next_candidate().get_doc_id() for term_node in self.term_nodes]

            # Find the max doc_id as its corresponding term is not present in any lower numbered doc
            # So, the lower numbered docs can be ignored
            max_doc_id = max(doc_id_for_each_term)

            # Move the postings lists of all terms to the max_doc_id if possible
            for term_node in self.term_nodes:
                term_node.skip_to(max_doc_id)
            all_term_nodes_on_same_doc = self.all_terms_on_same_doc(max_doc_id)

            # Check if all terms are on the same doc
            if all_term_nodes_on_same_doc:
                # Get all positions in the doc for each term (list of lists to maintain order in ordered window)
                term_positions = [term_node.get_positions_in_current_posting() for term_node in self.term_nodes]

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


class OrderedWindowNode(ProximityNode):
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
                            window_start_positions.append(
                                window_start_position)
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


class UnorderedWindowNode(ProximityNode):
    def __init__(self, inverted_index, term_nodes, window_size):
        super().__init__(inverted_index, term_nodes, window_size)

    def get_window_start_positions(self, term_positions):
        window_start_positions = list()

        num_terms = len(term_positions)
        if num_terms == 1:
            return term_positions[0]

        # For queries which have duplicate terms, the algorithm below to create unordered windows will
        # not work properly as when the term positions are sorted and the lowest positions are popped
        # out, it will pop out all of the duplicate term positions in successive iterations. This results
        # in the creation of the window only once for a duplicate term which is not desired, specially in
        # queries like "to be or not to be" where once all the windows for the first occurrence of "to" are
        # discarded, no more windows can be constructed using the second occurrence as all the positions have
        # already been popped out. So, a way around this is to distribute the positions among the multiple
        # term occurrences, so that the other duplicate occurrence can also get some windows around it.
        term_positions.sort(key=lambda x: x[0])
        distributed_term_positions = []
        current_term = 0
        # Loop through each term's positions list
        while current_term < num_terms:
            duplicate_count = 0
            # Get the positions list for the current term
            current_term_positions = term_positions[current_term]
            # Get the next term
            next_term = current_term + 1
            # Loop while there are duplicates
            while next_term < num_terms:
                # Get the next term's positions list
                next_term_positions = term_positions[next_term]
                # If the first positions match, if yes, then the list will match
                if next_term_positions[0] == current_term_positions[0]:
                    # Update duplicate counter
                    duplicate_count += 1
                    # Update next term
                    next_term += 1
                # Otherwise, there are no duplicates for this term
                else:
                    break
            # If there are duplicates, divide the positions among the terms equally so each of them can
            # at least one window while creating unordered windows
            if duplicate_count:
                for i in range(duplicate_count + 1):
                    start_position = i % (duplicate_count + 1)
                    step = duplicate_count + 1
                    distributed_term_positions.append(
                        current_term_positions[start_position::step])
            # Otherwise, no distribution of positions is required
            else:
                distributed_term_positions.append(current_term_positions)
            current_term = next_term
        term_positions = distributed_term_positions

        # It is going to be difficult to check the windows for terms if the windows can be constructed
        # on either side of a term position. To avoid this, sort all term positions to get the smallest
        # term position at every iteration through the term positions, so that we always construct the
        # window to the right of the current smallest term position. This position could correspond to a
        # term which is not the first term in the query string. This is allowed in an unordered window.

        # As long as there are positions left in any term's positions list, keep checking
        while all(len(term_pos_list) > 0 for term_pos_list in term_positions):
            # Sort the term positions lists in place as described above
            term_positions.sort(key=lambda x: x[0])
            # Create a window with the start position as the lowest position in the term positions list
            window_start_position = term_positions[0].pop(0)
            # Set the previous term position as the start of the window
            prev_term_position = window_start_position
            # Go through the other term's positions lists and check if they lie inside the window
            for term_pos_list in term_positions[1:]:
                # If the term's position lies inside the window of the previous term
                if prev_term_position < term_pos_list[0] and term_pos_list[0] < window_start_position + self.window_size:
                    # Set the previous term position as the position of this term and keep going
                    prev_term_position = term_pos_list[0]
                # Otherwise break the loop and get the next window
                else:
                    break
            # If the above for loop was not broken, it means that all the terms were found inside the window
            # So, add this window to the window_start_positions list
            else:
                window_start_positions.append(window_start_position)

        return window_start_positions


class BooleanAndNode(UnorderedWindowNode):
    def __init__(self, inverted_index, term_nodes):
        # Instead of getting lengths of each document for the window size
        # we can just set the window size to a very large number
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


class BeliefNode(QueryNode):
    def __init__(self, inverted_index, term_nodes):
        self.term_nodes = term_nodes
        super().__init__(inverted_index)

    def has_more(self):
        # If any term node has more documents, they need to be considered
        return any(term_node.has_more() for term_node in self.term_nodes)

    def next_candidate(self):
        # Consider the minimum next doc_id from all term nodes
        candidate = None
        min_doc_id = sys.maxsize
        for term_node in self.term_nodes:
            if term_node.has_more():
                doc_id = term_node.next_candidate().get_doc_id()
                if doc_id < min_doc_id:
                    min_doc_id = doc_id
                    candidate = term_node.next_candidate()
        return candidate

    def skip_to(self, doc_id):
        # Move all term nodes to the given doc_id
        for term_node in self.term_nodes:
            term_node.skip_to(doc_id)


class NotNode(BeliefNode):
    def __init__(self, inverted_index, term_nodes):
        super().__init__(inverted_index, term_nodes)

    def score(self, doc_id):
        term_node = self.term_nodes[0]
        probability = math.exp(term_node.score(doc_id))
        score = math.log(1 - probability)
        return score


class OrNode(BeliefNode):
    def __init__(self, inverted_index, term_nodes):
        super().__init__(inverted_index, term_nodes)

    def score(self, doc_id):
        total_probability = 0
        for term_node in self.term_nodes:
            probability = math.log(1 - math.exp(term_node.score(doc_id)))
            total_probability += probability
        return math.log(1 - math.exp(total_probability))


class WeightedAndNode(BeliefNode):
    def __init__(self, inverted_index, term_nodes, weights):
        self.weights = weights
        super().__init__(inverted_index, term_nodes)

    def score(self, doc_id):
        total_probability = 0
        for i, term_node in enumerate(self.term_nodes):
            weight = self.weights[i]
            probability = weight * term_node.score(doc_id)
            total_probability += probability
        return total_probability


class AndNode(WeightedAndNode):
    def __init__(self, inverted_index, term_nodes):
        weights = [1] * len(term_nodes)
        super().__init__(inverted_index, term_nodes, weights)


class WeightedSumNode(BeliefNode):
    def __init__(self, inverted_index, term_nodes, weights):
        self.weights = weights
        super().__init__(inverted_index, term_nodes)

    def score(self, doc_id):
        total_probability = 0
        total_weight = 0
        for i, term_node in enumerate(self.term_nodes):
            weight = self.weights[i]
            probability = weight * math.exp(term_node.score(doc_id))
            total_probability += probability
            total_weight += weight
        return math.log(total_probability / total_weight)


class SumNode(WeightedSumNode):
    def __init__(self, inverted_index, term_nodes):
        weights = [1] * len(term_nodes)
        super().__init__(inverted_index, term_nodes, weights)


class MaxNode(BeliefNode):
    def __init__(self, inverted_index, term_nodes):
        super().__init__(inverted_index, term_nodes)

    def score(self, doc_id):
        probabilities = [term_node.score(doc_id)
                         for term_node in self.term_nodes]
        return max(probabilities)
