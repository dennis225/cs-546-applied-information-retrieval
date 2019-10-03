# Import built-in libraries
import argparse

# Import src files
from Config import Config
from Indexer import Indexer


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--uncompressed', default=False, help='Set to True to store uncompressed index, default is False and only compressed index is stored')
    args = parser.parse_args()

    if not args.compressed:
        config = Config(data_file_name='shakespeare-scenes.json', uncompressed=args.uncompressed)
        indexer = Indexer(config)
        indexer.create_index()
        indexer.dump_index_to_disk()