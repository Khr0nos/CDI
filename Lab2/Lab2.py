# coding=utf-8
"""
Javier Garcia Sanchez
47179375-G
"""
import string
import sys

from numpy.lib.scimath import log2

def huffman_code(src):
    pass


def shannon_fano_code(src):
    pass


def shannon_code(src):
    pass


def source_extension(src, k):
    k_src = []

    return k_src


def source_fromstring(txt):
    src = []
    length = len(txt) - txt.count(" ")
    for ltr in string.ascii_lowercase:
        count = float(txt.count(ltr))
        if count > 0:
            p = count / length
            src.append((ltr, p))
    return src


def source_fromstring_weights(txt):
    src = []
    for ltr in string.ascii_lowercase:
        count = float(txt.count(ltr))
        if count > 0:
            src.append((ltr, count))
    return src


def entropy_source(src):
    accum = 0.0
    for par in src:
        if par[1] > 0:
            accum += par[1] * log2(1.0 / par[1])
    return accum


def entropy_source_weights(src, l):  #l = suma de tots els pesos
    accum = 0.0
    for par in src:
        if par[1] > 0:
            p = par[1] / l
            accum += p * log2(1.0 / p)
    return accum


def get_source(infile):
    src = []
    for line in infile:
        l = line.split(" ")
        src.append((l[0], float(l[1])))
    return src


def main(case="", input="", aux=""):
    if case == "source":
        if aux == "":
            src = source_fromstring(input)
            print "Source extracted\n" + str(src)
        elif aux == "w":                            #flag "w" vol dir calcular la font amb weights no probabilitats
            src = source_fromstring_weights(input)
            print "Source extracted\n" + str(src)
        elif aux != "" and int(aux) > 0:
            with open(input, 'r') as infile:
                src = get_source(infile)
                k = int(aux)
                src = source_extension(src, k)
                print "Source with " + str(k) + " extension\n" + str(src)
    elif case == "entropy":
        with open(input, 'r') as infile:
            src = get_source(infile)
            if aux != "" and float(aux) > 0:
                print "H(S): " + str(entropy_source_weights(src, float(aux)))
            elif aux == "":
                print "H(S): " + str(entropy_source(src))


if __name__ == '__main__':  # no tocar
    main(*sys.argv[1:])


#quijote_clean.txt as source with length = 1640626
