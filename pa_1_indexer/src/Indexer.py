# Import built-in libraries
import json
import os
from collections import defaultdict

# Import src files
from InvertedList import InvertedList


class Indexer:
    def __init__(self, config):
        self.config = config
        self.inverted_index = defaultdict(InvertedList)
    
    def load_data(self):
        with open(self.config.data_file) as f:
            root, ext = os.path.splitext(self.config.data_file)
            # Check if file extension is .json
            if ext == '.json':
                # Load json data from file and return
                return json.load(f)

    def create_index(self):
        data = load_data()
        doc_id = 0
        for scene in data['corpus']:
            doc_id += 1
            scene_text = scene['text']
            # Filter None removes empty strings from the list after the split on space
            terms = list(filter(None, scene_text.split()))
            for position, term in enumerate(terms):
                inverted_list = self.inverted_index[term]
                inverted_list.add_posting(doc_id, position)

    def dump_index_to_disk(self):
        pass

    def dump_vocabulary_to_disk(self):
        pass
