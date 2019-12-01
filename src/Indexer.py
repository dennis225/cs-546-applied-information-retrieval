# Import built-in libraries
import os
import json
import math
from collections import defaultdict

# Import third-part libraries
import numpy as np

# Import src files
from Config import Config
from InvertedList import InvertedList
from InvertedIndex import InvertedIndex
from DocumentVector import DocumentVector


class Indexer:
    """
    Class to create, store and load an inverted index
    """
    def __init__(self, new_config):
        """
        Namespace config: Arguments passed on the command line
        """
        self.root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        stored_config = self.get_config(new_config)
        stored_config.update(vars(new_config))
        self.config = Config(**stored_config)
    
    def get_config(self, params):
        """
        Returns the configuration from the disk (if it exists), otherwise an empty dict
        Namespace params: Configuration params from command line
        """
        config = {}
        try:
            with open(self.root_dir + '/' + params.index_dir + '/' + params.config_file_name, 'r') as f:
                # Load config from disk
                config = json.load(f)
        except:
            # Return empty dictionary
            config = {}
        
        return config
    
    def load_data(self):
        """
        Loads a data file from the disk for any extension, currently only .json is supported
        """
        data_file = self.root_dir + '/' + self.config.data_dir + '/' + self.config.data_file_name
        with open(data_file, 'r') as f:
            root, ext = os.path.splitext(data_file)
            # Check if file extension is .json
            if ext == '.json':
                # Load json data from file and return
                return json.load(f)

    def create_inverted_index(self, compressed):
        """
        Creates and returns an inverted index
        bool compressed: Flag to choose between a compressed / uncompressed index
        """
        inverted_index = InvertedIndex(self.config, compressed)
        data = self.load_data()
        doc_id = -1
        for scene in data['corpus']:
            doc_id += 1
            scene_text = scene['text']
            # Filter None removes empty strings from the list after the split on space
            terms = list(filter(None, scene_text.split()))
            doc_meta = {
                'playId': scene['playId'],
                'sceneId': scene['sceneId'],
                'sceneNum': scene['sceneNum'],
                'sceneLength': len(terms)
            }
            inverted_index.update_docs_meta(doc_id, doc_meta)
            inverted_index.update_collection_stats(doc_length=doc_meta['sceneLength'])
            for position, term in enumerate(terms):
                inverted_index.update_map(term, doc_id, position)
        inverted_index.update_collection_stats(average_length=True)
        inverted_index.load_vocabulary()
        return inverted_index
    
    def get_inverted_index(self, compressed):
        """
        Loads an inverted index from file or calls the create method if it doesn't exist
        bool compressed: Flag to choose between a compressed / uncompressed index
        """
        inverted_index = None
        try:
            with open(self.root_dir + '/' + self.config.index_dir + '/' + self.config.collection_stats_file_name, 'rb') as collection_stats_file:
                with open(self.root_dir + '/' + self.config.index_dir + '/' + self.config.docs_meta_file_name, 'rb') as docs_meta_file:
                    if not compressed:
                        with open(self.root_dir + '/' + self.config.index_dir + '/' + self.config.uncompressed_dir + '/' + self.config.lookup_table_file_name, 'r') as lookup_table_file:
                            with open(self.root_dir + '/' + self.config.index_dir + '/' + self.config.uncompressed_dir + '/' + self.config.inverted_lists_file_name, 'rb') as inverted_lists_file:
                                # Load lookup table, docs meta info and inverted lists(if in_memory is True) from uncompressed version on disk
                                inverted_index = self.load_inverted_index_in_memory(collection_stats_file, docs_meta_file, lookup_table_file, inverted_lists_file, False)
                    if compressed:
                        with open(self.root_dir + '/' + self.config.index_dir + '/' + self.config.compressed_dir + '/' + self.config.lookup_table_file_name, 'r') as lookup_table_file:
                            with open(self.root_dir + '/' + self.config.index_dir + '/' + self.config.compressed_dir + '/' + self.config.inverted_lists_file_name, 'rb') as inverted_lists_file:
                                # Load lookup table, docs meta info and inverted lists(if in_memory is True) from compressed version on disk
                                inverted_index = self.load_inverted_index_in_memory(collection_stats_file, docs_meta_file, lookup_table_file, inverted_lists_file, True)
        except Exception as e:
            # Create inverted index
            inverted_index = self.create_inverted_index(compressed)
            self.dump_inverted_index_to_disk(inverted_index)
            if not self.config.in_memory:
                self.remove_inverted_index_from_memory(inverted_index)
        
        return inverted_index
    
    def load_inverted_index_in_memory(self, collection_stats_file, docs_meta_file, lookup_table_file, inverted_lists_file, compressed):
        """
        Loads an inverted index in memory, inverted lists are not loaded by default
        buffer collection_stats_file: Buffer for the collection stats file
        buffer docs_meta_file: Buffer for the docs meta file
        buffer lookup_table_file: Buffer for the lookup table file
        buffer inverted_lists_file: Buffer for the inverted lists file
        """
        inverted_index = InvertedIndex(self.config, compressed)

        # Load collection statistics
        collection_stats = json.load(collection_stats_file)
        inverted_index.load_collection_stats(collection_stats)

        # Load meta info for documents
        docs_meta = json.load(docs_meta_file)
        inverted_index.load_docs_meta(docs_meta)

        # Load lookup table
        lookup_table = json.load(lookup_table_file)
        inverted_index.load_lookup_table(lookup_table)

        # Load vocabulary
        inverted_index.load_vocabulary()
        
        # Load inverted lists only if in_memory is True
        if self.config.in_memory:
            index_map = defaultdict(InvertedList)
            for term, term_stats in lookup_table.items():
                inverted_list = index_map[term]
                inverted_list_binary = inverted_index.read_inverted_list_from_file(inverted_lists_file, term_stats['posting_list_position'], term_stats['posting_list_size'])
                inverted_list.bytearray_to_postings(inverted_list_binary, compressed, term_stats['df'])
            inverted_index.load_map(index_map)
        
        return inverted_index
    
    def create_document_vectors(self, inverted_index):
        with open(self.root_dir + '/' + self.config.index_dir + '/' + self.config.document_vectors_file_name, 'wb') as file_buffer:
            data = self.load_data()
            doc_id = -1
            vocabulary = inverted_index.get_vocabulary()
            document_vectors = defaultdict(DocumentVector)
            for scene in data['corpus']:
                doc_id += 1
                document_vector = document_vectors[doc_id]
                document_vector.set_doc_id(doc_id)
                scene_text = scene['text']
                terms = list(filter(None, scene_text.split()))
                # Get the unique terms from the text as we need to calculate score for each term
                unique_terms = set(terms)
                for term in unique_terms:
                    term_id = vocabulary.index(term)
                    # Refer Chapter - 7, page 242 for the calculation below
                    fik = terms.count(term)
                    N = inverted_index.get_total_docs()
                    nk = inverted_index.get_df(term)
                    term_value = 0
                    if fik:
                        term_value = (math.log(fik) + 1) * math.log((N + 1) / (nk + 0.5))
                    # Add an entry with this term_id, term_value pair to the doc vector for this doc
                    document_vector.add_doc_vector_entry(term_id, term_value)
                
                numerator = np.array(list(document_vector.get_doc_vector().values()))
                denominator = np.linalg.norm(numerator)
                normalized_vector = numerator / denominator
                for idx, term_id in enumerate(list(document_vector.get_doc_vector().keys())):
                    normalized_term_value = float(normalized_vector[idx])
                    document_vector.add_doc_vector_entry(term_id, normalized_term_value)
                doc_vector_binary, size_in_bytes = document_vector.vector_to_bytearray()
                position_in_file = file_buffer.tell()
                file_buffer.write(doc_vector_binary)
                doc_meta = inverted_index.get_doc_meta(doc_id)
                doc_meta['document_vector_position'] = position_in_file
                doc_meta['document_vector_size'] = size_in_bytes
                inverted_index.update_docs_meta(doc_id, doc_meta)
        
        with open(self.root_dir + '/' + self.config.index_dir + '/' + self.config.docs_meta_file_name, 'w') as f:
            json.dump(inverted_index.get_docs_meta(), f)
    
    def get_document_vectors(self, inverted_index):
        number_of_docs = inverted_index.get_total_docs()
        document_vectors = defaultdict(DocumentVector)
        with open(self.root_dir + '/' + self.config.index_dir + '/' + self.config.document_vectors_file_name, 'rb') as document_vectors_file:
            for doc_id in range(number_of_docs):
                doc_meta = inverted_index.get_doc_meta(doc_id)
                position_in_file = doc_meta['document_vector_position']
                size_in_bytes = doc_meta['document_vector_size']
                document_vectors_file.seek(position_in_file)
                document_vector = document_vectors[doc_id]
                document_vector.set_doc_id(doc_id)
                document_vector_binary = bytearray(document_vectors_file.read(size_in_bytes))
                document_vector.bytearray_to_vector(document_vector_binary, size_in_bytes)
        return document_vectors

    def dump_inverted_lists_to_disk(self, file_buffer, inverted_index):
        """
        Stores the inverted lists on disk
        buffer file_buffer: Buffer for the inverted lists file
        class inverted_index: Instance of the inverted index being used
        """
        for term, inverted_list in inverted_index.get_map().items():
            position_in_file = file_buffer.tell()
            inverted_list_binary, size_in_bytes = inverted_list.postings_to_bytearray(inverted_index.compressed)
            file_buffer.write(inverted_list_binary)
            inverted_index.update_lookup_table(term, position_in_file, size_in_bytes)
    
    def dump_inverted_index_to_disk(self, inverted_index):
        """
        Stores the docs meta, configuration, lookup table and inverted lists on disk
        class inverted_index: Instance of the inverted index being used
        """
        # Create the index directory if it doesn't exist
        if not os.path.exists(self.root_dir + '/' + self.config.index_dir):
            os.mkdir(self.root_dir + '/' + self.config.index_dir)
        
        if not self.config.compressed:
            # Create uncompressed index directory if it doesn't exist
            if not os.path.exists(self.root_dir + '/' + self.config.index_dir + '/' + self.config.uncompressed_dir):
                os.mkdir(self.root_dir + '/' + self.config.index_dir + '/' + self.config.uncompressed_dir)
            
            with open(self.root_dir + '/' + self.config.index_dir + '/' + self.config.uncompressed_dir + '/' + self.config.inverted_lists_file_name, 'wb') as f:
                self.dump_inverted_lists_to_disk(f, inverted_index)
            
            with open(self.root_dir + '/' + self.config.index_dir + '/' + self.config.uncompressed_dir + '/' + self.config.lookup_table_file_name, 'w') as f:
                json.dump(inverted_index.get_lookup_table(), f)
        
        if self.config.compressed:
            # Create compressed index directory if it doesn't exist
            if not os.path.exists(self.root_dir + '/' + self.config.index_dir + '/' + self.config.compressed_dir):
                    os.mkdir(self.root_dir + '/' + self.config.index_dir + '/' + self.config.compressed_dir)
            
            with open(self.root_dir + '/' + self.config.index_dir + '/' + self.config.compressed_dir + '/' + self.config.inverted_lists_file_name, 'wb') as f:
                self.dump_inverted_lists_to_disk(f, inverted_index)
            
            with open(self.root_dir + '/' + self.config.index_dir + '/' + self.config.compressed_dir + '/' + self.config.lookup_table_file_name, 'w') as f:
                json.dump(inverted_index.get_lookup_table(), f)
        
        with open(self.root_dir + '/' + self.config.index_dir + '/' + self.config.collection_stats_file_name, 'w') as f:
            json.dump(inverted_index.get_collection_stats(), f)

        with open(self.root_dir + '/' + self.config.index_dir + '/' + self.config.docs_meta_file_name, 'w') as f:
            json.dump(inverted_index.get_docs_meta(), f)
        
        with open(self.root_dir + '/' + self.config.index_dir + '/' + self.config.config_file_name, 'w') as f:
            json.dump(self.config.get_params(), f)
    
    def remove_inverted_index_from_memory(self, inverted_index):
        """
        Removes an inverted index from memory to free up memory
        class inverted_index: Instance of the inverted index being used
        """
        inverted_index.delete_map()
