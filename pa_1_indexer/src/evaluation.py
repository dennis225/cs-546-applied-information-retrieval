# Import built-in libraries
import os


if __name__ == '__main__':
    # Create the tests directory if it doesn't exist
    if not os.path.exists('../tests'):
        os.mkdir('../tests')
    
    # Generate 100 queries of 7 words each
    queries = generate_random_queries(vocab, 100, 7)
    
    # Dump 100 queries of 7 words each to disk
    dump_queries_to_disk(queries, '../tests/queries.txt')

    # Read 100 queries of 7 words each from disk
    with open('../tests/queries.txt', 'r') as f:
        queries = f.read().split('\n')
    
    # Generate 100 queries with dice pairs of each of the 7 words - returns 14 word queries
    dice_paired_queries = add_dice_terms_to_random_queries(queries, dice)

    # Dump 14 word queries to disk
    dump_queries_to_disk(dice_paired_queries, '../tests/dice_paired_queries.txt')