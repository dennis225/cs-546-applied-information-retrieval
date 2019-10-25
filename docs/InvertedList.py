class InvertedList:
    """
    Class which exposes APIs for operation on an inverted list
    """
    def __init__(self):
        """
        Initialize
        """
    
    def add_posting(self, doc_id, position):
        """
        Adds a new posting to the inverted list or modifies it
        int doc_id: ID of the document to be added or modified
        int position: Position of the term in the document
        """
    
    def postings_to_bytearray(self, compressed):
        """
        Converts the inverted list to a bytearray and returns the bytearray
        bool compressed: Flag to choose between a compressed / uncompressed inverted list
        """
    
    def bytearray_to_postings(self, inverted_list_binary, compressed, df):
        """
        Converts the bytearray to a postings list and sets the postings in the inverted list
        buffer inverted_list_binary: A buffer for the inverted list read from disk
        bool compressed: Flag to choose between a compressed / uncompressed inverted list
        int df: Number of documents in the inverted list - Document Frequency
        """
    
    def get_postings(self):
        """
        Returns the list of postings in the inverted list
        """
        return self._postings
