# Import built-in libraries
import os


class Config:
    """
    Class to create a configuration for the inverted index
    """
    def __init__(
        self,
        data_file_name,
        compressed=1,
        in_memory=False,
        retrieval_model='raw_counts',
        data_dir='data',
        index_dir='index',
        compressed_dir='compressed',
        uncompressed_dir='uncompressed',
        config_file_name='config',
        inverted_lists_file_name='inverted_lists',
        lookup_table_file_name='lookup_table',
        docs_meta_file_name='docs_meta',
        collection_stats_file_name='collection_stats'
    ):
        """
        str data_file_name: Name of the data file to build the index from
        int compressed: Flag to check if compressed index is to be used
        int in_memory: Flag to check if index is to be loaded in memory
        str retrieval_model: Scoring model to be used for querying
        str data_dir: Directory where data is stored
        str index_dir: Directory where index is stored
        str compressed_dir: Directory where compressed index is stored
        str uncompressed_dir: Directory where uncompressed is stored
        str config_file_name: Name of the config file on disk
        str inverted_lists_file_name: Name of the inverted lists file on disk
        str lookup_table_file_name: Name of the lookup table file on disk
        str docs_meta_file_name: Name of the docs meta file on disk
        str collection_stats_file_name: Name of the collection stats file on disk
        """
        self.data_file_name = data_file_name
        self.compressed = int(compressed)
        self.in_memory = int(in_memory)
        self.retrieval_model = retrieval_model
        self.data_dir = data_dir
        self.index_dir = index_dir
        self.compressed_dir = compressed_dir
        self.uncompressed_dir = uncompressed_dir
        self.config_file_name = config_file_name
        self.inverted_lists_file_name = inverted_lists_file_name
        self.lookup_table_file_name = lookup_table_file_name
        self.docs_meta_file_name = docs_meta_file_name
        self.collection_stats_file_name = collection_stats_file_name

    def get_params(self):
        """
        Returns a dictionary of the configuration
        """
        return {
            'data_file_name': self.data_file_name,
            'compressed': self.compressed,
            'in_memory': self.in_memory,
            'retrieval_model': self.retrieval_model,
            'data_dir': self.data_dir,
            'index_dir': self.index_dir,
            'compressed_dir': self.compressed_dir,
            'uncompressed_dir': self.uncompressed_dir,
            'config_file_name': self.config_file_name,
            'inverted_lists_file_name': self.inverted_lists_file_name,
            'lookup_table_file_name': self.lookup_table_file_name,
            'docs_meta_file_name': self.docs_meta_file_name,
            'collection_stats_file_name': self.collection_stats_file_name
        }
