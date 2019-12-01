class DocumentVector:
    def __init__(self):
        """
        This class defines a map of key-value pairs for each term and its value calculated
        by a given metric (default is using the scoring function - vector space model)
        """
    
    def set_doc_id(self, doc_id):
        """
        Sets the doc ID for this document vector
        """
    
    def get_doc_id(self):
        """
        Returns the doc ID for this document vector
        """
    
    def add_doc_vector_entry(self, term_id, term_value):
        """
        Adds a new term_id, term_value pair to the vector map
        """
    
    def vector_to_bytearray(self):
        """
        Converts the vector map from map to bytes without delta-encoding
        """

    def bytearray_to_vector(self, document_vector_binary, document_vector_size):
        """
        Converts the vector map from bytes to map without delta-encoding
        """

    def get_doc_vector(self):
        """
        Returns the document's vector map
        """
