import os


class Config:
    def __init__(
        self,
        data_file_name,
        uncompressed=False,
        in_memory=True,
        retrieval_model='raw_counts',
        data_dir='data',
        index_dir='index',
        config_file_name='config',
        inverted_lists_file_name='inverted_lists',
        lookup_table_file_name='lookup_table',
        docs_meta_file_name='docs_meta'
    ):
        self.data_file_name = data_file_name
        self.uncompressed = uncompressed
        self.in_memory = in_memory
        self.retrieval_model = retrieval_model
        self.data_dir = data_dir
        self.index_dir = index_dir
        self.config_file_name = config_file_name
        self.inverted_lists_file_name = inverted_lists_file_name
        self.lookup_table_file_name = lookup_table_file_name
        self.docs_meta_file_name = docs_meta_file_name
        # Create the index directory if it doesn't exist
        if not os.path.exists('../' + self.index_dir):
            os.mkdir('../' + self.index_dir)

    def get_params(self):
        return {
            'data_file_name': self.data_file_name,
            'uncompressed': self.uncompressed,
            'in_memory': self.in_memory,
            'retrieval_model': self.retrieval_model,
            'data_dir': self.data_dir,
            'index_dir': self.index_dir,
            'config_file_name': self.config_file_name,
            'inverted_lists_file_name': self.inverted_lists_file_name,
            'lookup_table_file_name': self.lookup_table_file_name,
            'docs_meta_file_name': self.docs_meta_file_name
        }
