# -*- coding: utf-8 -*-
"""
Javier Garcia Sanchez
47179375-G
"""
import random as rng
import re
import string
import sys
import unicodedata

from numpy.lib.scimath import log2


# region auxiliars
def pars(txt):                    # llista de parells de lletres
    pairs = []
    for i in range(0, len(txt) - 1):
        if txt[i] != ' ' and txt[i + 1] != ' ': pairs.append(txt[i] + txt[i + 1])
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


def entropy(txt):                            # entropia de la variable X d'un text: lletra aleatoria del text
    total_letters = count_total(txt)
    accum = 0.0
    for l in string.ascii_lowercase:
        count = float(txt.count(l))
        if count > 0:
            p = count / total_letters
            accum += p * info(p)
            #print l + " " + str(p) + " " + str(count)
    return accum
# endregion


# region joint entropy
def parells():   #llista de tots els parells possibles des de "aa" fins a "zz"
    p = []
    for i in string.ascii_lowercase:
        for j in string.ascii_lowercase:
            p.append(i + j)
    return p


def joint_entropy(txt):                          # entropia conjunta de dos variables aleatories
    total_pairs = total_consecutive(txt)         # que representen un parell de lletres consecutives
    accum = 0.0
    pairs = parells()
    for par in pairs:
        count = count_consecutive(txt, par)
        if count > 0:
            p = count / total_pairs
            accum += p * info(p)
            #print par + " " + str(count) + " " + str(p)
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


def conditional_entropy1(txt, ltr):              # entropia condicional respecte una lletra fixada "ltr"
    if ltr == "espai":                           # entropia d'una lletra del text si ve després de "ltr"
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


def conditional_entropy(txt):                    # entropia condicional d'una lletra Y respecte X per
    total_pairs = total_consecutive(txt)         # a tots els parells Y,X del text donat
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
def conditional_entropy(txt):                    # implementació alternativa del calcul de entropia
    letters = count_total(txt)                   # condicional H(Y|X) (més costós)
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
def new_text(nom, txt):                                 #text random generat amb les mateixes probilitats
    nou = ""                                            #de lletres que el text donat, i per tant, mateixa entropia
    for i in range(0, len(txt)):
        nou += rng.choice(txt)
    nou = re.sub(' +', ' ', nou)
    with open(nom + ".txt", 'w') as text:
        text.write(nou)
    print "New text entropy: " + str(entropy(nou))

def new_text_joint(nom, txt):                            #text random de parells amb espais forçats per
    nou = ""                                             #a que sigui possible obtenir entropia correcta
    pairs = pars(txt)                                    #sino les probabilitats de parells no son correctes
    for i in range(0, len(txt) / 2):
        p = " " + rng.choice(pairs)
        nou += p
    with open(nom + ".txt", 'w') as text:
        text.write(nou)
    #print "New text joint entropy: " + str(joint_entropy(nou))
    #print "New text conditional entropy: " + str(conditional_entropy(nou))
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

'''
He utilitzat 2 textos en català, 2 en anglès, 1 en castellà (el quijote) i 1 en alemany.
La majoria de les proves les he fet finalment amb un dels textos en català (Tirant lo Blanc) i el text
en castellà (el quijote) perque son els dos mes llargs que he obtingut (sobre els 2 milions de caracters cadascun).
Entropia de "El Quijote": 4.0304
Entropia "Tirant lo Blanc": 4.0231
Entropia "Also sprach Zarathustra": 4.0415
Entropia "Oliver Twist": 4.1812
Entropia "Ulysses": 4.2051
En general sembla que l'anglès té una mica més d'informació (entropia) que el castellà, català o alemany

A l'hora de generar nous textos aleatoris cal remarcar que per a poder generar un text amb la mateixa entropia conjunta,
aquest es genera guardant directament els parells seleccionats aleatoriament del text base perque sino per a fer el calcul
de la entropia conjunta del nou text es compten probabilitats de parells errònies:
per exemple: si tenim un text "aabbcc" i generem un nou amb els parells extrets aleatòriament per exemple "aaaacc"
en el primer text tenim: 1 "aa", 1 "ab", 1 "bb", 1 "bc" i 1 "cc" mentre que en el segon tindriem: 3 "aa" (quan en
realitat hem inserit 2), 1 "ac"(que no existeix en el text base) i 1 "cc"
Si guardem el text generat per parells inserint espais no tenim aquest problema "aa aa cc" pero estem introduint
espais de manera forçada (tot i que el text base també té espais)

'''