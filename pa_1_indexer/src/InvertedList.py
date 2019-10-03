from Posting import Posting


class InvertedList:
    def __init__(self):
        self._postings = []
        self._ctf = 0
    
    # Returns the postings in the inverted list
    def get_postings(self):
        return self._postings
    
    # Returns collection term frequency - number of times the word occurs in the collection
    def get_ctf(self):
        return self._ctf

    # Returns document frequency - number of documents (== postings) in the inverted list
    def get_df(self):
        return len(self._postings)
    
    # Add a new posting to the inverted list
    def add_posting(self, doc_id, position):
        if not len(self._postings) or self._postings[-1].get_doc_id() != doc_id:
            new_posting = Posting(doc_id)
            self._postings.append(new_posting)
        self._postings[-1].update_term_positions(position)
        self._postings[-1].update_dtf()
