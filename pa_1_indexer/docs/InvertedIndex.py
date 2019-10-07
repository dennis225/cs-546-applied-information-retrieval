class InvertedIndex:
    """
    Class which exposes APIs to interact with the inverted index
    """
    def __init__(self, config, compressed):
        """
        class config: Instance of the configuration for this index
        bool compressed: Flag to choose between a compressed / uncompressed index
        """
    
    def get_docs_meta(self):
        """
        Returns the docs meta dictionary
        """
    
    def load_docs_meta(self, docs_meta):
        """
        Loads the docs meta dictionary into the index
        dict docs_meta: Dictionary containing the meta info for documents in the dataset
        """
    
    def update_docs_meta(self, doc_id, doc_meta):
        """
        Adds a new entry to the meta info for documents in the dataset
        int doc_id: ID of the active document
        dict doc_meta: Dictionary of playId, sceneId, sceneNum and sceneLength of the document
        """
    
    def get_doc_meta(self, doc_id):
        """
        Returns the meta info of the document with the given doc_id
        int doc_id: ID of the active document
        """
    
    def get_map(self):
        """
        Returns inverted index hash map (term to postings list)
        """
    
    def load_map(self, index_map):
        """
        Loads a hash map into the index
        dict index_map: Inverted index hash map (term to postings list)
        """
    
    def delete_map(self):
        """
        Removes the inverted index hash map to free up memory
        """
    
    def update_map(self, term, doc_id, position):
        """
        Add a new {term: postingsList} to the hash map and lookup table
        str term: The term in the document
        int doc_id: ID of the active document
        int position: Position of term in the document
        """
    
    def get_lookup_table(self):
        """
        Returns the lookup table from the inverted index
        """
    
    def load_lookup_table(self, lookup_table):
        """
        Loads a lookup table in the index
        dict lookup_table: Lookup table to load in the index
        """
    
    def add_to_lookup_table(self, term, df):
        """
        Adds a new {term: term_info} to the lookup table
        str term: Term to add to the lookup table
        int df: Document Frequency of the term
        """
    
    def update_lookup_table(self, term, posting_list_position, posting_list_size):
        """
        Modifies the entry for the given term in the lookup table
        str term: Term for which the info is to be modified
        int posting_list_position: Position of the inverted list in the binary file
        int posting_list_size: Size (in bytes) of the inverted list in the binary file
        """
    
    def get_ctf(self, term):
        """
        Returns collection term frequency - number of times the word occurs in the collection
        str term: Term to get the CTF for
        """

    def get_df(self, term):
        """
        Returns document frequency - number of documents (== postings) in the inverted list
        str term: Term to get the DF for
        """
    
    def get_posting_list_position(self, term):
        """
        Returns starting position of the inverted list in the inverted_lists file
        str term: Term to get the inverted list position for
        """
    
    def set_posting_list_position(self, term, position_in_file):
        """
        Sets the starting position of the inverted list in the binary inverted list file
        str term: Term to set the starting position of the inverted list for
        int position_in_file: Starting position of the inverted list in the binary file
        """
    
    def get_posting_list_size(self, term):
        """
        Returns size of the inverted list in bytes
        str term: Term to get the size of the inverted list for
        """
    
    def read_inverted_list_from_file(self, inverted_lists_file, posting_list_position, posting_list_size):
        """
        Reads and returns an inverted list from a buffer given starting position and size
        buffer inverted_lists_file: A buffer for the inverted lists file
        int posting_list_position: Position of the inverted list in the binary file
        int posting_list_size: Size of the inverted list in bytes
        """

    def get_inverted_list(self, term):
        """
        Returns an inverted list read from the disk for the given term
        str term: Term to get the inverted list for
        """
    
    def load_vocabulary(self):
        """
        Loads the vocabulary in the index
        """
    
    # Returns a list of terms in the vocabulary
    def get_vocabulary(self):
        """
        Returns the vocabulary from the index
        """