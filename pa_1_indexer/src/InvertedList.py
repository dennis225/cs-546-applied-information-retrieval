import struct
from Posting import Posting


class InvertedList:
    def __init__(self):
        self._postings = []
    
    # Add a new posting to the inverted list
    def add_posting(self, doc_id, position):
        if not len(self._postings) or self._postings[-1].get_doc_id() != doc_id:
            new_posting = Posting(doc_id)
            self._postings.append(new_posting)
        self._postings[-1].update_term_positions(position)
        return len(self._postings)
    
    # Converts the inverted list to a bytearray and returns the bytearray
    def convert_to_bytearray(self, uncompressed=False):
        # Initialize an empty bytearray
        inverted_list_binary = bytearray()
        size_in_bytes = 0
        if uncompressed:
            for posting in self._postings:
                # Convert document ID to binary using little-endian byte-order and integer format
                format_doc_id = '<i'
                doc_id_binary = struct.pack(format_doc_id, posting.get_doc_id())
                size_in_bytes += struct.calcsize(format_doc_id)
                
                # Convert document term frequency to binary
                format_dtf = '<i'
                dtf_binary = struct.pack(format_dtf, posting.get_dtf())
                size_in_bytes += struct.calcsize(format_dtf)
                
                # Convert term positions to binary
                format_positions = '<' + str(posting.get_dtf()) + 'i'
                positions_binary = struct.pack(format_positions, *posting.get_term_positions())
                inverted_list_binary += doc_id_binary + dtf_binary + positions_binary
                size_in_bytes += struct.calcsize(format_positions)
        else:
            pass
        return (inverted_list_binary, size_in_bytes)
    
    # Returns the postings in the inverted list
    def get_postings(self, uncompressed=False, in_memory=False):
        # While fetching positions in a document use tuple instead of list - faster than list
        if not in_memory:
            if uncompressed:
                pass
            else:
                pass
        return self._postings
