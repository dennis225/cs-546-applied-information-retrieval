class Config:
    def __init__(self, data_file_name, uncompressed=False, retrieval_model='raw_counts', data_dir='../data', index_dir='../index'):
        self.uncompressed = uncompressed
        self.retrieval_model = retrieval_model
        self.data_dir = data_dir
        self.index_dir = index_dir
        self.data_file = self.data_dir + '/' + data_file_name