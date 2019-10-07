class Indexer:
    """
    Class to create, store and load an inverted index
    """
    def __init__(self, new_config):
        """
        Namespace config: Arguments passed on the command line
        """
    
    def get_config(self, params):
        """
        Returns the configuration from the disk (if it exists), otherwise an empty dict
        Namespace params: Configuration params from command line
        """
    
    def load_data(self):
        """
        Loads a data file from the disk for any extension, currently only .json is supported
        """

    def create_inverted_index(self, compressed):
        """
        Creates and returns an inverted index
        bool compressed: Flag to choose between a compressed / uncompressed index
        """
    
    def get_inverted_index(self, compressed):
        """
        Loads an inverted index from file or calls the create method if it doesn't exist
        bool compressed: Flag to choose between a compressed / uncompressed index
        """
    
    def load_inverted_index_in_memory(self, docs_meta_file, lookup_table_file, inverted_lists_file, compressed):
        """
        Loads an inverted index in memory, inverted lists are not loaded by default
        buffer docs_meta_file: Buffer for the docs meta file
        buffer lookup_table_file: Buffer for the lookup table file
        buffer inverted_lists_file: Buffer for the inverted lists file
        """

    def dump_inverted_lists_to_disk(self, file_buffer, inverted_index):
        """
        Stores the inverted lists on disk
        buffer file_buffer: Buffer for the inverted lists file
        class inverted_index: Instance of the inverted index being used
        """
    
    def dump_inverted_index_to_disk(self, inverted_index):
        """
        Stores the docs meta, configuration, lookup table and inverted lists on disk
        class inverted_index: Instance of the inverted index being used
        """
    
    def remove_inverted_index_from_memory(self, inverted_index):
        """
        Removes an inverted index from memory to free up memory
        class inverted_index: Instance of the inverted index being used
        """
