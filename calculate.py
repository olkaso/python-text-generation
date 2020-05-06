import pickle
import string
from collections import defaultdict
import re

GOOD_CHARS = '[^a-zA-ZА-Яа-я\s.,:;(){}"?!\'\[\]\-]'


def get_tokens(in_file):
    tokens = list()
    inp = in_file.read()
    inp = re.sub(GOOD_CHARS, '', inp)
    inp = inp.split()
    for token in inp:
        tokens += re.findall(fr"(\w+'\w+|\w+-\w+|\w+|[{string.punctuation}])", token)
    return tokens


def float_dict():
    return defaultdict(float)


def count_probabilities(tokens, depth):
    appears_count = defaultdict(float_dict)
    for token in enumerate(tokens):
        for d in range(depth):
            if d > token[0]:
                continue
            last = tokens[token[0] - d: token[0]]
            appears_count[tuple(last)][token[1]] += 1
    for key in appears_count.keys():
        tokens_sum = sum(appears_count[key].values())
        for token in appears_count[key].keys():
            appears_count[key][token] = appears_count[key][token] / tokens_sum
    return appears_count


def run_calculation(in_file, out_file, depth):
    tokens = get_tokens(in_file)
    pickle.dump(count_probabilities(tokens, depth), out_file)
