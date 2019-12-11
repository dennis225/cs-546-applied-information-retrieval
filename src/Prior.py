# Import built-in libraries
import math


class Prior:
    def __init__(self, inverted_index):
        self.inverted_index = inverted_index
    
    def create_prior(self, prior_type):
        if prior_type == 'uniform':
            self.create_uniform_prior()
        else:
            self.create_random_prior()
    
    def get_prior(self, prior_type, doc_id):
        if prior_type == 'uniform':
            self.get_uniform_prior(doc_id)
        else:
            self.get_random_prior(doc_id)
    
    def create_uniform_prior(self):
        total_docs = self.inverted_index.get_total_docs()
        prior = math.log(1 / total_docs)
        
        # Initialize an empty bytearray
        uniform_prior_binary = bytearray()
        size_in_bytes = 0
        
        for doc_id in range(total_docs):
            # Convert prior to binary using little-endian byte-order and float format (8 bytes)
            format_prior = '<d'
            prior_binary = struct.pack(format_prior, prior)
            size_in_bytes += struct.calcsize(format_prior)
            
            uniform_prior_binary += prior_binary
    
    def get_uniform_prior(self, doc_id):
        # 
    
    def create_random_prior(self):
        # 
