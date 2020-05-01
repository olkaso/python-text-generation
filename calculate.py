import pickle
import string
from collections import defaultdict
import re


def get_tokens(in_file):
    tokens = list()
    inp = in_file.read()
    inp = re.sub(r'[^a-zA-ZА-Яа-я\s.,:;(){}"?!\'\[\]\-]', '', inp)
    inp = inp.split()
    for token in inp:
        tokens += (re.findall(r"(\w+'\w+|\w+-\w+|\w+|.|:|;|[(]|[)]|{|}|\"|[?]|!|'|[|]|-)",  token))
    return tokens


def count_probabilities(tokens, depth):
    appears_count = dict()
    current_token = 0
    for token in tokens:
        for d in range(depth):
            if d > current_token:
                continue
            last = tokens[current_token - d: current_token]
            if tuple(last) not in appears_count:
                appears_count[tuple(last)] = defaultdict(float)
            appears_count[tuple(last)][token] += 1
        current_token += 1
    for key in appears_count.keys():
        tokens_sum = 0
        for token in appears_count[key].keys():
            tokens_sum += appears_count[key][token]
        for token in appears_count[key].keys():
            appears_count[key][token] = appears_count[key][token] / tokens_sum
    return appears_count


def run(in_file, out_file, depth):
    tokens = get_tokens(in_file)
    pickle.dump(count_probabilities(tokens, depth), out_file)
