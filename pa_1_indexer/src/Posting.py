class Posting:
    def __init__(self, doc_id):
        self._doc_id = doc_id
        self._term_positions = []
        self._dtf = 0
    
    def get_doc_id(self):
        return self._doc_id
    
    def get_term_positions(self):
        return self._term_positions
    
    def get_dtf(self):
        return self._dtf

    def update_term_positions(self, position):
        self._term_positions.append(position)
    
    def update_dtf(self):
        self._dtf += 1