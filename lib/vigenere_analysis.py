import operator
from functools import reduce
from math import gcd

from lib import vigenere
from config import ALPHABET, NGRAM_LENGTH, PLAIN_FILENAME
from lib.utils import sort_dictionary_by_value, sort_dictionary_by_key, print_dict, write_file


def get_ngram_freq(text, ngram_length, min_occurrences=3):
    """ Return all n-grams and their counts in specified text. """

    n = len(text)

    ngrams = dict()

    for i in range(n):
        gram = ''
        for j in range(i, n):
            gram += text[j]
            if gram in ngrams.keys():
                ngrams[gram] += 1
            else:
                ngrams[gram] = 1

    # sorting dictionary
    ngrams = dict(sorted(ngrams.items(), key=operator.itemgetter(1), reverse=True))

    result_dict = dict()

    for i in ngrams:
        if len(i) == ngram_length and ngrams[i] >= min_occurrences:
            result_dict[i] = {'occurrences': ngrams[i]}

    return result_dict


def get_offsets(ngrams, text):
    """ Return offsets between n-grams in specified text. """

    for gram in ngrams:
        offsets = []
        first_occ = text.index(gram)
        for j in range(1, ngrams[gram]['occurrences']):
            next_occ = text.index(gram, first_occ + 1)
            offset = next_occ - first_occ
            offsets.append(offset)
            first_occ = next_occ
        ngrams[gram]['offsets'] = offsets

    return ngrams


def get_gcd(ngrams):
    """ Return the greatest common divider of n-gram's offsets. """
    for gram in ngrams:
        grams_gcd = reduce(gcd, ngrams[gram]['offsets'])
        ngrams[gram]['gcd'] = grams_gcd

    return ngrams


def get_key_length(ngrams):
    """ Return the most possible key length. """
    for v in ngrams.values():
        if v['gcd'] > 2:
            return v['gcd']

    return None


def get_chars_count_dict(column):
    freq_dict = dict.fromkeys(ALPHABET, 0)
    for n in column:
        freq_dict[n] += 1
    return sort_dictionary_by_key(freq_dict)


def get_nth_letters(text, n, offset):
    return text[offset::n]


def get_chars_frequency_dict(chars_count_dict, column_length):
    d = {}
    for i in chars_count_dict:
        d[i] = chars_count_dict[i] / column_length

    return d


def get_index_of_coincidence(chars_count, column_len):
    result = 0

    for i in chars_count:
        result += chars_count[i] * (chars_count[i] - 1)

    result = result / (column_len * (column_len - 1))

    return result


def get_mutual_index_of_coincidence(first_col_char_count, next_col_char_count, first_col_len, next_col_len):
    result = 0

    for i in first_col_char_count:
        result += first_col_char_count[i] * next_col_char_count[i]

    result = result / (first_col_len * next_col_len)

    return result


def divide_text_by_columns(text, columns_count):
    columns = []

    for i in range(columns_count):
        column = get_nth_letters(text, columns_count, i)
        column = column.replace("\n", "")
        columns.append(column)

    return columns


def get_columns_length(columns):
    columns_length = []

    for col in columns:
        columns_length.append(len(col))

    return columns_length


def get_columns_chars_count_list(columns):
    columns_chars_counters = []

    for col in columns:
        char_counts_dict = get_chars_count_dict(col)
        columns_chars_counters.append(char_counts_dict)

    return columns_chars_counters


def get_chars_frequencies_list(columns_chars_count_list, columns_lengths):
    columns_chars_frequencies = []

    for i in range(len(columns_lengths)):
        char_count_dict = columns_chars_count_list[i]
        length = columns_lengths[i]
        char_frequencies_dict = get_chars_frequency_dict(char_count_dict, length)
        columns_chars_frequencies.append(char_frequencies_dict)

    return columns_chars_frequencies


def get_index_of_coincidence_list(chars_counts, lengths):
    indexes = []

    for i in range(0, len(chars_counts)):
        char_count = chars_counts[i]
        column_len = lengths[i]
        index = get_index_of_coincidence(char_count, column_len)
        indexes.append(index)

    return indexes


def get_mutual_index_of_coincidence_list(chars_counts, lengths):
    mutual_indexes = []

    for i in range(1, len(chars_counts)):
        char_count = chars_counts[0]
        column_len = lengths[0]
        char_count2 = chars_counts[i]
        column_len2 = lengths[i]
        mutual_index = get_mutual_index_of_coincidence(char_count, char_count2, column_len, column_len2)
        mutual_indexes.append(mutual_index)

    return mutual_indexes


def get_most_frequent_in_column(chars_frequencies):
    dict_pairs = sort_dictionary_by_value(chars_frequencies).items()
    pairs_iterator = iter(dict_pairs)
    first_pair = next(pairs_iterator)

    return first_pair


def get_most_frequent_list(chars_frequencies_list):
    most_frequent_chars = []
    for chars_freq in chars_frequencies_list:
        pair = get_most_frequent_in_column(chars_freq)
        most_frequent_chars.append(pair)

    return most_frequent_chars


def get_key(most_frequent_chars, key_length):
    key = ''

    for i in range(key_length):
        most_frequent_char = most_frequent_chars[i]
        key += most_frequent_char[0]

    return key


def print_columns_stats(columns, columns_lengths, chars_counts, chars_frequencies):
    print("--------------------------------------------------------------------------")

    for i in range(len(columns)):
        column = columns[i]
        column_len = columns_lengths[i]
        chars_count = chars_counts[i]
        chars_frequency = chars_frequencies[i]

        print(f'Column {i + 1}: {column}')
        print()
        print(f'Column length: {column_len}')
        print()
        print(f'Chars count: {chars_count}')
        print()
        print(f'Chars frequencies: {chars_frequency}')

        print()
        print("--------------------------------------------------------------------------")
        print()


def print_indexes(indexes_of_coincidence, mutual_indexes_of_coincidence, key_length):
    for i in range(key_length):
        index_of_coincidence = indexes_of_coincidence[i]
        print(f'Index of coincidence for {i + 1} column: {index_of_coincidence}')

    print()

    for i in range(key_length - 1):
        mutual_index_of_coincidence = mutual_indexes_of_coincidence[i]
        print(f'Mutual index of coincidence for {i + 1} and {i + 2} columns: {mutual_index_of_coincidence}')

    print()


def print_most_frequent(most_frequent_chars, key_length):
    for i in range(key_length):
        most_frequent_char = most_frequent_chars[i]
        print(f'The most frequent char in {i + 1} column: {most_frequent_char}')

    print()


def analyze_ciphertext(ciphertext):
    print("Analyze ciphertext.. Please wait.")
    print()

    ngrams = get_ngram_freq(ciphertext, NGRAM_LENGTH)
    ngrams = get_offsets(ngrams, ciphertext)
    ngrams = get_gcd(ngrams)

    print(f'List of {NGRAM_LENGTH}-grams:')
    print_dict(ngrams)
    print()

    key_length = get_key_length(ngrams)
    print(f'Key length: {key_length}')
    print()

    columns = divide_text_by_columns(ciphertext, key_length)
    lengths = get_columns_length(columns)
    counts = get_columns_chars_count_list(columns)
    frequencies = get_chars_frequencies_list(counts, lengths)

    indexes_of_coincidence = get_index_of_coincidence_list(counts, lengths)
    mutual_indexes_of_coincidence = get_mutual_index_of_coincidence_list(counts, lengths)

    most_frequent_chars = get_most_frequent_list(frequencies)

    key = get_key(most_frequent_chars, key_length)
    plaintext = vigenere.decrypt(key, ciphertext, ALPHABET)

    print_columns_stats(columns, lengths, counts, frequencies)
    print_indexes(indexes_of_coincidence, mutual_indexes_of_coincidence, key_length)
    print_most_frequent(most_frequent_chars, key_length)

    print()
    print(f'Key={key}')

    write_file(PLAIN_FILENAME, plaintext)

    print()
    print('Plaintext saved into file "plain.txt".')
