# Import built-in libraries
from collections import defaultdict

# Import src files
from InvertedList import InvertedList


class InvertedIndex:
    def __init__(self):
        self._map = defaultdict(InvertedList)
        self._lookup_table = {}
        self._in_memory = False
    
    def set_in_memory(self, boolean):
        self._in_memory = boolean
    
    def get_map(self):
        return self._map
    
    def delete_map(self):
        self._map = {}
        self.set_in_memory(False)
    
    def update_map(self, term, doc_id, position):
        inverted_list = self._map[term]
        df = inverted_list.add_posting(doc_id, position)
        self.add_to_lookup_table(term, df=df)
    
    def get_lookup_table(self):
        return self._lookup_table
    
    def add_to_lookup_table(self, term, df):
        if term not in self._lookup_table:
            self._lookup_table[term] = {
                'ctf': 1,
                'df': df
            }
        else:
            self._lookup_table[term]['ctf'] += 1
            self._lookup_table[term]['df'] = df
    
    def update_lookup_table(self, term, posting_list_position, posting_list_size):
        self._lookup_table[term]['posting_list_position'] = posting_list_position
        self._lookup_table[term]['posting_list_size'] = posting_list_size
    
    # Returns collection term frequency - number of times the word occurs in the collection
    def get_ctf(self, term):
        return self._lookup_table[term]['ctf']

    # Returns document frequency - number of documents (== postings) in the inverted list
    def get_df(self, term):
        return self._lookup_table[term]['df']
    
    # Returns starting position of the inverted list in the inverted_lists file
    def get_posting_list_position(self, term):
        return self._lookup_table[term]['posting_list_position']
    
    # Set the starting position of the inverted list in the binary inverted list file
    def set_posting_list_position(self, term, position_in_file):
        self._lookup_table[term]['posting_list_position'] = position_in_file
    
    # Returns size of the inverted list in bytes
    def get_posting_list_size(self, term):
        return self._lookup_table[term]['posting_list_size']
    
    # Returns a list of terms in the vocabulary
    def get_vocabulary(self):
        return list(self._lookup_table.keys())
