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
        ind = -1
        if not token.isalpha():
            word = ''
            for i in token:
                ind += 1
                if i in string.punctuation and i != '-' and i != "'":
                    if word != '':
                        tokens.append(word)
                        word = ''
                    tokens.append(i)
                else:
                    word += i
            if word != '':
                tokens.append(word)
        else:
            tokens.append(token)
    return tokens


def count_probabilities(tokens, depth):
    appears_count = dict()
    appears_count[''] = defaultdict(int)
    for d in range(depth):
        last = tokens[:d]
        for token in tokens[d:]:
            if d == 0:
                appears_count[''][token] += 1
                continue
            if tuple(last) not in appears_count.keys():
                appears_count[tuple(last)] = defaultdict(float)
            appears_count[tuple(last)][token] += 1
            last.append(token)
            last = last[1:]
    probs = dict()
    for key in appears_count.keys():
        tokens_sum = 0
        if key not in probs.keys():
            probs[key] = dict()
        for token in appears_count[key].keys():
            tokens_sum += appears_count[key][token]
        for token in appears_count[key].keys():
            probs[key][token] = appears_count[key][token] / tokens_sum
    return probs


def run(in_file, out_file, depth):
    tokens = get_tokens(in_file)
    count_probabilities(tokens, depth)
    pickle.dump(count_probabilities(tokens, depth), out_file)
