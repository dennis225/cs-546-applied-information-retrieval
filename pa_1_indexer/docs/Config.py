class Config:
    """
    Class to create a configuration for the inverted index
    """
    def __init__(self, *args, **kwargs):
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

    def get_params(self):
        """
        Returns a dictionary of the configuration
        """
