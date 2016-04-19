# coding=utf-8
"""
Javier Garcia Sanchez
47179375-G
"""
import string
import sys
from math import floor

def binary_bits(x, n):
    bits = bin(x).split('b')[1]
    if len(bits) < n:
        bits = '0' * (n - len(bits)) + bits
    return bits


def source_fromstring(txt):
    src = [(ltr, txt.count(ltr)) for ltr in string.ascii_lowercase if txt.count(ltr) > 0]
    src2 = [(ltr, float(txt.count(ltr)) / len(txt)) for ltr in string.ascii_lowercase if txt.count(ltr) > 0]
    return src, src2


def source_fromstring_binary(txt):
    src = [(bit, txt.count(bit)) for bit in ['0', '1']]
    src2 = [(bit, float(txt.count(bit)) / len(txt)) for bit in ['0', '1']]
    return src, src2


def fill(str, char, u):
    return str + (char * u)

def arithmetic_encode(txt, src, k, pi):
    # initialization
    code = []
    alpha = '0' * k
    beta = '1' * k
    u = 0
    for i in range(len(txt)):
        #split into n subintervals
        delta = int(beta, 2) - int(alpha, 2) + 1
        interval = []
        for j in range(1, len(pi)):
            interval.append((int(int(alpha, 2) + floor(delta * pi[j-1])), int(int(alpha, 2) + floor(delta * pi[j] - 1))))
        #update to next subinterval
        it = [src.index(item) for item in src if item[0] == txt[i]][0]
        alpha = binary_bits(interval[it][0], k)
        beta = binary_bits(interval[it][1], k)
        #rescaling
        #print alpha, beta
        while alpha[0] == beta[0]:
            if u > 0:
                if alpha[0] == '0':
                    for x in range(u):
                        code.append('1')
                else:
                    for x in range(u):
                        code.append('0')
                u = 0
            else:
                code.append(alpha[0])
            alpha = alpha[1:]
            beta = beta[1:]
            alpha += '0'
            beta += '1'
        #print alpha, beta
        #underflow prevention
        while alpha[:2] != "00" or beta[:2] != "11":
            alpha = alpha[:1] + alpha[2:] + '0'
            beta = beta[:1] + beta[2:] + '1'
            u += 1
    return code


def arithmetic_decode(bin_code, src, k, l, pi):
    #initialization
    txt = ""
    alpha = '0' * k
    beta = '1' * k
    gamma = ""
    for c in bin_code[:k]:
        gamma += c
    for i in range(l):
        # split into n subintervals
        delta = int(beta, 2) - int(alpha, 2) + 1
        interval = []
        for j in range(1, len(pi)):
            interval.append((int(int(alpha, 2) + floor(delta * pi[j - 1])), int(int(alpha, 2) + floor(delta * pi[j] - 1))))
        #find next letter
        next = int(gamma, 2)
        it = 0
        for j in range(len(interval)):
            if interval[j][0] <= next <= interval[j][1]:
                it = j
                break
        txt += src[it][0]
        alpha = binary_bits(interval[it][0], k)
        beta = binary_bits(interval[it][1], k)
        if len(txt) == l:
            break
        #rescaling

    return txt


def main(case="", txt="", k="", l="", code=""):
    if case == "encode":
        if txt[0] in string.ascii_lowercase:
            src, src2 = source_fromstring(txt)
        else:
            src, src2 = source_fromstring_binary(txt)
        pi = [0]
        acc = 0.0
        for i in range(len(src2)):
            acc += src2[i][1]
            pi.append(acc)
        pi[len(src2)] = 1.0
        # print pi
        with open(txt + "_source.txt", 'w') as output:
            for par in src:
                output.write(str(par[0]) + " " + str(par[1]) + "\n")
                # output.write(str(len(txt)))
        bin_code = arithmetic_encode(txt, src, int(k), pi)        #txt == input string
        print bin_code
    else:
        src = []
        src2 = []
        with open(txt, 'r') as infile:                            #txt == fitxer amb la font
            for line in infile:
                par = line.split(" ")
                src.append((par[0], int(par[1])))
                src2.append((par[0], float(par[1]) / int(l)))
        pi = [0]
        acc = 0.0
        for i in range(len(src2)):
            acc += src2[i][1]
            pi.append(acc)
        pi[len(src2)] = 1.0
        #print src
        #print src2
        code = [c for c in code]
        txt = arithmetic_decode(code, src, int(k), int(l), pi)         #code == bin
        print txt


if __name__ == '__main__':  # no tocar
    main(*sys.argv[1:])
