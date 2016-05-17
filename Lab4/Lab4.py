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


def LZ77_decode(tok):  # en alguns casos pot donar com a resultat un text decodificat amb l'última lletra repetida
    x = ""
    for i in range(len(tok)):
        if int(tok[i][0]) == 0 and int(tok[i][1]) == 0:
            x += tok[i][2]
        else:
            theta = int(tok[i][0])
            lmbda = int(tok[i][1])
            if theta <= len(x):
                pos = len(x) - theta
                if lmbda <= len(x):
                    word = x[pos:pos + lmbda]
                    x += word + tok[i][2]
                else:
                    count = len(x)
                    for j in range(lmbda):
                        x += x[j % count]
                    x += tok[i][2]
    return x


def LZSS_encode(txt, s, t, m):
    bsa = ceil(log2(alphabet_size(txt)))
    bsn = 1 + ceil(log2(s + 1)) + ceil(log2(t))
    bs = "tokens (0, a) " + str(bsa) + " " + "bits per symbol\n" + "tokens (1, theta, lambda) " + str(
        bsn) + " bits per symbol\n"
    tok = []
    lmbda = 0
    tok.append((0, txt[0]))
    srch = txt[:lmbda + 1]
    ahead = txt[lmbda + 1:]
    while ahead != "":
        theta, lmbda = longest_match(srch, ahead, t)
        if lmbda < m:
            tok.append((0, ahead[0]))
        elif len(ahead) > lmbda >= m:
            tok.append((1, theta, lmbda))
        elif lmbda == len(ahead):
            tok.append((1, theta, lmbda))
        if lmbda == 1:
            srch += ahead[0]
        else:
            srch += ahead[:lmbda + 1]
        if len(srch) > s:
            left = len(srch) - s
            srch = srch[left:]
        if lmbda == 1:
            ahead = ahead[lmbda:]
        else:
            ahead = ahead[lmbda + 1:]
    return bs, tok


def LZSS_decode(tok):
    x = ""
    for i in range(len(tok)):
        if int(tok[i][0]) == 0:
            x += tok[i][1]
        else:
            theta = int(tok[i][1])
            lmbda = int(tok[i][2])
            if theta <= len(x):
                pos = len(x) - theta
                if lmbda <= len(x):
                    word = x[pos:pos + lmbda]
                    x += word
                else:
                    count = len(x)
                    for j in range(lmbda):
                        x += x[j % count]
    return x


def longest_prefix(buffer, dic):
    word = ""
    length = 0
    i = 1
    candidat = buffer[:i]
    while len(candidat) <= len(buffer) and i < len(dic):
        if candidat in dic and len(candidat) > length:
            word = candidat
            length = len(candidat)
        i += 1
        candidat = buffer[:i]
    return word, length


def LZ78_encode(txt):
    bs = ceil(log2(alphabet_size(txt))) + 2**4
    dic_size = 2**4
    dic = ["", txt[0]]
    tok = [(0, txt[0])]
    buffer = txt[1:]
    while buffer != "":
        word, length = longest_prefix(buffer, dic)
        if word not in dic:
            dic.append(word)
            i = dic.index(word)
        elif word == "" or length == 0:
            dic.append(buffer[0])
            i = 0
        else:
            i = dic.index(word)

        if length < len(buffer):
            last = buffer[length]
        else:
            last = buffer[len(buffer) - 1]
        if len(dic) + 1 >= dic_size:
            dic_size *= 2
        tok.append((i, last))
        buffer = buffer[length + 1:]

    #print(dic)
    bs += dic_size
    return bs, tok


def LZ78_decode(tok):
    x = ""
    dic = [""]
    for i in range(len(tok)):
        if tok[i][0] == 0:
            x += tok[i][1]
            dic.append(tok[i][1])
        else:
            x += dic[tok[i][0]] + tok[i][1]
    #print(dic)
    return x


def LZW_encode(txt):
    pass


def LZW_decode(dic, tok):
    pass


def main():
    parser = argparse.ArgumentParser(description="Dictionary coding script")
    parser.add_argument('case', choices=["encode_lz77", "decode_lz77", "encode_lzss", "decode_lzss", "encode_lz78",
                                         "decode_lz78", "encode_lzw", "decode_lzw"], help="option case to be executed",
                        metavar="case")
    parser.add_argument('-txt', help="string of characters to be encoded")
    parser.add_argument('-s', type=int, help="maximum offset")
    parser.add_argument('-t', type=int, help="maximum length")
    parser.add_argument('-m', type=int, help="smallest match length lambda")
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
        if args.txt is not None and args.s is not None and args.t is not None and args.m is not None:
            bs, tok = LZSS_encode(args.txt, args.s, args.t, args.m)
            print(bs)
            print("Llista amb " + str(len(tok)) + " tokens:")
            print(tok)
        else:
            print("Falten parametres 's', 't', 'm' i/o el text")

    elif case == "decode_lzss":
        tok = literal_eval(input("Entra la llista de tokens tal com dóna la sortida del encoder\n"))
        print(LZSS_decode(tok))

    elif case == "encode_lz78":
        if args.txt is not None:
            bs, tok = LZ78_encode(args.txt)
            print(str(bs) + " " + "bits per symbol")
            print("Llista amb " + str(len(tok)) + " tokens:")
            print(tok)
        else:
            print("Falta el text")

    elif case == "decode_lz78":
        tok = literal_eval(input("Entra la llista de tokens tal com dóna la sortida del encoder\n"))
        print(LZ78_decode(tok))

    elif case == "encode_lzw":
        if args.txt is not None:
            LZW_encode(args.txt)
        else:
            print("Falta el text")

    elif case == "decode_lzw":
        tok = literal_eval(input("Entra la llista de tokens tal com dóna la sortida del encoder\n"))
        dic = literal_eval(input("Entra el diccionari tal com dóna la sortida del encoder\n"))
        print(LZW_decode(dic, tok))


'''Els decoders demanen com a input la llista de tokens tal com ve donada pel corresponent encoder,
es a dir, si un encoder mostra per exemple en la sortida: [(0, 's'), (1, 'e')]
hi ha prou amb copiar i enganxar el string per la entrada estàndar quan ho demana el decoder corresponent
'''


if __name__ == '__main__':  # no tocar
    main()
