# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 12:45:24 2016

@author: Javier Garcia Sanchez
"""
import sys

def clean_txt(txt, prefix):
    with open(prefix+"_clean.txt",'w') as out:
        del_sym = [',', '.', ';', ':', '_', '¡', '!', '¿', '?', '(', ')', '$', '€', '*', '=', '%', '&', '/', '#', '·']
        space_sym = ['-', '\n', '"', "'", '»', '«', '<', '>']
        for c in txt:
            if (c in del_sym): c = ''
            elif (c in space_sym): c = ' '
            
            out.write(c.lower())


def main(input="C:\Users\Xavi\Documents\FIB\CDI\Lab\Lab1\quijote.txt", filename="quijote"):
    with open(input,'r') as file:
        txt = file.read()
    clean_txt(txt,filename)



if __name__ == '__main__':                  #no tocar                               
    main(*sys.argv[1:])
