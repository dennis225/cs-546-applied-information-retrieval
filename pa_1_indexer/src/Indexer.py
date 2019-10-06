# Import built-in libraries
import os
import pickle
import json
from collections import defaultdict

# Import src files
from InvertedList import InvertedList
from InvertedIndex import InvertedIndex


class Indexer:
    def __init__(self, config):
        self.config = config
        self.inverted_index = InvertedIndex(config)
    
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
            doc_meta = {
                'playId': scene['playId'],
                'sceneId': scene['sceneId'],
                'sceneNum': scene['sceneNum'],
                'sceneLength': len(terms)
            }
            self.inverted_index.update_docs_meta(doc_id, doc_meta)
            for position, term in enumerate(terms):
                self.inverted_index.update_map(term, doc_id, position)
        if not self.config.in_memory:
            self.dump_inverted_index_to_disk()
            self.remove_inverted_index_from_memory()
    
    def get_inverted_index(self):
        return self.inverted_index
    
    def load_inverted_index_in_memory(self, lookup_table_file, inverted_lists_file, docs_meta_file):
        # Load lookup table
        lookup_table = json.load(lookup_table_file)
        self.inverted_index.load_lookup_table(lookup_table)

        # Load meta info for documents
        docs_meta = json.load(docs_meta_file)
        self.inverted_index.load_docs_meta(docs_meta)
        
        # Load inverted lists
        index_map = defaultdict(InvertedList)
        for term, term_stats in lookup_table.items():
            inverted_list = index_map[term]
            inverted_list_binary = self.inverted_index.read_inverted_list_from_file(inverted_lists_file, term_stats['posting_list_position'], term_stats['posting_list_size'])
            inverted_list.bytearray_to_postings(inverted_list_binary, self.config.uncompressed, term_stats['df'])
        self.inverted_index.load_map(index_map)
    
    def remove_inverted_index_from_memory(self):
        self.inverted_index.delete_map()
    
    def dump_inverted_index_to_disk(self):
        with open('../' + self.config.index_dir + '/' + self.config.inverted_lists_file_name, 'wb') as f:
            for term, inverted_list in self.inverted_index.get_map().items():
                position_in_file = f.tell()
                inverted_list_binary, size_in_bytes = inverted_list.postings_to_bytearray(self.config.uncompressed)
                f.write(inverted_list_binary)
                self.inverted_index.update_lookup_table(term, position_in_file, size_in_bytes)
        
        with open('../' + self.config.index_dir + '/' + self.config.lookup_table_file_name, 'w') as f:
            json.dump(self.inverted_index.get_lookup_table(), f)
        
        with open('../' + self.config.index_dir + '/' + self.config.config_file_name, 'w') as f:
            json.dump(self.config.get_params(), f)
        
        with open('../' + self.config.index_dir + '/' + self.config.docs_meta_file_name, 'w') as f:
            json.dump(self.inverted_index.get_docs_meta(), f)
