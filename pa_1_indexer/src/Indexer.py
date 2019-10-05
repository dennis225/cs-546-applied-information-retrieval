# Import built-in libraries
import os
import pickle
import json
from collections import defaultdict

# Import src files
from InvertedIndex import InvertedIndex


class Indexer:
    def __init__(self, config):
        self.config = config
        self.inverted_index = InvertedIndex()
    
    def load_data(self):
        data_file = '../' + self.config.data_dir + '/' + self.config.data_file_name
        with open(data_file, 'r') as f:
            root, ext = os.path.splitext(data_file)
            # Check if file extension is .json
            if ext == '.json':
                # Load json data from file and return
                return json.load(f)

    def create_inverted_index(self):
        data = self.load_data()
        doc_id = 0
        for scene in data['corpus']:
            doc_id += 1
            scene_text = scene['text']
            # Filter None removes empty strings from the list after the split on space
            terms = list(filter(None, scene_text.split()))
            for position, term in enumerate(terms):
                self.inverted_index.update_map(term, doc_id, position)
        if not self.config.in_memory:
            self.dump_inverted_index_to_disk()
            self.remove_inverted_index_from_memory()
    
    def load_inverted_index_in_memory(self):
        pass
    
    def remove_inverted_index_from_memory(self):
        self.inverted_index.delete_map()
    
    def dump_inverted_index_to_disk(self):
        with open('../' + self.config.index_dir + '/' + self.config.inverted_lists_file_name, 'wb') as f:
            for term, inverted_list in self.inverted_index.get_map().items():
                position_in_file = f.tell()
                inverted_list_binary, size_in_bytes = inverted_list.convert_to_bytearray(self.config.uncompressed)
                f.write(inverted_list_binary)
                self.inverted_index.update_lookup_table(term, position_in_file, size_in_bytes)
        
        with open('../' + self.config.index_dir + '/' + self.config.lookup_table_file_name, 'w') as f:
            json.dump(self.inverted_index.get_lookup_table(), f)
        
        with open('../' + self.config.index_dir + '/' + self.config.config_file_name, 'w') as f:
            json.dump(self.config.get_params(), f)
