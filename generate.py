import pickle
from random import random
import string

FULL_STOP = '.?!'
BRACKET_PAIR = {'{': '}', '(': ')', '[': ']', '"': '"', "'": "'", "}": '{', ')': '(', "]": '['}
PUNCT = '.,:;?!'
OPENING_BRACKETS = '{[('
CLOSING_BRACKETS = '}])'


def can_be_next(token, current_token, text, tokens_number, brackets, unary_quote_open, double_quote_open):
    if token not in string.punctuation:
        return True
    if current_token == 0 or current_token == tokens_number - 2 or (token in PUNCT and text[-1] in PUNCT) \
            or token == '-' or text[-1] == '-':
        return False
    if token in CLOSING_BRACKETS and (len(brackets) == 0 or brackets[-1] != BRACKET_PAIR[token]
                                      or text[-1] in '{[[:;-'):
        return False
    if token == '"' and (double_quote_open and brackets[-1] != '"') or text[-1] in '":;-':
        return False
    if token == "'" and (unary_quote_open and brackets[-1] != "'") or text[-1] in "':;-":
        return False
    return True


def close_brackets(brackets, current_token, text, new_tokens):
    if brackets:
        current_token += len(brackets)
        text += [BRACKET_PAIR[br] for br in reversed(brackets)]
        new_tokens += [BRACKET_PAIR[br] for br in reversed(brackets)]
        brackets.clear()
    return current_token, text, new_tokens


def choose_next_token(probs, last, current_token, text, tokens_number, brackets, unary_quote_open, double_quote_open):
    while last not in probs:
        last = last[1:]
    next_token = ""
    while not next_token:
        sum = 0
        thr = random()
        for token in probs[last].keys():
            if not can_be_next(token, current_token, text, tokens_number, brackets,
                               unary_quote_open, double_quote_open):
                continue
            sum += probs[last][token]
            if sum > thr:
                next_token = token
                break
        if not next_token:
            last = last[1:]
    return next_token, last


def quotes(next_token, double_quote_open, unary_quote_open, brackets):
    if next_token == '"':
        if double_quote_open:
            brackets = brackets[:-1]
        else:
            brackets.append(next_token)
    if next_token == "'":
        if unary_quote_open:
            brackets = brackets[:-1]
        else:
            brackets.append(next_token)
    return brackets


def spaces(new_tokens, text, paragraph_size, tokens_list, unary_quote_open, double_quote_open, i, cap, new_paragraph):
    for token in new_tokens:
        if token in FULL_STOP:
            cap = True
            if paragraph_size > 100:
                new_paragraph = True
            if double_quote_open:
                if text[-1].isspace():
                    text = text[:-1]
                text += '"'
                double_quote_open = not double_quote_open
            if unary_quote_open:
                if text[-1].isspace():
                    text = text[:-1]
                text += "'"
                unary_quote_open = not unary_quote_open
        if token in PUNCT:
            if text[-1].isspace():
                text = text[:-1]

        elif token == '"':
            if not double_quote_open:
                if not text[-1].isspace():
                    text += " "
            else:
                if text[-1].isspace():
                    text = text[:-1]
                token += " "
            double_quote_open = not double_quote_open
        elif token == "'":
            if not unary_quote_open:
                if not text[-1].isspace():
                    text += " "
            else:
                if text[-1].isspace():
                    text = text[:-1]
                token += " "
            unary_quote_open = not unary_quote_open
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
    return text, unary_quote_open, double_quote_open, cap, new_paragraph


def get_generated_text(probs, tokens_number, depth):
    tokens_list = list()
    last = tuple()
    brackets = list()
    double_quote_open = False
    unary_quote_open = False
    current_token = 0
    paragraph_size = 0
    new_paragraph = False
    cap = False
    text = ""
    while len(tokens_list) < tokens_number - 1:
        new_tokens = []
        if current_token == 1:
            paragraph_size += 1
            text = tokens_list[0].capitalize()
            cap = not text[0][0].isupper()

        next_token, last = choose_next_token(probs, last, current_token, tokens_list,
                                             tokens_number, brackets, unary_quote_open, double_quote_open)
        token = next_token
        if token not in string.punctuation and cap:
            token = token.capitalize()
            cap = False
        if next_token in FULL_STOP:
            current_token, tokens_list, new_tokens = close_brackets(brackets, current_token, tokens_list, new_tokens)
        if next_token in CLOSING_BRACKETS:
            brackets = brackets[:-1]
        if next_token in OPENING_BRACKETS:
            brackets.append(next_token)
        brackets = quotes(next_token, double_quote_open, unary_quote_open, brackets)
        tokens_list.append(next_token)
        new_tokens.append(token)
        if not current_token == 0:
            text, unary_quote_open, double_quote_open, cap, new_paragraph = spaces(new_tokens, text, paragraph_size,
                                                                                   tokens_list, unary_quote_open,
                                                                                   double_quote_open, current_token,
                                                                                   cap, new_paragraph)
        paragraph_size += 1
        if new_paragraph:
            text += '\n\n'
            paragraph_size = 0
            new_paragraph = False
        current_token += 1
        last += tuple(next_token)
        if len(last) > depth - 1:
            last = last[1:]
    text += ''.join([BRACKET_PAIR[br] for br in reversed(brackets)])
    text += '.'
    return text


def run(in_file, depth, tokens_number, out_file=None):
    probs = pickle.load(in_file)
    text = get_generated_text(probs, tokens_number, depth)
    if out_file is not None:
        with open(out_file, 'w') as out_file:
            out_file.write(text)
    else:
        print(text)
