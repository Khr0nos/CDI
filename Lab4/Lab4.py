# coding=utf-8
"""
Javier Garcia Sanchez
47179375-G
"""
import argparse
import string
from math import ceil

from numpy.lib.scimath import log2


def item(s):
    try:
        par = s.split(",")
        ltr = par[0]
        count = int(par[1])
        return ltr, count
    except:
        raise argparse.ArgumentTypeError("letter dictionary expected")


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


def LZ77_encode(txt, s, t):
    bs = ceil(log2(s + 1)) + ceil(log2(t)) + ceil(log2(alphabet_size(txt)))
    tok = []
    for i in range(len(txt)):
        pass
    return bs, tok


def LZ77_decode(tok):
    pass


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
    with open(dic) as infile:
        pass
    return dicc

def main():
    parser = argparse.ArgumentParser(description="Dictionary coding script")
    parser.add_argument('case', choices=["encode_lz77", "decode_lz77", "encode_lzss", "decode_lzss", "encode_lz78",
                                         "decode_lz78", "encode_lzw", "decode_lzw"], help="option case to be executed",
                        metavar="case")
    parser.add_argument('txt', help="string of characters to be encoded")
    parser.add_argument('-s', type=int, help="offset")
    parser.add_argument('-t', type=int, help="length")
    parser.add_argument('-m', type=int, help="smallest match length lambda")
    parser.add_argument('-dic')
    parser.add_argument('-tok', help="especificar tipus de token segons cada cas")
    args = parser.parse_args()
    case = args.case
    if case == "encode_lz77":
        bs, tok = LZ77_encode(args.txt, args.s, args.t)
        #print bits/symbol i llista de tokens
    elif case == "decode_lz77":
        LZ77_decode(args.tok)
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
