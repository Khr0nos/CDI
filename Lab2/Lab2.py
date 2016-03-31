# coding=utf-8
"""
Javier Garcia Sanchez
47179375-G
"""
import sys

def source_fromstring(string):
    pass

def entropy_source(src):
    pass


def get_source(infile):
    src = []
    for line in infile:
        l = line.split(" ")
        src.append((l[0], float(l[1])))
    return src

def main(case="", input=""):
    if case == "source":
        source_fromstring(input)
    elif case == "entropy":
        with open(input, 'r') as infile:
            src = get_source(infile)
            entropy_source(src)


if __name__ == '__main__':  # no tocar
    main(*sys.argv[1:])
