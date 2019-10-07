class DiceCoefficient:
    """
    Class to expose methods for Dice's Coefficient calculation
    """
    def __init__(self, config, inverted_index):
        """
        class config: Instance of the Config class
        class inverted_index: Instance of the InvertedIndex class
        """

    def count_consecutive_occurrences(self, postings_a, postings_b):
        """
        Returns the number of consecutive occurrences of a pair of words (n_ab)
        list postings_a: List of postings for first word
        list postings_b: List of postings for second word
        """

    def calculate_dice_coefficients(self, term, count=1):
        """
        Returns the top 'count' number of Dice's Doefficients and terms for a term
        str term: Term to find the Dice's Coefficients for
        int count: Number of Dice's Coefficients to find, default is 1 (max Dice)
        """
    
    def get_dice_coefficient(self, n_a, n_b, n_ab):
        """
        Returns the Dice's Coefficient for a term pair
        int n_a: Number of times term_a occurs in the collection
        int n_b: Number of times term_b occurs in the collection
        int n_ab: Number of times term_a and term_b occur consecutively in the collection
        """
