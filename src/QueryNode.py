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
        self.inverted_list = InvertedList()
        self.mu = 1500
    
    def get_doc_score(self, doc):
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
            score = self.get_doc_score(posting)
            scores[doc_id] = score
        
        scores_list = scores.items()
        # https://stackoverflow.com/a/613218/6492944 - Sorting a list of tuples by second element in descending order
        # https://stackoverflow.com/questions/54300715/python-3-list-sorting-with-a-tie-breaker
        # When sorting two docs with same scores, they are sorted by document ID to maintain consistency
        sorted_scores_list = sorted(scores_list, key=lambda x: (x[1], x[0]), reverse=True)

        # Return the meta info of the top count number of documents
        for score in sorted_scores_list[:count]:
            doc_id = score[0]
            doc_meta = deepcopy(self.inverted_index.get_doc_meta(doc_id))
            doc_meta['score'] = score[1]
            results.append(doc_meta)
        return results


class BeliefNode(QueryNode):
    def __init__(self, childNodes):
        super().__init__()
        self.childNodes = childNodes


class NotNode(BeliefNode):
    def __init__(self):
        super().__init__()


class OrNode(BeliefNode):
    def __init__(self):
        super().__init__()


class AndNode(BeliefNode):
    def __init__(self):
        super().__init__()


class WeightedAndNode(BeliefNode):
    def __init__(self):
        super().__init__()


class MaxNode(BeliefNode):
    def __init__(self):
        super().__init__()


class SumNode(BeliefNode):
    def __init__(self):
        super().__init__()


class WeightedSumNode(BeliefNode):
    def __init__(self):
        super().__init__()
    

class ProximityNode(QueryNode):
    def __init__(self, inverted_index):
        super().__init__(inverted_index)
    
    # def score()


class TermNode(ProximityNode):
    def __init__(self, inverted_index, term):
        super().__init__(inverted_index)
        self.term = term
        inverted_list = self.inverted_index.get_inverted_list(term)
        self.postings = inverted_list.get_postings()
        self.term_posting_index = 0
    
    def has_more_postings(self):
        return self.term_posting_index < len(self.postings) - 1
    
    def get_doc_id(self):
        return self.postings[self.term_posting_index].get_doc_id()
    
    def move_to_doc_id(self, doc_id):
        while self.term_posting_index < len(self.postings) - 1:
            if self.get_doc_id() < doc_id:
                self.term_posting_index += 1
            else:
                break

    def get_term_positions(self):
        return self.postings[self.term_posting_index].get_term_positions()


class WindowNode(ProximityNode):
    def __init__(self, inverted_index, term_nodes, window_size):
        super().__init__(inverted_index)
        self.term_nodes = term_nodes
        self.window_size = window_size
    
    def all_terms_have_more_postings(self):
        # Check if all terms have more postings left in their respective postings lists
        return all(term_node.has_more_postings() for term_node in self.term_nodes)
    
    def all_terms_on_same_doc(self, doc_id):
        return all(term_node.get_doc_id() == doc_id for term_node in self.term_nodes)
    
    def get_docs_with_query_terms_in_window(self):
        # Get a map of {doc_id: [positions]}
        # doc_id: Doc in which all the query terms are present in the given window size
        # positions: Starting positions of the windows in the doc with given doc_id
        doc_window_positions = {}
        while self.all_terms_have_more_postings():
            # Get current doc_id for each term
            doc_id_for_each_term = [term_node.get_doc_id() for term_node in self.term_nodes]
            
            # Find the max doc_id as its corresponding term is not present in any lower numbered doc
            # So, the lower numbered docs can be ignored
            max_doc_id = max(doc_id_for_each_term)

            # Move the postings lists of all terms to the max_doc_id if possible
            for term_node in self.term_nodes:
                term_node.move_to_doc_id(max_doc_id)
            all_term_nodes_on_same_doc = self.all_terms_on_same_doc(max_doc_id)
            
            # Check if all terms are on the same doc
            if all_term_nodes_on_same_doc:
                # print('All terms on Doc ID: ', max_doc_id)
                # Get all term positions in the doc
                term_positions = [term_node.get_term_positions() for term_node in self.term_nodes]
                # print(term_positions)
                
                # Find the window start positions (there could be multiple windows with all query terms)
                window_start_positions = self.get_window_start_positions(term_positions)
                # print('Window Start Positions: ', window_start_positions)

                # Add the window start positions to the doc_window_positions for the query
                doc_window_positions[max_doc_id] = window_start_positions
            
            # Move all term nodes to the next doc after max_doc_id if possible
            next_doc_id = max_doc_id + 1
            for term_node in self.term_nodes:
                term_node.move_to_doc_id(next_doc_id)
        
        return doc_window_positions
    
    def get_inverted_list_for_query_terms(self):
        doc_window_positions = self.get_docs_with_query_terms_in_window()
        for doc_id, positions in doc_window_positions.items():
            self.inverted_list.add_posting_with_positions(doc_id, positions)
            self.ctf += len(positions)


class OrderedWindowNode(WindowNode):
    def __init__(self, inverted_index, term_nodes, window_size):
        super().__init__(inverted_index, term_nodes, window_size)
        self.get_inverted_list_for_query_terms()
    
    def get_window_start_positions(self, term_positions):
        positions = list()
        print('Getting ordered window positions')

        num_terms = len(term_positions)
        if num_terms == 1:
            return term_positions[0]

        indices = [0] * num_terms
        left = term_positions[0][0]
        prev = left

        cur_word = 1
        while cur_word < num_terms and indices[cur_word] < len(term_positions[cur_word]):
            cur_word_index = indices[cur_word]
            while cur_word_index < len(term_positions[cur_word]) and \
                    term_positions[cur_word][cur_word_index] < prev + self.window_size:
                cur_word_index += 1
            if cur_word_index < len(term_positions[cur_word]):
                # It is either within the window, or has crossed it
                indices[cur_word] = cur_word_index
                if term_positions[cur_word][cur_word_index] - prev <= self.window_size:
                    if cur_word == num_terms - 1:
                        positions.append(left)
                        cur_word = 0
                        indices[cur_word] += 1
                        if indices[cur_word] < len(term_positions[cur_word]):
                            cur_word_index = indices[cur_word]
                            prev = term_positions[cur_word][cur_word_index]
                            left = prev
                            cur_word = 1
                        else:
                            break
                    else:
                        prev = term_positions[cur_word][cur_word_index]
                        cur_word += 1
                else:
                    cur_word -= 1
                    if cur_word == 0:
                        indices[cur_word] += 1
                        if indices[cur_word] < len(term_positions[cur_word]):
                            cur_word_index = indices[cur_word]
                            prev = term_positions[cur_word][cur_word_index]
                            left = prev
                            cur_word = 1
                        else:
                            break
                    else:
                        cur_word_index = indices[cur_word]
                        prev = term_positions[cur_word][cur_word_index]
            else:
                break
        return positions


class UnorderedWindowNode(WindowNode):
    def __init__(self, inverted_index, term_nodes, window_size):
        super().__init__(inverted_index, term_nodes, window_size)
        self.get_inverted_list_for_query_terms()
    
    def get_window_start_positions(self, term_positions):
        positions = list()
        print('Getting unordered window positions')

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
    def __init__(self):
        super().__init__()


class FilterRequire(FilterNode):
    def __init__(self):
        super().__init__()


class FilterReject(FilterNode):
    def __init__(self):
        super().__init__()