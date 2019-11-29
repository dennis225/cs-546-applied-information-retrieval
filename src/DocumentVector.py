# Import built-in libraries
import struct
from collections import defaultdict

# Import src files
from Posting import Posting
import utils


class DocumentVector:
    def __init__(self):
        """
        sparse vector only contains entries for terms present in the document
        It is a map of key-value pairs for each term and its value calculated
        by a given metric (default is using the scoring function - dirichlet)
        """
        self._sparse_vector = defaultdict(float)
    
    def vector_to_bytearray(self):
        """
        Convert to bytes without delta-encoding
        """
        # Initialize an empty bytearray
        sparse_vector_binary = bytearray()
        size_in_bytes = 0
        for term_id, term_value in self._sparse_vector.items():
            # Convert term ID to binary using little-endian byte-order and integer format (4 bytes)
            format_term_id = '<i'
            term_id_binary = struct.pack(format_term_id, term_id)
            size_in_bytes += struct.calcsize(format_term_id)

            # Convert term value to binary using little-endian byte-order and float format (8 bytes)
            format_term_value = '<d'
            term_value_binary = struct.pack(format_term_value, term_value)
            size_in_bytes += struct.calcsize(format_term_value)

            sparse_vector_binary += term_id_binary + term_value_binary
        
        return (sparse_vector_binary, size_in_bytes)

    def bytearray_to_vector(self, sparse_vector_binary, term_count):
        """
        Convert from bytes without delta-encoding
        """
        size_in_bytes = 0
        sparse_vector = defaultdict(float)
        for _ in range(term_count):
            # Convert binary to term ID using little-endian byte-order and integer format (4 bytes)
            format_term_id = '<i'
            term_id = struct.unpack_from(format_term_id, sparse_vector_binary, size_in_bytes)[0]
            size_in_bytes += struct.calcsize(format_term_id)

            # Convert binary to term value using little-endian byte-order and float format (8 bytes)
            format_term_value = '<d'
            term_value = struct.unpack_from(format_term_value, sparse_vector_binary, size_in_bytes)[0]
            size_in_bytes += struct.calcsize(format_term_value)

            sparse_vector[term_id] = term_value
        self._sparse_vector = sparse_vector

    def get_vector(self):
        return self._sparse_vector
