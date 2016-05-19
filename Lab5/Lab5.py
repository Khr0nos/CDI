# coding=utf-8
"""
Javier Garcia Sanchez
47179375-G
"""
import argparse

import matplotlib.pyplot as plt
import numpy as np
import scipy.linalg
from scipy import misc


def fit_image(image, N):          #ajustar imatge per a tenir un nombre de files/columnes multiple de N
    rows = 0
    columns = 0
    h = image.shape[0]
    w = image.shape[1]
    #last_column = image[:, w - 1:]
    last_row = image[h - 1:]
    while h % N != 0:
        image = np.insert(image, h - 1, last_row, 0)
        rows += 1
        h = image.shape[0]

    while w % N != 0:
        image = np.insert(image, w - 1, image[:, w - 1:], 1)
        columns += 1
        w += image.shape[1]

    return rows, columns, image


def lossy_transform(img, T, Q):
    image = misc.imread(img)
    N = T.shape[0]
    original_shape = image.shape
    print(original_shape)
    if original_shape[0] % N != 0 or original_shape[1] % N != 0:
        rows, columns, image = fit_image(image, N)
    print(image.shape)
    plt.imshow(image)
    plt.show()












def main():
    parser = argparse.ArgumentParser(description="Transform image coding")
    parser.add_argument('image', help="path to image")
    parser.add_argument('-T', help="N x N Transform matrix", metavar="Matrix")
    parser.add_argument('-Q', help="N x N Quantization matrix", metavar="Matrix")
    parser.add_argument('-H', type=int, help="Mida de la matriu Hadamard de transformació", metavar="N")
    #parser.add_argument('-q', type=int, help="Mida de la matriu de quantització Q", metavar="N")
    args = parser.parse_args()
    Q = None
    T = None
    if args.H is not None:
        T = scipy.linalg.hadamard(args.H, dtype=float)


    lossy_transform(args.image, T, Q)


if __name__ == '__main__':  # no tocar
    main()
