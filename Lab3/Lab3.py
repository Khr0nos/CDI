# coding=utf-8
"""
Javier Garcia Sanchez
47179375-G
"""
import sys
import string


def source_fromstring(txt):
    src = {ltr: int(txt.count(ltr)) for ltr in string.ascii_lowercase if int(txt.count(ltr)) > 0}
    return src






def arithmetic_encode(str, src, k):
    return []


def arithmetic_decode(bin, src, k, len):
    return ""


def main(case="", source="", str="", k="", l=""):
    src = source_fromstring(source)
    if case == "encode":
        bin = arithmetic_encode(str, src, int(k))
        print bin
    else:
        str = arithmetic_decode(bin, src, k, l)
        print str


if __name__ == '__main__':  # no tocar
    main(*sys.argv[1:])
