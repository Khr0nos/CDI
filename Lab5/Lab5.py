# coding=utf-8
"""
Javier Garcia Sanchez
47179375-G
"""

import matplotlib.pyplot as plt
import scipy.misc


def main():
    img = scipy.misc.imread("lena.jpg")
    #print(img)
    plt.imshow(img)
    plt.show()








if __name__ == '__main__':  # no tocar
    main()
