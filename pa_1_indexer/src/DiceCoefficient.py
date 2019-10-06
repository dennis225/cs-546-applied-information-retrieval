class DiceCoefficient:
    def __init__(self, config, inverted_index):
        self.config = config
        self.inverted_index = inverted_index

    def count_consecutive_occurrences(self, postings_a, postings_b):
        n_ab = 0
        a = 0
        b = 0
        while a < len(postings_a) and b < len(postings_b):
            # If doc ID of postings_a is less than doc ID of posting_b, move ahead in posting_a
            if postings_a[a].get_doc_id() < postings_b[b].get_doc_id():
                a += 1
            # If doc ID of postings_b is less than doc ID of posting_a, move ahead in posting_b
            elif postings_b[b].get_doc_id() < postings_a[a].get_doc_id():
                b += 1
            # If doc ID of postings_a is equal to doc ID of posting_b, compare positions in each
            elif postings_a[a].get_doc_id() == postings_b[b].get_doc_id():
                positions_a = postings_a[a].get_term_positions()
                positions_b = postings_b[b].get_term_positions()
                i = 0
                j = 0
                while i < len(positions_a) and j < len(positions_b):
                    # If next position in positions_a is less than positions_b, move ahead in positions_a
                    if positions_a[i] + 1 < positions_b[j]:
                        i += 1
                    # If next position in positions_a is greater than positions_b, move ahead in positions_b
                    elif positions_a[i] + 1 > positions_b[j]:
                        j += 1
                    # If next position in positions_a is equal to positions_b, terms occur consecutively, update n_ab
                    elif positions_a[i] + 1 == positions_b[j]:
                        n_ab += 1
                        i += 1
                        j += 1
                a += 1
                b += 1
        return n_ab

    # Returns count number of top (term, dice_coefficient) pairs
    def calculate_dice_coefficients(self, term, count=1):
        inverted_list_a = self.inverted_index.get_inverted_list(term)
        postings_a = inverted_list_a.get_postings()
        # Number of times term_a occurs in the collection
        n_a = self.inverted_index.get_lookup_table()[term]['ctf']
        dice_coefficients = []
        for term_b in self.inverted_index.get_vocabulary():
            n_b = self.inverted_index.get_ctf(term_b)
            inverted_list_b = self.inverted_index.get_inverted_list(term_b)
            postings_b = inverted_list_b.get_postings()
            n_ab = self.count_consecutive_occurrences(postings_a, postings_b)
            dice_coeff = self.get_dice_coefficient(n_a, n_b, n_ab)
            dice_coefficients.append((term_b, dice_coeff))
        sorted_dice_coefficients = sorted(dice_coefficients, key=lambda x: x[1], reverse=True)
        return sorted_dice_coefficients[:count]
    
    def get_dice_coefficient(self, n_a, n_b, n_ab):
        return n_ab / (n_a + n_b)
