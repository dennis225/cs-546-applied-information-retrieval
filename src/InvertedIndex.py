# Import built-in libraries
import os
import struct
from collections import defaultdict

# Import src files
from InvertedList import InvertedList


class InvertedIndex:
    """
    Class which exposes APIs to interact with the inverted index
    """

    def __init__(self, config, compressed):
        """
        class config: Instance of the configuration for this index
        bool compressed: Flag to choose between a compressed / uncompressed index
        """
        self.config = config
        self._map = defaultdict(InvertedList)
        self._collection_stats = {
            'totalLength': 0,
            'numberOfDocs': 0,
            'averageLength': 0
        }
        self._docs_meta = {}
        self._lookup_table = {}
        self._vocabulary = []
        self.compressed = compressed
        self.root_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__)))

    def get_collection_stats(self):
        """
        Returns the collection statistics
        """
        return self._collection_stats

    def load_collection_stats(self, collection_stats):
        """
        Loads the collection stats dictionary into the index
        dict collection_stats: Dictionary containing the collection statistics
        """
        self._collection_stats = collection_stats

    def update_collection_stats(self, doc_length=0, average_length=False):
        """
        Updates collection statistics
        int doc_length: Length of the document being added to the inverted index
        bool average_length: Flag to check whether to update the average doc length
        """
        if doc_length:
            self._collection_stats['totalLength'] += doc_length
            self._collection_stats['numberOfDocs'] += 1
        if average_length:
            self._collection_stats['averageLength'] = self._collection_stats['totalLength'] / \
                self._collection_stats['numberOfDocs']

    def get_collection_length(self):
        """
        Returns the total length of all documents in the collection
        """
        return self._collection_stats['totalLength']

    def get_total_docs(self):
        """
        Returns the total number of documents in the collection
        """
        return self._collection_stats['numberOfDocs']

    def get_average_doc_length(self):
        """
        Returns the average length of a document in the collection
        """
        return self._collection_stats['averageLength']

    def get_docs_meta(self):
        """
        Returns the docs meta dictionary
        """
        return self._docs_meta

    def load_docs_meta(self, docs_meta):
        """
        Loads the docs meta dictionary into the index
        dict docs_meta: Dictionary containing the meta info for documents in the dataset
        """
        self._docs_meta = docs_meta

    def update_docs_meta(self, doc_id, doc_meta):
        """
        Adds a new entry to the meta info for documents in the dataset
        int doc_id: ID of the active document
        dict doc_meta: Dictionary of playId, sceneId, sceneNum and sceneLength of the document
        """
        self._docs_meta[str(doc_id)] = doc_meta

    def get_doc_meta(self, doc_id):
        """
        Returns the meta info of the document with the given doc_id
        int doc_id: ID of the document to lookup
        """
        return self._docs_meta[str(doc_id)]

    def get_doc_length(self, doc_id):
        """
        Returns the length of a document with the given doc_id
        int doc_id: ID of the document to lookup
        """
        return self._docs_meta[str(doc_id)]['sceneLength']

    def get_map(self):
        """
        Returns inverted index hash map (term to postings list)
        """
        return self._map

    def load_map(self, index_map):
        """
        Loads a hash map into the index
        dict index_map: Inverted index hash map (term to postings list)
        """
        self._map = index_map

    def delete_map(self):
        """
        Removes the inverted index hash map to free up memory
        """
        self._map = {}

    def update_map(self, term, doc_id, position):
        """
        Add a new {term: postingsList} to the hash map and lookup table
        str term: The term in the document
        int doc_id: ID of the active document
        int position: Position of term in the document
        """
        # Add or update the InvertedList corresponding to the term
        inverted_list = self._map[term]
        inverted_list.add_posting(doc_id, position)
        df = len(inverted_list.get_postings())
        self.add_to_lookup_table(term, df=df)

    def get_lookup_table(self):
        """
        Returns the lookup table from the inverted index
        """
        return self._lookup_table

    def load_lookup_table(self, lookup_table):
        """
        Loads a lookup table in the index
        dict lookup_table: Lookup table to load in the index
        """
        self._lookup_table = lookup_table

    def add_to_lookup_table(self, term, df):
        """
        Adds a new {term: term_info} to the lookup table
        str term: Term to add to the lookup table
        int df: Document Frequency of the term
        """
        if term not in self._lookup_table:
            self._lookup_table[term] = {
                'ctf': 1,
                'df': df
            }
        else:
            self._lookup_table[term]['ctf'] += 1
            self._lookup_table[term]['df'] = df

    def update_lookup_table(self, term, posting_list_position, posting_list_size):
        """
        Modifies the entry for the given term in the lookup table
        str term: Term for which the info is to be modified
        int posting_list_position: Position of the inverted list in the binary file
        int posting_list_size: Size (in bytes) of the inverted list in the binary file
        """
        self._lookup_table[term]['posting_list_position'] = posting_list_position
        self._lookup_table[term]['posting_list_size'] = posting_list_size

    def get_ctf(self, term):
        """
        Returns collection term frequency - number of times the word occurs in the collection
        str term: Term to get the CTF for
        """
        return self._lookup_table[term]['ctf']

    def get_df(self, term):
        """
        Returns document frequency - number of documents (== postings) in the inverted list
        str term: Term to get the DF for
        """
        return self._lookup_table[term]['df']

    def get_posting_list_position(self, term):
        """
        Returns starting position of the inverted list in the inverted_lists file
        str term: Term to get the inverted list position for
        """
        return self._lookup_table[term]['posting_list_position']

    def set_posting_list_position(self, term, position_in_file):
        """
        Sets the starting position of the inverted list in the binary inverted list file
        str term: Term to set the starting position of the inverted list for
        int position_in_file: Starting position of the inverted list in the binary file
        """
        self._lookup_table[term]['posting_list_position'] = position_in_file

    def get_posting_list_size(self, term):
        """
        Returns size of the inverted list in bytes
        str term: Term to get the size of the inverted list for
        """
        return self._lookup_table[term]['posting_list_size']

    def read_inverted_list_from_file(self, inverted_lists_file, posting_list_position, posting_list_size):
        """
        Reads and returns an inverted list from a buffer given starting position and size
        buffer inverted_lists_file: A buffer for the inverted lists file
        int posting_list_position: Position of the inverted list in the binary file
        int posting_list_size: Size of the inverted list in bytes
        """
        inverted_lists_file.seek(posting_list_position)
        inverted_list_binary = bytearray(
            inverted_lists_file.read(posting_list_size))
        return inverted_list_binary

    def get_inverted_list(self, term):
        """
        Returns an inverted list read from the disk for the given term
        str term: Term to get the inverted list for
        """
        if not self.config.in_memory:
            term_stats = self._lookup_table[term]
            dir_name = self.config.uncompressed_dir
            if self.compressed:
                dir_name = self.config.compressed_dir
            with open(self.root_dir + '/' + self.config.index_dir + '/' + dir_name + '/' + self.config.inverted_lists_file_name, 'rb') as inverted_lists_file:
                inverted_list_binary = self.read_inverted_list_from_file(inverted_lists_file, term_stats['posting_list_position'], term_stats['posting_list_size'])
                inverted_list = InvertedList()
                inverted_list.bytearray_to_postings(inverted_list_binary, self.compressed, term_stats['df'])
                return inverted_list
        else:
            return self._map[term]

    def get_prior(self, prior_type, doc_id):
        """
        Returns the prior for a doc with the given doc ID
        str prior_type: Type of the prior to use (currently uniform or random)
        int doc_id: The doc to get the prior for
        """
        with open(self.root_dir + '/' + self.config.index_dir + '/' + prior_type + '_priors', 'rb') as priors_file:
            format_prior = '<d'
            size_in_bytes = struct.calcsize(format_prior)
            position_in_file = doc_id * size_in_bytes
            priors_file.seek(position_in_file)
            prior_binary = bytearray(priors_file.read(size_in_bytes))
            # Convert binary to prior using little-endian byte-order and float format (8 bytes)
            prior = struct.unpack_from(format_prior, prior_binary, 0)[0]
            print(doc_id, prior)
            return prior

    def load_vocabulary(self):
        """
        Loads the vocabulary in the index
        """
        self._vocabulary = list(self._lookup_table.keys())
        self._vocabulary.sort()

    def get_vocabulary(self):
        """
        Returns the vocabulary from the index - a list of terms
        """
        return self._vocabulary
