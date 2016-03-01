# -*- coding: utf-8 -*-
"""
Javier Garcia Sanchez
"""
import re
import string
import sys
import unicodedata

from numpy.lib.scimath import log2


def total_consecutive(txt):                      #total de parells consecutius
    pass

def count_consecutive(txt, par):                 #aparicions de parell "par" en el text
    pass

def count_letter(txt, c):
    ret = sum(l == c for l in txt)
    if ret > 0:
        return float(ret)

def count_total(txt):
    return sum(c != ' ' for c in txt)

def info(p):
    return log2(1.0 / p)

def entropy(txt):
    total_letters = count_total(txt)
    accum = 0.0
    for l in string.ascii_lowercase:
        count = count_letter(txt, l)
        if count > 0:
            p = count / total_letters
            accum += p * info(p)
            #print l + " " + str(p)
    return accum

def joint_entropy(txt):
    pass

#########################################################

def remove_accents(txt):
    return ''.join(
        x for x in unicodedata.normalize('NFKD', txt) if x in string.ascii_letters or x in string.whitespace).lower()


def clean_txt(txt, prefix):
    txt = unicode(txt, 'utf-8')
    txt = re.sub('[Ç]', 'c', txt)
    txt = re.sub('[ç]', 'c', txt)
    txt = remove_accents(txt)
    txt = re.sub('[\r]', '', txt)
    txt = re.sub('[\n]', ' ', txt)
    with open(prefix + "_clean.txt", 'w') as out:
        out.write(txt)
        #print set(txt)       #lletres resultants en el text netejat


#########################################################

def main(case="", input="", txtname=""):
    if case == "clean" and input != "" and txtname != "":
        with open(input, 'r') as file:
            txt = file.read()
        clean_txt(txt, txtname)
    elif case == "entropy" and input != "":
        with open(input, 'r') as file:
            txt = file.read()
        print "H(x): " + str(entropy(txt))
    else:
        print("Usage:")
        print("Lab1.py clean path/to/txt name_of_text")
        print("Lab1.py entropy path/to/txt")


if __name__ == '__main__':  # no tocar
    main(*sys.argv[1:])
