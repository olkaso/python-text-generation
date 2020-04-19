import pickle
from random import random
import string

fullstop = '.?!'


def get_generated_text(probs, tokens_number, depth):
    text = list()
    last = list()
    brackets = list()
    quote_open = False
    i = 0
    while len(text) < tokens_number - 1:
        while len(last) > 0 and tuple(last) not in probs.keys():
            last = last[1:]
        if len(last) == 0:
            history = ''
        else:
            history = tuple(last)
        max_pr = 0
        next_token = ""
        while next_token == "":
            for token in probs[history].keys():
                pr = probs[history][token] * random()
                if token in string.punctuation:
                    if i == 0 or i == tokens_number-2 or text[-1] in string.punctuation:
                        pr = 0
                    elif token == ')':
                        if len(brackets) == 0 or brackets[-1] != '(':
                            pr = 0
                    elif token == '}':
                        if len(brackets) == 0 or brackets[-1] != '{':
                            pr = 0
                    elif token == ']':
                        if len(brackets) == 0 or brackets[-1] != '[':
                            pr = 0
                    elif token == '"' and quote_open:
                        if brackets[-1] != '"':
                            pr = 0
                if pr > max_pr:
                    max_pr = pr
                    next_token = token
                if next_token == '':
                    history = history[1:]
                if len(history) == 0:
                    history = ""
        bracket_pair = {'{': '}', '(': ')', '[': ']', '"': '"'}
        if next_token in fullstop:
            if len(brackets) > 0:
                i += len(brackets)
                for br in brackets[::-1]:
                    text.append(bracket_pair[br])
                brackets.clear()
                quote_open = False
        if next_token in ')]}':
            brackets = brackets[:-1]
        if next_token in '([{':
            brackets.append(next_token)
        if next_token == '"':
            if quote_open:
                brackets = brackets[:-1]
            else:
                brackets.append(next_token)
            quote_open = not quote_open
        if i == 0 or text[-1] in fullstop:
            assert(next_token != '')
            next_token = next_token.capitalize()
        text.append(next_token)
        i += 1
        last.append(next_token)
        if len(last) > depth - 1:
            last = last[1:]
    text.append('.')
    return text


def run(in_file, depth, tokens_number, out_file=None):
    probs = pickle.load(in_file)
    tokens_list = get_generated_text(probs, tokens_number, depth)
    text = tokens_list[0]
    quote_open = False
    paragraph_size = 0
    new_paragraph = False
    i = 0
    for token in tokens_list[1:]:
        i += 1
        paragraph_size += 1
        if token in fullstop and paragraph_size > 100:
            new_paragraph = True
        if token in fullstop and quote_open:
            text += '"'
            quote_open = not quote_open
        if token in ".,!?:;)]}":
            if text[-1].isspace():
                text = text[:-1]
            token += " "
        elif token == '"':
            if not quote_open:
                text += " "
            else:
                token += " "
            quote_open = not quote_open
        elif token == '-' or token == '—':
            token = " " + token + " "
        elif token in '}])':
            token += " "
        elif token in '({[':
            text += " "
        elif token[0].isalpha():
            if len(tokens_list[i-1]) > 1 or tokens_list[i-1].isalpha():
                text += " "
        text += token
        if new_paragraph:
            text += '\n\n'
            paragraph_size = 0
            new_paragraph = False
    if out_file is not None:
        out_file = open(out_file, 'w')
        out_file.write(text)
        out_file.close()
    else:
        print(text)
