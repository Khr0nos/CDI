# -*- coding: utf-8 -*-
"""
Javier Garcia Sanchez
"""
import random as rng
import re
import string
import sys
import unicodedata

from numpy.lib.scimath import log2


# region auxiliars
def pars(txt):
    pairs = []
    for i in range(0, len(txt) - 1):
        pairs.append(txt[i] + txt[i + 1])
    return pairs


def total_consecutive(txt):       # total de parells consecutius
    total = 0
    for i in range(0, len(txt) - 1):
        if txt[i] != ' ' and txt[i + 1] != ' ': total += 1
    return total


def count_consecutive(txt, par):  # aparicions de parell "par" en el text
    ret = 0
    for i in range(0, len(txt) - 1):
        if txt[i] == par[0] and txt[i + 1] == par[1]: ret += 1
    return float(ret)


def count_total(txt):
    return len(txt) - txt.count(' ')
    #return sum(c != ' ' for c in txt)
# endregion


# region entropy
def info(p):
    return log2(1.0 / p)


def entropy(txt):
    total_letters = count_total(txt)
    accum = 0.0
    for l in string.ascii_lowercase:
        count = float(txt.count(l))
        if count > 0:
            p = count / total_letters
            accum += p * info(p)
            print l + " " + str(p)
    return accum
# endregion


# region joint entropy
def parells():
    p = []
    for i in string.ascii_lowercase:
        for j in string.ascii_lowercase:
            p.append(i + j)
    return p


def joint_entropy(txt):
    total_pairs = total_consecutive(txt)
    accum = 0.0
    pairs = parells()
    for par in pairs:
        count = count_consecutive(txt, par)
        if count > 0:
            p = count / total_pairs
            accum += p * info(p)
            print par + " " + str(p)
    return accum
# endregion


# region conditional entropy
def after_letter(txt, ltr, i):
    par = ltr + i
    ret = count_consecutive(txt, par) / total_consecutive(txt)
    if ret > 0:
        return ret
    else:
        return 0


def conditional_entropy1(txt, ltr):
    if ltr == "espai":
        count = float(txt.count(" "))
        if count > 0:
            p_ltr = count / len(txt)
        else:
            print("Specify an existing letter in text")
            return "Not found"
    else:
        count = float(txt.count(ltr))
        if count > 0:
            p_ltr = count / count_total(txt)
        else:
            print("Specify an existing letter in text")
            return "Not found"
    accum = 0.0
    for i in string.ascii_lowercase:
        p_Y_x = after_letter(txt, ltr, i)
        if p_Y_x > 0:
            p_con = p_Y_x / p_ltr
            accum += p_con * info(p_con)
    return accum


def conditional_entropy(txt):
    total_pairs = total_consecutive(txt)
    letters = count_total(txt)
    accum = 0.0
    for i in string.ascii_lowercase:                 #lletra X
        for j in string.ascii_lowercase:             #lletra Y
            count = count_consecutive(txt, i + j)
            #print i + j + str(count)
            if count > 0:
                p_x_y = count / total_pairs
                p_x = float(txt.count(i)) / letters
                p_con = p_x_y / p_x
                accum += p_x_y * info(p_con)
    return accum


'''
def conditional_entropy(txt):
    letters = count_total(txt)
    accum = 0.0
    for i in string.ascii_lowercase:                 #lletra X
        for j in string.ascii_lowercase:             #lletra Y
            count = count_consecutive(txt, i + j)
            if count > 0:
                p_x = float(txt.count(i)) / letters
                accum += p_x * conditional_entropy1(txt, i)
    return accum
'''
# endregion


# region text cleaning
def remove_accents(txt):
    return ''.join(
        x for x in unicodedata.normalize('NFKD', txt) if x in string.ascii_letters or x in string.whitespace).lower()


def clean_txt(txt, prefix):
    txt = unicode(txt, 'utf-8')
    txt = re.sub('[Ç]', 'c', txt)
    txt = re.sub('[ç]', 'c', txt)
    txt = remove_accents(txt)
    txt = re.sub('[\r]', '', txt)
    txt = re.sub('[\n]', ' ', txt)
    txt = re.sub(' +', ' ', txt)
    with open(prefix + "_clean.txt", 'w') as out:
        out.write(txt)
        # print set(txt)       #lletres resultants en el text netejat
# endregion


# region text generation
def new_text(nom, txt):
    nou = ""
    for i in range(0, len(txt)):
        nou += rng.choice(txt)
    nou = re.sub(' +', ' ', nou)
    with open(nom + ".txt", 'w') as text:
        text.write(nou)
    print "New text entropy: " + str(entropy(nou))

def new_text_joint(nom, txt):   #todo seleccionar parells del text directament?
    nou = ""
    pairs = pars(txt)
    length = len(txt) / 2
    for i in range(0, length):
        nou += rng.choice(pairs)
    nou = re.sub(' +', ' ', nou)
    with open(nom + ".txt", 'w') as text:
        text.write(nou)
    print "New text joint entropy: " + str(joint_entropy(nou))
# endregion


def main(case="", input="", aux=""):
    if input != "":
        with open(input, 'r') as file:
            txt = file.read()
            if case == "clean" and aux != "":
                clean_txt(txt, aux)
            elif case == "entropy":
                print "H(X): " + str(entropy(txt))
            elif case == "joint_entropy":
                print "H(X,Y): " + str(joint_entropy(txt))
            elif case == "conditional_entropy1" and aux != "":
                print "H(Y|x): " + str(conditional_entropy1(txt, aux))
            elif case == "conditional_entropy1" and aux == "espai":
                print "H(Y|x): " + str(conditional_entropy1(txt, " "))
            elif case == "conditional_entropy":
                print "H(Y|X): " + str(conditional_entropy(txt))
            elif case == "new" and aux != "":
                new_text(aux, txt)
            elif case == "new_joint" and aux != "":
                new_text_joint(aux, txt)
            else:
                print("Usage:")
                print("Lab1.py clean path/to/originaltxt nom_del_text")
                print("Lab1.py entropy path/to/cleantxt")
                print("Lab1.py joint_entropy path/to/cleantxt")
                print("Lab1.py conditional_entropy1 path/to/cleantxt specified_letter")
                print("Lab1.py conditional_entropy path/to/cleantxt")
                print("Lab1.py new clean_txt nom_del_nou_text")
                print("Lab1.py new_joint clean_txt nom_del_nou_text")
    else:
        print("Usage:")
        print("Lab1.py function path/to/text/defined/by/function")


if __name__ == '__main__':  # no tocar
    main(*sys.argv[1:])
