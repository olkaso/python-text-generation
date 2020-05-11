import pickle
import string
from collections import defaultdict
import re


def get_tokens(in_file):
    inp = in_file.read()
    bad_chars_pattern = r'[^a-zA-ZА-ЯЁа-яё\s.,:;(){}"?!\'\[\]\-]'
    inp = re.sub(bad_chars_pattern, '', inp)
    tokens = re.findall(fr"(\w+'\w+|\w+-\w+|\w+|[{string.punctuation}])", inp)
    return tokens


def make_float_defaultdict():
    return defaultdict(float)


def count_probabilities(tokens_count, depth):
    appears_count = defaultdict(make_float_defaultdict)
    for index, token in enumerate(tokens_count):
        for current_depth in range(depth):
            if current_depth > index:
                continue
            last = tokens_count[index - current_depth: index]
            appears_count[tuple(last)][token] += 1
    for tokens_count in appears_count.values():
        tokens_sum = sum(tokens_count.values())
        for token in tokens_count.keys():
            tokens_count[token] = tokens_count[token] / tokens_sum
    return appears_count


def run_calculation(in_file, out_file, depth):
    with open(in_file) as in_file:
        tokens = get_tokens(in_file)
    with open(out_file, 'wb') as out_file:
        pickle.dump(count_probabilities(tokens, depth), out_file)
