# -*- coding: utf-8 -*-
"""
Javier Garcia Sanchez
"""
import re
import string
import sys
import unicodedata

from numpy.lib.scimath import log2


def total_consecutive(txt):       # total de parells consecutius
    total = 0
    for i in range(0, len(txt) - 1):
        if txt[i] != ' ' and txt[i + 1] != ' ': total += 1
    return total


def count_consecutive(txt, par):  # aparicions de parell "par" en el text
    ret = 0
    for i in range(0, len(txt) - 1):
        if txt[i] == par[0] and txt[i + 1] == par[1]: ret += 1
    return float(ret)


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
            # print l + " " + str(p)
    return accum


def parells():
    p = []
    for i in string.ascii_lowercase:
        for j in string.ascii_lowercase:
            p.append(i + j)
    return p


def joint_entropy(txt):
    total_pairs = total_consecutive(txt)
    accum = 0.0
    pairs = parells()
    for par in pairs:
        count = count_consecutive(txt, par)
        if count > 0:
            p = count / total_pairs
            accum += p * info(p)
            print par + " " + str(p)
    return accum


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
        # print set(txt)       #lletres resultants en el text netejat


#########################################################

def main(case="", input="", txtname=""):
    if case == "clean" and input != "" and txtname != "":
        with open(input, 'r') as file:
            txt = file.read()
        clean_txt(txt, txtname)
    elif case == "entropy" and input != "":
        with open(input, 'r') as file:
            txt = file.read()
        print "H(X): " + str(entropy(txt))
    elif case == "joint_entropy" and input != "":
        with open(input, 'r') as file:
            txt = file.read()
        print "H(X,Y): " + str(joint_entropy(txt))
    else:
        print("Usage:")
        print("Lab1.py clean path/to/originaltxt name_of_text")
        print("Lab1.py entropy path/to/cleantxt")
        print("Lab1.py joint_entropy path/to/cleantxt")


if __name__ == '__main__':  # no tocar
    main(*sys.argv[1:])
