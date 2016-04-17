# coding=utf-8
"""
Javier Garcia Sanchez
47179375-G
"""
import string
import sys

def binary_bits(x, n):
    bits = bin(x).split('b')[1]
    return bits * n


def numeric_val(x):
    pass

def source_fromstring(txt):
    src = [(ltr, txt.count(ltr)) for ltr in string.ascii_lowercase if txt.count(ltr) > 0]
    return src


def source_fromstring_binary(txt):
    src = [(bit, txt.count(bit)) for bit in ['0', '1']]
    return src


def arithmetic_encode(txt, src, k):
    c = ""
    code = []
    alpha = binary_bits(0, k)
    beta = binary_bits(1, k)
    alpha_val = int(alpha, 2)
    beta_val = int(beta, 2)
    delta = int(beta, 2) - int(alpha, 2) + 1
    #print delta
    #split into n subintervals
    for i in range(len(txt)):
        pass
    return code


def arithmetic_decode(bin_code, src, k, len):
    return ""


def main(case="", txt="", k="", l="", code=""):
    if txt[0] in string.ascii_lowercase:
        src = source_fromstring(txt)
    else:
        src = source_fromstring_binary(txt)
    #print src
    with open(txt + "_source.txt", 'w') as output:
        for par in src:
            output.write(str(par[0]) + " " + str(par[1]) + "\n")
    if case == "encode":
        bin_code = arithmetic_encode(txt, src, int(k))        #txt == input string
        print bin_code
    else:
        txt = arithmetic_decode(code, src, int(k), l)         #code == bin
        print txt


if __name__ == '__main__':  # no tocar
    main(*sys.argv[1:])
