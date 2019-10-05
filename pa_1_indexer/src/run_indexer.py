# Import built-in libraries
import argparse
import json

# Import src files
from Config import Config
from Indexer import Indexer


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_file_name', default='shakespeare-scenes.json', help='Set the name of the data file to load the data from')
    parser.add_argument('--uncompressed', default=False, help='Set to True to store uncompressed index, by default only compressed index is stored')
    parser.add_argument('--in_memory', default=False, help='Set to True if you want to store the whole index in memory')
    parser.add_argument('--retrieval_model', default='raw_counts', help='Set the type of retrieval model for queries')
    parser.add_argument('--data_dir', default='data', help='Set the name of the data directory')
    parser.add_argument('--index_dir', default='index', help='Set the name of the index directory')
    parser.add_argument('--config_file_name', default='config', help='Set the name of the config file')
    parser.add_argument('--inverted_lists_file_name', default='inverted_lists', help='Set the name of the inverted lists file')
    parser.add_argument('--lookup_table_file_name', default='lookup_table', help='Set the name of the lookup table file')
    args = parser.parse_args()

    if args.uncompressed:
        try:
            with open('../' + args.index_dir + '/' + args.config_file, 'r') as f:
                # Load config params dictionary from disk
                params = json.load(f)
        except:
            # Convert argument namespace to a dictionary
            params = vars(args)
        
        config = Config(**params)
        indexer = Indexer(config)

        try:
            with open('../' + args.index_dir + '/' + args.lookup_table_file_name, 'r') as lookup_table_file:
                with open('../' + args.index_dir + '/' + args.inverted_lists_file_name, 'rb') as inverted_lists_file:
                    # Load lookup table and inverted lists from disk
                    indexer.load_inverted_index_in_memory(lookup_table_file, inverted_lists_file)
        except Exception as e:
            # Create inverted index
            indexer.create_inverted_index()
