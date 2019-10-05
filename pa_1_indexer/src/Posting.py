class Posting:
    def __init__(self, doc_id):
        self._doc_id = doc_id
        self._term_positions = []
    
    # Returns the document ID of the posting
    def get_doc_id(self):
        return self._doc_id
    
    # Returns a list of positions of the term in the given document
    def get_term_positions(self):
        return self._term_positions
    
    # Returns the document term frequency - number of times the term occurs in the given document
    def get_dtf(self):
        return len(self._term_positions)

    # Adds to the list the new position where the term occurred in the document
    def update_term_positions(self, position):
        self._term_positions.append(position)