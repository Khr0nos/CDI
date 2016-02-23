# -*- coding: utf-8 -*-
"""
Javier Garcia Sanchez
"""
import re
import sys
import unicodedata
import string

def remove_accents(txt):
    txt = unicode(txt, 'utf-8')
    return ''.join(x for x in unicodedata.normalize('NFKD', txt) if x in string.ascii_letters or x in string.whitespace).lower()


'''def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except NameError:  # unicode is a default on python 3
        pass
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)


def simplify(text):
    text = strip_accents(text.lower())
    text = re.sub('[\n]', ' ', text)
    text = re.sub('[^a-z ]', '', text)
    return text
'''

def clean_txt(txt, prefix):
    txt = remove_accents(txt)
    with open(prefix + "_clean.txt", 'w') as out:
        out.write(txt)


def main(input="", txtname=""):
    if input == "" or txtname == "":
        print("Usage: Lab1.py path/to/txt name_of_text\n")
    else:
        with open(input, 'r') as file:
            txt = file.read()
        clean_txt(txt, txtname)


if __name__ == '__main__':  # no tocar
    main(*sys.argv[1:])
