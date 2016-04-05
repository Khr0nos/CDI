# coding=utf-8
"""
Javier Garcia Sanchez
47179375-G
"""
import sys
import string

from numpy.lib.scimath import log2


def source_fromstring(txt):
    src = []
    length = len(txt) - txt.count(" ")
    for ltr in string.ascii_lowercase:
        count = float(txt.count(ltr))
        if count > 0:
            p = count / length
        '''else:
            p = 0'''
        src.append((ltr, p))
    return src

'''def info(p):
    return log2(1.0 / p)
'''


def entropy_source(src):
    accum = 0.0
    for par in src:
        if par[1] > 0:
            accum += par[1] * log2(1.0 / par[1])
    return accum


def get_source(infile):
    src = []
    for line in infile:
        l = line.split(" ")
        src.append((l[0], float(l[1])))
    return src


def main(case="", input=""):
    if case == "source":
        src = source_fromstring(input)
        print src
    elif case == "entropy":
        with open(input, 'r') as infile:
            src = get_source(infile)
            print "H(S): " + str(entropy_source(src))


if __name__ == '__main__':  # no tocar
    main(*sys.argv[1:])
