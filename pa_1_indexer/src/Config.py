import os


class Config:
    def __init__(
        self,
        data_file_name,
        uncompressed=False,
        retrieval_model='raw_counts',
        data_dir='../data',
        index_dir='../index',
        lookup_table_file_name='lookup_table',
        inverted_lists_file_name='inverted_lists',
        config_file_name='config'
    ):
        self.uncompressed = uncompressed
        self.retrieval_model = retrieval_model
        self.data_dir = data_dir
        self.index_dir = index_dir
        self.data_file = self.data_dir + '/' + data_file_name
        self.lookup_table_file_name = lookup_table_file_name
        self.inverted_lists_file_name = inverted_lists_file_name
        self.config_file_name = config_file_name
        # Create the index directory if it doesn't exist
        if not os.path.exists(self.index_dir):
            os.mkdir(self.index_dir)

    def get_params(self):
        return {
            'uncompressed': self.uncompressed,
            'retrieval_model': self.retrieval_model,
            'data_dir': self.data_dir,
            'index_dir': self.index_dir,
            'lookup_table_file_name': self.lookup_table_file_name,
            'inverted_lists_file_name': self.inverted_lists_file_name,
            'config_file_name': self.config_file_name
        }
