import pickle
from random import random
import string

FULL_STOP = '.?!'
BRACKET_PAIR = {'{': '}', '(': ')', '[': ']', '"': '"', "'": "'", "}": '{', ')': '(', "]": '['}
PUNCT = '.,:;?!'
OPENING_BRACKETS = '{[('
CLOSING_BRACKETS = '}])'


class TextState:
    unary_quote_open: bool = False
    double_quote_open: bool = False
    brackets: list = []
    cap: bool = False
    current_paragraph_size: int = 0
    new_paragraph: bool = False
    current_token_index = 0
    text = ""
    last_tokens = ()
    tokens_list = []
    paragraph_size: int = 100


def can_be_next(token, tokens_number, text):
    if token not in string.punctuation:
        return True
    if text.current_token_index == 0 or text.current_token_index == tokens_number - 2 or \
            (token in PUNCT and text.tokens_list[-1] in PUNCT) or token == '-' or text.tokens_list[-1] == '-':
        return False
    if token in CLOSING_BRACKETS and (len(text.brackets) == 0 or text.brackets[-1] != BRACKET_PAIR[token]
                                      or text.text[-1] in '{[[:;-,'):
        return False
    if token == '"' and (text.double_quote_open and text.brackets[-1] != '"') \
            or text.tokens_list[-1] in '":;-':
        return False
    if token == "'" and (text.unary_quote_open and text.brackets[-1] != "'") or \
            text.tokens_list[-1] in "':;-":
        return False
    return True


def close_brackets(text, new_tokens):
    if text.brackets:
        text.current_token_index += len(text.brackets)
        text.tokens_list += [BRACKET_PAIR[br] for br in reversed(text.brackets)]
        new_tokens += [BRACKET_PAIR[br] for br in reversed(text.brackets)]
        text.brackets.clear()
    return new_tokens


def choose_next_token(probs, text, tokens_number):
    while text.last_tokens not in probs:
        text.last_tokens = text.last_tokens[1:]
    next_token = ""
    while not next_token:
        possible_tokens = dict()
        for token, token_proba in probs[text.last_tokens].items():
            if can_be_next(token, tokens_number, text):
                possible_tokens[token] = token_proba
        if not possible_tokens:
            text.last_tokens = text.last_tokens[1:]
        else:
            thr = random() * sum(possible_tokens.values())
            prob_sum = 0
            for token in possible_tokens.keys():
                prob_sum += possible_tokens[token]
                if prob_sum > thr:
                    return token


def process_quotes(next_token, text):
    if next_token == '"':
        if text.double_quote_open:
            text.brackets = text.brackets[:-1]
        else:
            text.brackets.append(next_token)
    if next_token == "'":
        if text.unary_quote_open:
            text.brackets = text.brackets[:-1]
        else:
            text.brackets.append(next_token)
    return text.brackets


def process_full_stop(text):
    text.cap = True
    if text.current_paragraph_size > text.paragraph_size:
        text.new_paragraph = True
    if text.double_quote_open:
        if text.text[-1].isspace():
            text.text = text.text[:-1]
        text.text += '"'
        text.double_quote_open = not text.double_quote_open
    if text.unary_quote_open:
        if text.text[-1].isspace():
            text.text = text.text[:-1]
        text.text += "'"
        text.unary_quote_open = not text.unary_quote_open


def add_spaces_to_quotes(token, text):
    if token == '"':
        if not text.double_quote_open:
            if not text.text[-1].isspace():
                text.text += " "
        else:
            if text.text[-1].isspace():
                text.text = text.text[:-1]
            token += " "
        text.double_quote_open = not text.double_quote_open
    if token == "'":
        if not text.unary_quote_open:
            if not text.text[-1].isspace():
                text.text += " "
        else:
            if text.text[-1].isspace():
                text.text = text.text[:-1]
            token += " "
        text.unary_quote_open = not text.unary_quote_open
    return token


def add_spaces(new_tokens, text):
    for token in new_tokens:
        if token in FULL_STOP:
            process_full_stop(text)
        if token in PUNCT:
            if text.text[-1].isspace():
                text.text = text.text[:-1]
        elif token == '"' or token == "'":
            token = add_spaces_to_quotes(token, text)
        elif token in OPENING_BRACKETS + '-':
            text.text += " "
        elif token in CLOSING_BRACKETS:
            if text.text[-1].isspace():
                text.text = text.text[:-1]
        elif token[0].isalpha():
            if len(text.tokens_list[text.current_token_index - 1]) > 1 or \
                    text.tokens_list[text.current_token_index - 1].isalpha() or \
                    text.tokens_list[text.current_token_index - 1] in ".,!?:;)]}-":
                if not text.text[-1].isspace():
                    text.text += " "
        text.text += token


def add_token(probs, text, tokens_number):
    new_tokens = []
    if text.current_token_index == 1:
        text.current_paragraph_size += 1
        text.text = text.tokens_list[0].capitalize()
        text.cap = not text.text[0][0].isupper()
    next_token = choose_next_token(probs, text, tokens_number)
    token = next_token
    if token not in string.punctuation and text.cap:
        token = token.capitalize()
        text.cap = False
    if next_token in FULL_STOP:
        new_tokens = close_brackets(text, new_tokens)
    if next_token in CLOSING_BRACKETS:
        text.brackets = text.brackets[:-1]
    if next_token in OPENING_BRACKETS:
        text.brackets.append(next_token)
    text.brackets = process_quotes(next_token, text)
    text.tokens_list.append(next_token)
    new_tokens.append(token)
    if text.current_token_index:
        add_spaces(new_tokens, text)
    text.current_paragraph_size += 1
    if text.new_paragraph:
        text.text += '\n\n'
        text.current_paragraph_size = 0
        text.new_paragraph = False
    return next_token


def get_generated_text(probs, tokens_number, depth, paragraph_size):
    text = TextState()
    text.paragraph_size = paragraph_size
    while len(text.tokens_list) < tokens_number - 1:
        next_token = add_token(probs, text, tokens_number)
        text.current_token_index += 1
        text.last_tokens += tuple(next_token)
        if len(text.last_tokens) > depth - 1:
            text.last_tokens = text.last_tokens[1:]
    text.text += ''.join([BRACKET_PAIR[br] for br in reversed(text.brackets)])
    text.text += '.'
    return text.text


def run_generation(in_file, depth, tokens_number, paragraph_size, out_file=None):
    with open(in_file, 'rb') as in_file:
        probs = pickle.load(in_file)
    text = get_generated_text(probs, tokens_number, depth, paragraph_size)
    if out_file is not None:
        with open(out_file, 'w') as out_file:
            out_file.write(text)
    else:
        print(text)
