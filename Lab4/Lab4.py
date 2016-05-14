# coding=utf-8
"""
Javier Garcia Sanchez
47179375-G
"""
import argparse
import string
from ast import literal_eval
from math import ceil

from numpy.lib.scimath import log2


# def item(s):
#     try:
#         par = s.split(",")
#         ltr = par[0]
#         count = int(par[1])
#         return ltr, count
#     except:
#         raise argparse.ArgumentTypeError("letter dictionary expected")


def alphabet_size(txt):
    c = 0
    if txt[0] in string.ascii_lowercase:
        for ltr in string.ascii_lowercase:
            if ltr in txt:
                c += 1
    elif txt[0] == '0' or txt[0] == '1':
        c = 2
    else:
        print("alfabet desconegut")
        exit()
    return c


def longest_match(srch, ahead, t):
    l_max = 0
    pos = 0
    window = srch + ahead[:t]
    for i in range(1, t + 1):
        candidat = ahead[:i]
        it = window.find(candidat)
        if it != -1 and it < len(srch) and len(candidat) > l_max:
            l_max = len(candidat)
            pos = it
    n_theta = 0
    if pos >= 0:
        n_theta = len(srch) - pos
    n_lmbda = l_max
    return n_theta, n_lmbda


def LZ77_encode(txt, s, t):
    bs = ceil(log2(s + 1)) + ceil(log2(t)) + ceil(log2(alphabet_size(txt)))
    tok = []
    theta = 0
    lmbda = 0
    tok.append((theta, lmbda, txt[0]))
    srch = txt[:lmbda + 1]
    ahead = txt[lmbda + 1:]
    while ahead != "":
        theta, lmbda = longest_match(srch, ahead, t)
        if lmbda == 0 and theta == 0:
            tok.append((0, 0, ahead[lmbda]))
        if lmbda < len(ahead):
            tok.append((theta, lmbda, ahead[lmbda]))
        elif lmbda == len(ahead):
            tok.append((theta, lmbda, ahead[lmbda - 1]))
        srch += ahead[:lmbda + 1]
        if len(srch) > s:
            left = len(srch) - s
            srch = srch[left:]
        ahead = ahead[lmbda + 1:]
    return bs, tok


def LZ77_decode(tok):
    x = ""
    for i in range(len(tok)):
        if int(tok[i][0]) == 0 and int(tok[i][1]) == 0:
            x += tok[i][2]
        else:
            theta = int(tok[i][0])
            lmbda = int(tok[i][1])
            j = len(x) - theta      #TODO theta pot ser > len(x) compte!!
            pre = x[:j]
            post = x[j:]
            if pre == "":
                x = post + lmbda * tok[i][2]
            # elif :
            #     pass
            else:
                x = pre + lmbda * tok[i][2] + post
    return x

def LZSS_encode(txt, s, t, m):
    pass


def LZSS_decode(tok):
    pass


def LZ78_encode(txt):
    pass


def LZ78_decode(tok):
    pass


def LZW_encode(txt):
    pass


def LZW_decode(dic, tok):
    pass


def get_dict(dic):
    dicc = []
    #todo get dictionary maybe
    return dicc


def main():
    parser = argparse.ArgumentParser(description="Dictionary coding script")
    parser.add_argument('case', choices=["encode_lz77", "decode_lz77", "encode_lzss", "decode_lzss", "encode_lz78",
                                         "decode_lz78", "encode_lzw", "decode_lzw"], help="option case to be executed",
                        metavar="case")
    parser.add_argument('-txt', help="string of characters to be encoded")
    parser.add_argument('-s', type=int, help="maximum offset")
    parser.add_argument('-t', type=int, help="maximum length")
    parser.add_argument('-m', type=int, help="smallest match length lambda")
    parser.add_argument('-dic')
    parser.add_argument('-tok', help="especificar tipus de token segons cada cas")
    args = parser.parse_args()
    case = args.case
    if case == "encode_lz77":
        if args.txt is not None and args.s is not None and args.t is not None:
            bs, tok = LZ77_encode(args.txt, args.s, args.t)
            print(str(bs) + " " + "bits per symbol")
            print("Llista amb " + str(len(tok)) + " tokens:")
            print(tok)
        else:
            print("Falten parametres 's', 't' i/o el text")
    elif case == "decode_lz77":
        tok = literal_eval(input("Entra la llista de tokens tal com dóna la sortida del encoder\n"))
        print(LZ77_decode(tok))
    elif case == "encode_lzss":
        LZSS_encode(args.txt, args.s, args.t, args.m)
    elif case == "decode_lzss":
        LZSS_decode(args.tok)
    elif case == "encode_lz78":
        LZ78_encode(args.txt)
    elif case == "decode_lz78":
        LZ78_decode(args.tok)
    elif case == "encode_lzw":
        LZW_encode(args.txt)
    elif case == "decode_lzw":
        dicc = get_dict(args.dic)
        LZW_decode(args.dic, args.tok)


if __name__ == '__main__':  # no tocar
    main()
