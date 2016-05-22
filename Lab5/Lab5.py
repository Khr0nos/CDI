# coding=utf-8
"""
Javier Garcia Sanchez
47179375-G
"""
import argparse

import matplotlib.pyplot as plt
import scipy as sp
import scipy.linalg
from scipy import misc


def fit_image(image, N):  # ajustar imatge per a tenir un nombre de files/columnes multiple de N
    rows = 0
    columns = 0
    h = image.shape[0]
    last_row = image[h - 1:]
    while h % N != 0:
        image = sp.insert(image, h, last_row, 0)
        rows += 1
        h = image.shape[0]

    w = image.shape[1]
    last_column = image[:, w - 1]
    while w % N != 0:
        image = sp.insert(image, w, last_column, 1)
        columns += 1
        w = image.shape[1]

    return rows, columns, image


def trim_image(image, rows, columns):     # eliminar files/columnes sobrants
    h = image.shape[0]
    while rows > 0:
        image = sp.delete(image, h - 1, 0)
        h = image.shape[0]
        rows -= 1

    w = image.shape[1]
    while columns > 0:
        image = sp.delete(image, w - 1, 1)
        w = image.shape[1]
        columns -= 1

    return image


def lossy_transform(img, T, Q):
    original = misc.imread(img, mode='L')
    N = T.shape[0]
    print(original.shape)
    # afegir files/columnes si cal
    rows = 0
    columns = 0
    if original.shape[0] % N != 0 or original.shape[1] % N != 0:
        rows, columns, fitted_img = fit_image(original, N)
        print(fitted_img.shape)



    # eliminar files/columnes addicionals si s'han afegit previament
    trimmed_image = original
    if rows > 0 and columns > 0:
        trimmed_image = trim_image(fitted_img, rows, columns)
        print(trimmed_image.shape)
    #plt.gray()
    fig = plt.figure()
    a = fig.add_subplot(1, 2, 1)
    a.set_title('Original')
    plt.imshow(original, cmap=plt.cm.get_cmap('gray'))
    a = fig.add_subplot(1, 2, 2)
    a.set_title('Processada')
    plt.imshow(fitted_img, cmap=plt.cm.get_cmap('gray'))
    plt.show()


def main():
    parser = argparse.ArgumentParser(description="Transform image coding")
    parser.add_argument('image', help="path to image")
    parser.add_argument('-T', type=sp.ndarray, help="N x N Transform matrix", metavar="Matrix")
    parser.add_argument('-q', type=int, help="Matriu quantització uniforme N x N", metavar="enter > 0")
    parser.add_argument('-H', type=int, help="Mida de la matriu Hadamard de transformació", metavar="N")
    parser.add_argument('-I', type=int, help="Mida de la matriu identitat de quantització", metavar="I")
    args = parser.parse_args()
    if args.I is not None and args.H is not None:
        T = scipy.linalg.hadamard(args.H, dtype=float)
        Q = sp.identity(args.I, dtype=int)
        lossy_transform(args.image, T, Q)
    if args.q is not None and args.H is not None:
        T = scipy.linalg.hadamard(args.H, dtype=float)
        N = T.shape[0]
        Q = sp.ones((N, N), dtype=int) * args.q
        lossy_transform(args.image, T, Q)
    # if args.q is None:
    #     print("El valor per a la matriu de quantitzacio no s'ha definit [-q enter]")


if __name__ == '__main__':  # no tocar
    main()
