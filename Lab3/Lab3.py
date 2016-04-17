# coding=utf-8
"""
Javier Garcia Sanchez
47179375-G
"""
import string
import sys


def source_fromstring(txt):
    src = {ltr: int(txt.count(ltr)) for ltr in string.ascii_lowercase if int(txt.count(ltr)) > 0}
    return src


def source_fromstring_binary(txt):
    src = {bit: float(txt.count(bit)) for bit in ['0', '1']}
    return src



def arithmetic_encode(str, src, k):
    return []


def arithmetic_decode(bin_code, src, k, len):
    return ""


def main(case="", font="", txt="", k="", l=""):
    if font[0] in string.ascii_lowercase:
        src = source_fromstring(font)
    else:
        src = source_fromstring_binary(font)
    #print src
    if case == "encode":
        bin_code = arithmetic_encode(txt, src, int(k))
        print bin_code
    else:
        txt = arithmetic_decode(bin_code, src, k, l)
        print txt


if __name__ == '__main__':  # no tocar
    main(*sys.argv[1:])
