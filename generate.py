import pickle
from random import random
import string

FULL_STOP = '.?!'
BRACKET_PAIR = {'{': '}', '(': ')', '[': ']', '"': '"', "'": "'", "}": '{', ')': '(', "]": '['}
PUNCT = '.,:;?!'
OPENING_BRACKETS = '{[('
CLOSING_BRACKETS = '}])'


class Sentence:
    unary_quote_open: bool = False
    double_quote_open: bool = False
    brackets: list = []
    cap: bool = False
    paragraph_size: int = 0
    new_paragraph: bool = False


def can_be_next(token, current_token, text, tokens_number, sentence):
    if token not in string.punctuation:
        return True
    if current_token == 0 or current_token == tokens_number - 2 or (token in PUNCT and text[-1] in PUNCT)\
            or token == '-' or text[-1] == '-':
        return False
    if token in CLOSING_BRACKETS and (len(sentence.brackets) == 0 or sentence.brackets[-1] != BRACKET_PAIR[token]
                                      or text[-1] in '{[[:;-,'):
        return False
    if token == '"' and (sentence.double_quote_open and sentence.brackets[-1] != '"') or text[-1] in '":;-':
        return False
    if token == "'" and (sentence.unary_quote_open and sentence.brackets[-1] != "'") or text[-1] in "':;-":
        return False
    return True


def close_brackets(brackets, current_token, text, new_tokens):
    if brackets:
        current_token += len(brackets)
        text += [BRACKET_PAIR[br] for br in reversed(brackets)]
        new_tokens += [BRACKET_PAIR[br] for br in reversed(brackets)]
        brackets.clear()
    return current_token, text, new_tokens


def choose_next_token(probs, last, current_token, text, tokens_number, sentence):
    while last not in probs:
        last = last[1:]
    next_token = ""
    while not next_token:
        possible_tokens = dict()
        for token in probs[last].keys():
            if can_be_next(token, current_token, text, tokens_number, sentence):
                possible_tokens[token] = probs[last][token]
        if not possible_tokens:
            last = last[1:]
        else:
            thr = random()*sum(possible_tokens.values())
            prob_sum = 0
            for token in possible_tokens.keys():
                prob_sum += possible_tokens[token]
                if prob_sum > thr:
                    next_token = token
                    break
    return next_token, last


def process_quotes(next_token, sentence):
    if next_token == '"':
        if sentence.double_quote_open:
            sentence.brackets = sentence.brackets[:-1]
        else:
            sentence.brackets.append(next_token)
    if next_token == "'":
        if sentence.unary_quote_open:
            sentence.brackets = sentence.brackets[:-1]
        else:
            sentence.brackets.append(next_token)
    return sentence.brackets


def process_full_stop(sentence, text):
    sentence.cap = True
    if sentence.paragraph_size > 100:
        sentence.new_paragraph = True
    if sentence.double_quote_open:
        if text[-1].isspace():
            text = text[:-1]
        text += '"'
        sentence.double_quote_open = not sentence.double_quote_open
    if sentence.unary_quote_open:
        if text[-1].isspace():
            text = text[:-1]
        text += "'"
        sentence.unary_quote_open = not sentence.unary_quote_open
    return sentence, text


def add_spaces_to_quotes(text, token, sentence):
    if token == '"':
        if not sentence.double_quote_open:
            if not text[-1].isspace():
                text += " "
        else:
            if text[-1].isspace():
                text = text[:-1]
            token += " "
        sentence.double_quote_open = not sentence.double_quote_open
    if token == "'":
        if not sentence.unary_quote_open:
            if not text[-1].isspace():
                text += " "
        else:
            if text[-1].isspace():
                text = text[:-1]
            token += " "
        sentence.unary_quote_open = not sentence.unary_quote_open
    return text, token, sentence


def add_spaces(new_tokens, text, tokens_list, i, sentence):
    for token in new_tokens:
        if token in FULL_STOP:
            sentence, text = process_full_stop(sentence, text)
        if token in PUNCT:
            if text[-1].isspace():
                text = text[:-1]
        elif token == '"' or token == "'":
            text, token, sentence = add_spaces_to_quotes(text, token, sentence)
        elif token in OPENING_BRACKETS + '-':
            text += " "
        elif token in CLOSING_BRACKETS:
            if text[-1].isspace():
                text = text[:-1]
        elif token[0].isalpha():
            if len(tokens_list[i - 1]) > 1 or tokens_list[i - 1].isalpha() or tokens_list[i - 1] in ".,!?:;)]}-":
                if not text[-1].isspace():
                    text += " "
        text += token
    return text, sentence


def get_generated_text(probs, tokens_number, depth):
    tokens_list = list()
    last = tuple()
    sentence = Sentence()
    current_token = 0
    text = ""
    while len(tokens_list) < tokens_number - 1:
        new_tokens = []
        if current_token == 1:
            sentence.paragraph_size += 1
            text = tokens_list[0].capitalize()
            sentence.cap = not text[0][0].isupper()

        next_token, last = choose_next_token(probs, last, current_token, tokens_list,
                                             tokens_number, sentence)
        token = next_token
        if token not in string.punctuation and sentence.cap:
            token = token.capitalize()
            sentence.cap = False
        if next_token in FULL_STOP:
            current_token, tokens_list, new_tokens = close_brackets(sentence.brackets, current_token,
                                                                    tokens_list, new_tokens)
        if next_token in CLOSING_BRACKETS:
            sentence.brackets = sentence.brackets[:-1]
        if next_token in OPENING_BRACKETS:
            sentence.brackets.append(next_token)
        sentence.brackets = process_quotes(next_token, sentence)
        tokens_list.append(next_token)
        new_tokens.append(token)
        if current_token:
            text, sentence = add_spaces(new_tokens, text, tokens_list, current_token, sentence)
        sentence.paragraph_size += 1
        if sentence.new_paragraph:
            text += '\n\n'
            sentence.paragraph_size = 0
            sentence.new_paragraph = False
        current_token += 1
        last += tuple(next_token)
        if len(last) > depth - 1:
            last = last[1:]
    text += ''.join([BRACKET_PAIR[br] for br in reversed(sentence.brackets)])
    text += '.'
    return text


def run_generation(in_file, depth, tokens_number, out_file=None):
    probs = pickle.load(in_file)
    text = get_generated_text(probs, tokens_number, depth)
    if out_file is not None:
        with open(out_file, 'w') as out_file:
            out_file.write(text)
    else:
        print(text)
