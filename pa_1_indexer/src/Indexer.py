# Import built-in libraries
import os
import pickle
import json
from collections import defaultdict

# Import src files
from Config import Config
from InvertedList import InvertedList
from InvertedIndex import InvertedIndex


class Indexer:
    def __init__(self, new_config):
        stored_config = self.get_config(new_config)
        stored_config.update(vars(new_config))
        self.config = Config(**stored_config)
    
    def get_config(self, params):
        config = {}
        try:
            with open('../' + params.index_dir + '/' + params.config_file_name, 'r') as f:
                # Load config from disk
                config = json.load(f)
        except:
            # Return empty dictionary
            config = {}
        
        return config
    
    def load_data(self):
        data_file = '../' + self.config.data_dir + '/' + self.config.data_file_name
        with open(data_file, 'r') as f:
            root, ext = os.path.splitext(data_file)
            # Check if file extension is .json
            if ext == '.json':
                # Load json data from file and return
                return json.load(f)

    def create_inverted_index(self, compressed):
        inverted_index = InvertedIndex(self.config, compressed)
        data = self.load_data()
        doc_id = 0
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
            for position, term in enumerate(terms):
                inverted_index.update_map(term, doc_id, position)
        inverted_index.load_vocabulary()
        return inverted_index
    
    def get_inverted_index(self, compressed):
        inverted_index = None
        try:
            with open('../' + self.config.index_dir + '/' + self.config.docs_meta_file_name, 'rb') as docs_meta_file:
                if not compressed:
                    with open('../' + self.config.index_dir + '/' + self.config.uncompressed_dir + '/' + self.config.lookup_table_file_name, 'r') as lookup_table_file:
                        with open('../' + self.config.index_dir + '/' + self.config.uncompressed_dir + '/' + self.config.inverted_lists_file_name, 'rb') as inverted_lists_file:
                            # Load lookup table, docs meta info and inverted lists(if in_memory is True) from uncompressed version on disk
                            inverted_index = self.load_inverted_index_in_memory(docs_meta_file, lookup_table_file, inverted_lists_file, False)
                if compressed:
                    with open('../' + self.config.index_dir + '/' + self.config.compressed_dir + '/' + self.config.lookup_table_file_name, 'r') as lookup_table_file:
                        with open('../' + self.config.index_dir + '/' + self.config.compressed_dir + '/' + self.config.inverted_lists_file_name, 'rb') as inverted_lists_file:
                            # Load lookup table, docs meta info and inverted lists(if in_memory is True) from compressed version on disk
                            inverted_index = self.load_inverted_index_in_memory(docs_meta_file, lookup_table_file, inverted_lists_file, True)
        except Exception as e:
            # Create inverted index
            inverted_index = self.create_inverted_index(compressed)
            self.dump_inverted_index_to_disk(inverted_index)
            if not self.config.in_memory:
                self.remove_inverted_index_from_memory(inverted_index)
        
        return inverted_index
    
    def load_inverted_index_in_memory(self, docs_meta_file, lookup_table_file, inverted_lists_file, compressed):
        inverted_index = InvertedIndex(self.config, compressed)

        # Load meta info for documents
        docs_meta = json.load(docs_meta_file)
        inverted_index.load_docs_meta(docs_meta)

        # Load lookup table
        lookup_table = json.load(lookup_table_file)
        inverted_index.load_lookup_table(lookup_table)

        # Load vocabulary
        inverted_index.load_vocabulary()
        
        # Load inverted lists if in_memory is True
        if self.config.in_memory:
            index_map = defaultdict(InvertedList)
            for term, term_stats in lookup_table.items():
                inverted_list = index_map[term]
                inverted_list_binary = inverted_index.read_inverted_list_from_file(inverted_lists_file, term_stats['posting_list_position'], term_stats['posting_list_size'])
                inverted_list.bytearray_to_postings(inverted_list_binary, compressed, term_stats['df'])
            inverted_index.load_map(index_map)
        
        return inverted_index

    def dump_inverted_lists_to_disk(self, file_buffer, inverted_index):
        for term, inverted_list in inverted_index.get_map().items():
            position_in_file = file_buffer.tell()
            inverted_list_binary, size_in_bytes = inverted_list.postings_to_bytearray(inverted_index.compressed)
            file_buffer.write(inverted_list_binary)
            inverted_index.update_lookup_table(term, position_in_file, size_in_bytes)
    
    def dump_inverted_index_to_disk(self, inverted_index):
        # Create the index directory if it doesn't exist
        if not os.path.exists('../' + self.config.index_dir):
            os.mkdir('../' + self.config.index_dir)
        
        if not self.config.compressed:
            # Create uncompressed index directory if it doesn't exist
            if not os.path.exists('../' + self.config.index_dir + '/' + self.config.uncompressed_dir):
                os.mkdir('../' + self.config.index_dir + '/' + self.config.uncompressed_dir)
            
            with open('../' + self.config.index_dir + '/' + self.config.uncompressed_dir + '/' + self.config.inverted_lists_file_name, 'wb') as f:
                self.dump_inverted_lists_to_disk(f, inverted_index)
            
            with open('../' + self.config.index_dir + '/' + self.config.uncompressed_dir + '/' + self.config.lookup_table_file_name, 'w') as f:
                json.dump(inverted_index.get_lookup_table(), f)
        
        if self.config.compressed:
            # Create compressed index directory if it doesn't exist
            if not os.path.exists('../' + self.config.index_dir + '/' + self.config.compressed_dir):
                    os.mkdir('../' + self.config.index_dir + '/' + self.config.compressed_dir)
            
            with open('../' + self.config.index_dir + '/' + self.config.compressed_dir + '/' + self.config.inverted_lists_file_name, 'wb') as f:
                self.dump_inverted_lists_to_disk(f, inverted_index)
            
            with open('../' + self.config.index_dir + '/' + self.config.compressed_dir + '/' + self.config.lookup_table_file_name, 'w') as f:
                json.dump(inverted_index.get_lookup_table(), f)
        
        with open('../' + self.config.index_dir + '/' + self.config.docs_meta_file_name, 'w') as f:
            json.dump(inverted_index.get_docs_meta(), f)
        
        with open('../' + self.config.index_dir + '/' + self.config.config_file_name, 'w') as f:
            json.dump(self.config.get_params(), f)
    
    def remove_inverted_index_from_memory(self, inverted_index):
        inverted_index.delete_map()
