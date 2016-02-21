# -*- coding: utf-8 -*-
"""
Javier Garcia Sanchez
"""
import re
import sys
import unicodedata


def strip_accents(text):
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


def clean_txt(txt, prefix):
    txt = simplify(txt)
    with open(prefix + "_clean.txt", 'w') as out:
        out.write(txt)


def main(input="", filename=""):
    if input == "" or filename == "":
        print("Usage: Lab1.py path/to/txt filename\n")
    else:
        with open(input, 'r') as file:
            txt = file.read()
        clean_txt(txt, filename)


if __name__ == '__main__':  # no tocar
    main(*sys.argv[1:])
