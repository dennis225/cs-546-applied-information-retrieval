# Import built-in libraries
import sys
import random
import struct
from collections import defaultdict


def generate_random_terms_from_vocab(vocab, number_of_terms):
    terms = random.sample(vocab, number_of_terms)
    return terms

def generate_random_queries(index, number_of_queries, terms_per_query):
    queries = []
    vocab = index.get_vocabulary()
    for i in range(number_of_queries):
        terms = generate_random_terms_from_vocab(vocab, terms_per_query)
        query = ' '.join(terms)
        queries.append(query)
    return queries

def create_dice_paired_query(query, dice):
    terms = query.split()
    dice_terms = []
    dice_paired_terms = []
    for term in terms:
        dice_term, dice_coeff = dice.calculate_dice_coefficients(term, count=1)[0]
        dice_terms.append(dice_term)
        dice_paired_terms.append(term)
        dice_paired_terms.append(dice_term)
    dice_paired_query = ' '.join(dice_paired_terms)
    dice_terms_string = ' '.join(dice_terms)
    return (dice_terms_string, dice_paired_query)

def add_dice_terms_to_random_queries(queries, dice):
    dice_paired_queries = []
    dice_terms_strings = []
    for query in queries:
        dice_terms_string, dice_paired_query = create_dice_paired_query(query, dice)
        dice_terms_strings.append(dice_terms_string)
        dice_paired_queries.append(dice_paired_query)
    return (dice_terms_strings, dice_paired_queries)

def dump_strings_to_disk(queries, file):
    with open(file, 'w') as f:
        for query in queries:
            f.write(query)
            f.write('\n')

def compare_indices(index_1, index_2):
    vocab_1 = index_1.get_vocabulary()
    vocab_2 = index_2.get_vocabulary()
    assert len(vocab_1) == len(vocab_2), 'Vocabularies of the indices do not have equal number of terms'

    for i, term in enumerate(vocab_1):
        assert term == vocab_2[i], 'Vocabularies of the indices do not have terms in the same order'
        
        ctf_1 = index_1.get_ctf(term)
        ctf_2 = index_2.get_ctf(term)
        assert ctf_1 == ctf_2, 'Collection Term Frequencies do not match, term: {}, Index 1 has CTF: {} and Index 2 has CTF: {}'.format(term, ctf_1, ctf_2)

        df_1 = index_1.get_df(term)
        df_2 = index_2.get_df(term)
        assert df_1 == df_2, 'Document Frequencies do not match, term: {}, Index 1 has DF: {} and Index 2 has DF: {}'.format(term, df_1, df_2)
    return 'Indices are identical'

def get_data_stats(index):
    plays = defaultdict(int)
    shortest_scene = ('', 0, sys.maxsize)       # Tuple of (sceneId, sceneNum, sceneLength)
    longest_scene = ('', 0, 0)                  # Tuple of (sceneId, sceneNum, sceneLength)
    docs_meta = index.get_docs_meta()
    total_scene_length = 0
    for doc_id, doc_meta in docs_meta.items():
        play_id = doc_meta['playId']
        scene_id = doc_meta['sceneId']
        scene_num = doc_meta['sceneNum']
        scene_length = doc_meta['sceneLength']
        plays[play_id] += scene_length
        total_scene_length += scene_length
        if scene_length <= shortest_scene[2]:
            shortest_scene = (scene_id, scene_num, scene_length)
        if scene_length >= longest_scene[2]:
            longest_scene = (scene_id, scene_num, scene_length)
    average_scene_length = total_scene_length / len(docs_meta.keys())
    plays_list = plays.items()
    sorted_plays_list = sorted(plays_list, key=lambda x: x[1], reverse=True)
    longest_play = sorted_plays_list[0]
    shortest_play = sorted_plays_list[-1]
    return (longest_play, shortest_play, longest_scene, shortest_scene, average_scene_length)

# https://stackoverflow.com/questions/52668295/vbyte-decoder-in-information-retrieval
# https://nlp.stanford.edu/IR-book/html/htmledition/variable-byte-codes-1.html
def vbyte_encode(num_list):
    list_buffer = bytearray()
    size_in_bytes = 0
    for num in num_list:
        while num >= 128:
            list_buffer += struct.pack('<B', num & 0x7f)
            size_in_bytes += struct.calcsize('<B')
            num >>= 7
        list_buffer += struct.pack('<B', num | 0x80)
        size_in_bytes += struct.calcsize('<B')
    return (list_buffer, size_in_bytes)

# https://stackoverflow.com/questions/52668295/vbyte-decoder-in-information-retrieval
# https://nlp.stanford.edu/IR-book/html/htmledition/variable-byte-codes-1.html
def vbyte_decode(list_buffer):
    num_list = []
    i = 0
    while i < len(list_buffer):
        pointer = 0
        byte = list_buffer[i]
        num = byte & 0x7f
        while byte & 0x80 == 0:
            i += 1
            pointer += 1
            byte = list_buffer[i]
            new_byte = byte & 0x7f
            num |= new_byte << (7 * pointer)
        num_list.append(num)
        i += 1
    return num_list

def delta_encode(positions):
    delta_encoded_positions = []
    previous_position = 0
    for position in positions:
        diff = position - previous_position
        delta_encoded_positions.append(diff)
        previous_position = position
    return delta_encoded_positions

def delta_decode(delta_encoded_positions):
    positions = []
    previous_position = 0
    for delta_encoded_position in delta_encoded_positions:
        position = delta_encoded_position + previous_position
        positions.append(position)
        previous_position = position
    return positions

def generate_trecrun_file(filename, query_results):
    with open(filename, 'w') as f:
        for query_result in query_results:
            col1 = query_result['topic_number']
            col2 = 'skip'
            col6 = query_result['run_tag']
            for rank, doc in enumerate(query_result['docs']):
                col3 = doc['sceneId']
                col4 = rank + 1
                col5 = doc['score']
                f.write('{:4} {} {:35} {:4} {:4.4f} {}\n'.format(col1, col2, col3, col4, col5, col6))
