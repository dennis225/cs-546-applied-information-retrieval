import struct
from Posting import Posting
import utils


class InvertedList:
    def __init__(self):
        self._postings = []
    
    # Add a new posting to the inverted list
    def add_posting(self, doc_id, position):
        if not len(self._postings) or self._postings[-1].get_doc_id() != doc_id:
            new_posting = Posting(doc_id)
            self._postings.append(new_posting)
        self._postings[-1].update_term_positions(position)
    
    # Converts the inverted list to a bytearray and returns the bytearray
    def postings_to_bytearray(self, compressed):
        # Initialize an empty bytearray
        inverted_list_binary = bytearray()
        size_in_bytes = 0
        if not compressed:
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
                size_in_bytes += struct.calcsize(format_positions)

                inverted_list_binary += doc_id_binary + dtf_binary + positions_binary
        else:
            num_list = []
            previous_doc_id = 0
            for posting in self._postings:
                # Append the delta-encoded doc IDs
                doc_id = posting.get_doc_id()
                num_list.append(doc_id - previous_doc_id)
                
                # Append the dtf next
                dtf = posting.get_dtf()
                num_list.append(dtf)
                
                # Append the delta-encoded positions next
                positions = posting.get_term_positions()
                delta_encoded_postions = utils.delta_encode(positions)
                num_list += delta_encoded_postions
                
                # Update previous doc_id
                previous_doc_id = doc_id
            inverted_list_binary, size_in_bytes = utils.vbyte_encode(num_list)
        return (inverted_list_binary, size_in_bytes)
    
    # Converts the bytearray to a postings list
    def bytearray_to_postings(self, inverted_list_binary, compressed, df):
        # While fetching positions in a document use tuple instead of list - faster than list
        size_in_bytes = 0
        if not compressed:
            # Loop over all postings
            for _ in range(df):
                # Convert binary to document ID using little-endian byte-order and integer format
                format_doc_id = '<i'
                doc_id = struct.unpack_from(format_doc_id, inverted_list_binary, size_in_bytes)[0]
                size_in_bytes += struct.calcsize(format_doc_id)
                
                # Convert binary to document term frequency
                format_dtf = '<i'
                dtf = struct.unpack_from(format_dtf, inverted_list_binary, size_in_bytes)[0]
                size_in_bytes += struct.calcsize(format_dtf)
                
                # Convert binary to term positions
                format_positions = '<' + str(dtf) + 'i'
                positions = list(struct.unpack_from(format_positions, inverted_list_binary, size_in_bytes))
                size_in_bytes += struct.calcsize(format_positions)

                posting = Posting(doc_id)
                posting.set_term_positions(positions)
                self._postings.append(posting)
        else:
            vbyte_decoded_inverted_list = utils.vbyte_decode(inverted_list_binary)
            pointer = 0
            previous_doc_id = 0
            for _ in range(df):
                # Add delta to the previous doc_id to get current doc_id
                delta = vbyte_decoded_inverted_list[pointer]
                doc_id = delta + previous_doc_id
                pointer += 1
                
                # Get dtf
                dtf = vbyte_decoded_inverted_list[pointer]
                pointer += 1
                
                # Get delta-decoded positions
                delta_encoded_positions = vbyte_decoded_inverted_list[pointer: pointer + dtf]
                positions = utils.delta_decode(delta_encoded_positions)
                pointer += dtf
                
                # Create posting
                posting = Posting(doc_id)
                posting.set_term_positions(positions)
                self._postings.append(posting)
                
                # Update previous doc_id
                previous_doc_id = doc_id
    
    # Returns the postings in the inverted list
    def get_postings(self):
        return self._postings
