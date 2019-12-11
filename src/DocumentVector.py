# Import built-in libraries
import struct
from collections import defaultdict

# Import src files
from Posting import Posting
import utils


class DocumentVector:
    def __init__(self):
        """
        It is a map of key-value pairs for each term and its value calculated
        by a given metric (default is using the scoring function - vector space model)
        """
        self._doc_id = None
        self._doc_vector = defaultdict(float)

    def set_doc_id(self, doc_id):
        self._doc_id = doc_id

    def get_doc_id(self):
        return self._doc_id

    def add_doc_vector_entry(self, term_id, term_value):
        """
        """
        self._doc_vector[term_id] = term_value

    def vector_to_bytearray(self):
        """
        Convert to bytes without delta-encoding
        """
        # Initialize an empty bytearray
        document_vector_binary = bytearray()
        size_in_bytes = 0

        # Convert doc ID to binary using little-endian byte-order and integer format (4 bytes)
        format_doc_id = '<i'
        doc_id_binary = struct.pack(format_doc_id, self._doc_id)
        size_in_bytes += struct.calcsize(format_doc_id)

        document_vector_binary += doc_id_binary

        for term_id, term_value in self._doc_vector.items():
            # Convert term ID to binary using little-endian byte-order and integer format (4 bytes)
            format_term_id = '<i'
            term_id_binary = struct.pack(format_term_id, term_id)
            size_in_bytes += struct.calcsize(format_term_id)

            # Convert term value to binary using little-endian byte-order and float format (8 bytes)
            format_term_value = '<d'
            term_value_binary = struct.pack(format_term_value, term_value)
            size_in_bytes += struct.calcsize(format_term_value)

            document_vector_binary += term_id_binary + term_value_binary

        return (document_vector_binary, size_in_bytes)

    def bytearray_to_vector(self, document_vector_binary, document_vector_size):
        """
        Convert from bytes without delta-encoding
        """
        size_in_bytes = 0

        # Convert binary to doc ID using little-endian byte-order and integer format (4 bytes)
        format_doc_id = '<i'
        self._doc_id = struct.unpack_from(
            format_doc_id, document_vector_binary, size_in_bytes)[0]
        size_in_bytes += struct.calcsize(format_doc_id)

        doc_vector = defaultdict(float)
        while size_in_bytes < document_vector_size:
            # Convert binary to term ID using little-endian byte-order and integer format (4 bytes)
            format_term_id = '<i'
            term_id = struct.unpack_from(format_term_id, document_vector_binary, size_in_bytes)[0]
            size_in_bytes += struct.calcsize(format_term_id)

            # Convert binary to term value using little-endian byte-order and float format (8 bytes)
            format_term_value = '<d'
            term_value = struct.unpack_from(format_term_value, document_vector_binary, size_in_bytes)[0]
            size_in_bytes += struct.calcsize(format_term_value)

            doc_vector[term_id] = term_value
        self._doc_vector = doc_vector

    def get_doc_vector(self):
        return self._doc_vector
