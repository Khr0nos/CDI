# coding=utf-8
"""
Javier Garcia Sanchez
47179375-G
"""
import math
import operator
import string
import sys
from random import choice

from numpy.lib.scimath import log2

fano_code = []

def huffman_code(src):
    pass



def shannon_fano_code(inici, final):
    n = final - inici + 1
    if n > 1:
        mig = int(n / 2 + inici)
        for i in range(inici, final + 1):
            val = fano_code[i]
            if i < mig:
                fano_code[i] = val[0], val[1], val[2] + '0'
            else:
                fano_code[i] = val[0], val[1], val[2] + '1'
        shannon_fano_code(inici, mig - 1)
        shannon_fano_code(mig, final)


def shannon_code(src):
    code = []
    mean = 0.0
    keys = src.keys()
    for k in keys:
        l = math.ceil(log2(1.0 / src[k]))
        mean += (l * src[k])
        prefix = False
        c = "".join(choice(keys) for i in range(int(l)))
        found = False
        while not found:
            for val in code:
                if val.startswith(c):
                    prefix = True
                    break
            if prefix:
                prefix = False
                c = "".join(choice(keys) for i in range(int(l)))
            else:
                found = True
        code.append(c)
    return code, mean


def source_extension(src, k):
    k_src = {}
    claus = sorted(src.keys())
    if k == 2:
        for i in claus:
            for j in claus:
                k_src[i + j] = src[i] * src[j]
    elif k == 3:
        for i in claus:
            for j in claus:
                for k in claus:
                    k_src[i + j + k] = src[i] * src[j] * src[k]
    elif k == 4:
        for i in claus:
            for j in claus:
                for k in claus:
                    for l in claus:
                        k_src[i + j + k + l] = src[i] * src[j] * src[k] * src[l]
    return k_src


def source_fromstring_binary(txt):
    length = len(txt)
    src = {bit: float(txt.count(bit)) / length for bit in ['0', '1']}
    return src

def source_fromstring(txt):
    length = len(txt) - txt.count(" ")
    src = {ltr: float(txt.count(ltr)) / length for ltr in string.ascii_lowercase if float(txt.count(ltr)) > 0}
    '''src = {}
    length = len(txt) - txt.count(" ")
    for ltr in string.ascii_lowercase:
        count = float(txt.count(ltr))
        if count > 0:
            p = count / length
            src[ltr] = p'''
    return src


def source_fromstring_weights(txt):
    src = {ltr: float(txt.count(ltr)) for ltr in string.ascii_lowercase if float(txt.count(ltr)) > 0}
    '''for ltr in string.ascii_lowercase:
        count = float(txt.count(ltr))
        if count > 0:
            src[ltr] = count'''
    return src


def entropy_source(src):
    accum = 0.0
    for k in sorted(src.keys()):
        if src[k] > 0:
            accum += src[k] * log2(1.0 / src[k])
    return accum


def entropy_source_weights(src, l):  #l = suma de tots els pesos
    accum = 0.0
    for k in sorted(src.keys()):
        if src[k] > 0:
            p = src[k] / l
            accum += p * log2(1.0 / p)
    return accum


def get_source(infile):
    src = {}
    for line in infile:
        l = line.split(" ")
        src[l[0]] = float(l[1])
    return src


def main(case="", input="", aux=""):
    global fano_code
    if case == "source":
        if aux == "":
            src = source_fromstring(input)
            print "Source extracted\n" + str(src)
        elif aux == "w":                            #flag "w" vol dir calcular la font amb weights, no probabilitats
            src = source_fromstring_weights(input)
            print "Source extracted\n" + str(src)
        elif aux != "" and int(aux) > 0:            #k extension >= 2 i <= 4
            #with open(input, 'r') as infile:
            #    src = get_source(infile)
            src = source_fromstring(input)
            k = int(aux)
            src_k = source_extension(src, k)
            print "Source with " + str(k) + " extension\n" + str(src_k)
    elif case == "entropy":
        with open(input, 'r') as infile:
            src = get_source(infile)
            if aux != "" and float(aux) > 0:
                print "H(S): " + str(entropy_source_weights(src, float(aux)))
            elif aux == "":
                print "H(S): " + str(entropy_source(src))
    elif case == "code":
        src = source_fromstring_binary(input)
        if aux == "shannon":
            code, l = shannon_code(source_extension(src, 2))
            print "Shannon code: " + str(code) + " mean length " + str(l)
        elif aux == "fano":
            src = source_extension(src, 2)
            fano_code = sorted(src.items(), key=operator.itemgetter(1), reverse=True)
            for i in range(len(fano_code)):
                fano_code[i] = fano_code[i][0], fano_code[i][1], ''
            shannon_fano_code(0, len(fano_code) - 1)
            print fano_code
            #print "Shannon-Fano code: " + str(code) + " mean length " + str(l)
        elif aux == "huffman":
            pass
            #code, l = huffman_code(src)
            #print "Huffman code: " + str(code) + " mean length " + str(l)
    else:
        print "Usage:\n"
        print "source source_string [w flag per usar weights o be un numero entre 2 i 4 per a calcular k-extensió]"
        print "entropy filepath [numero que representa la longitud del codi font]"
        print "filepath: fitxer amb el codi font com a llista de tuples"
        print "code source_string shannon "
        print "calcula codi Shannon de la 2 extenssió d'una font i la seva longitud promig"


if __name__ == '__main__':  # no tocar
    main(*sys.argv[1:])


#src1_weights.txt as source with length = 1640626
#implementat shannon coding.
#shannon-fano coding implementació inicial, no l'he pogut acabar