# Import built-in libraries
from collections import defaultdict

# Import src files
from InvertedList import InvertedList


class InvertedIndex:
    def __init__(self, config):
        self.config = config
        self._map = defaultdict(InvertedList)
        self._lookup_table = {}
        self._docs_meta = {}
    
    def get_docs_meta(self):
        return self._docs_meta
    
    def load_docs_meta(self, docs_meta):
        self._docs_meta = docs_meta
    
    def update_docs_meta(self, doc_id, doc_meta):
        self._docs_meta[str(doc_id)] = doc_meta
    
    def get_doc_meta(self, doc_id):
        return self._docs_meta[doc_id]
    
    def get_map(self):
        return self._map
    
    def load_map(self, index_map):
        self._map = index_map
    
    def delete_map(self):
        self._map = {}
    
    def update_map(self, term, doc_id, position):
        # Add or update the InvertedList corresponding to the term
        inverted_list = self._map[term]
        inverted_list.add_posting(doc_id, position)
        df = len(inverted_list.get_postings())
        self.add_to_lookup_table(term, df=df)
    
    def get_lookup_table(self):
        return self._lookup_table
    
    def load_lookup_table(self, lookup_table):
        self._lookup_table = lookup_table
    
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
    
    def read_inverted_list_from_file(self, inverted_lists_file, posting_list_position, posting_list_size):
        inverted_lists_file.seek(posting_list_position)
        inverted_list_binary = bytearray(inverted_lists_file.read(posting_list_size))
        return inverted_list_binary

    def get_inverted_list(self, term):
        if not self.config.in_memory:
            term_stats = self._lookup_table[term]
            with open('../' + self.config.index_dir + '/' + self.config.inverted_lists_file_name, 'rb') as inverted_lists_file:
                inverted_list_binary = self.read_inverted_list_from_file(inverted_lists_file, term_stats['posting_list_position'], term_stats['posting_list_size'])
                inverted_list = InvertedList()
                inverted_list.bytearray_to_postings(inverted_list_binary, self.config.uncompressed, term_stats['df'])
                return inverted_list
        else:
            return self._map[term]
    
    # Returns a list of terms in the vocabulary
    def get_vocabulary(self):
        return list(self._lookup_table.keys())
