class Posting:
    """
    Class which exposes APIs for operation on a posting
    """

    def __init__(self, doc_id):
        """
        int doc_id: ID of the document corresponding to this posting
        """
        self._doc_id = doc_id
        self._term_positions = []

    def get_doc_id(self):
        """
        Returns the document ID of the posting
        """
        return self._doc_id

    def get_term_positions(self):
        """
        Returns a list of positions of the term in the given document
        """
        return self._term_positions

    def get_dtf(self):
        """
        Returns the document term frequency - number of times the term occurs in the given document
        """
        return len(self._term_positions)

    def update_term_positions(self, position):
        """
        Adds to the list the new position where the term occurred in the document
        int position: Position to be updated of the term in the document
        """
        self._term_positions.append(position)

    def set_term_positions(self, positions):
        """
        Sets a list of positions of the term in the given document
        """
        self._term_positions = positions
