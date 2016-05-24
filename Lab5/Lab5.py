# coding=utf-8
"""
Javier Garcia Sanchez
47179375-G
"""
import argparse

import matplotlib.pyplot as plt
import numpy as np
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


def trim_image(image, rows, columns):  # eliminar files/columnes sobrants
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
    original = img
    color = len(tuple(original.shape)) == 3
    N = T.shape[0]

    # afegir files/columnes si cal
    rows = 0
    columns = 0
    fitted_img = original
    if original.shape[0] % N != 0 or original.shape[1] % N != 0:
        rows, columns, fitted_img = fit_image(original, N)


    # transformation to frequency domain
    if color:
        h = fitted_img.shape[0]
        w = fitted_img.shape[1]
        d = fitted_img.shape[2]
        transformed = sp.ndarray(shape=(h, w, d), dtype=float)
        for i in range(0, h, N):
            for j in range(0, w, N):
                for k in range(d):
                    transformed[i:i + N, j:j + N, k] = T * fitted_img[i:i + N, j:j + N, k] * T.transpose()

    else:
        h = fitted_img.shape[0]
        w = fitted_img.shape[1]
        transformed = sp.ndarray(shape=(h, w), dtype=float)
        for i in range(0, h, N):
            for j in range(0, w, N):
                transformed[i:i + N, j:j + N] = T * fitted_img[i:i + N, j:j + N] * T.transpose()

    # quantization
    if color:
        h = transformed.shape[0]
        w = transformed.shape[1]
        d = transformed.shape[2]
        for i in range(0, h, N):
            for j in range(0, w, N):
                for k in range(d):
                    transformed[i:i + N, j:j + N, k] = transformed[i:i + N, j:j + N, k] / Q

        for i in range(0, h, N):
            for j in range(0, w, N):
                for k in range(d):
                    transformed[i:i + N, j:j + N, k] = np.round(transformed[i:i + N, j:j + N, k]) * Q

    else:
        h = transformed.shape[0]
        w = transformed.shape[1]
        for i in range(0, h, N):
            for j in range(0, w, N):
                transformed[i:i + N, j:j + N] = transformed[i:i + N, j:j + N] / Q

        for i in range(0, h, N):
            for j in range(0, w, N):
                transformed[i:i + N, j:j + N] = np.round(transformed[i:i + N, j:j + N]) * Q

    # inverse transform
    if color:
        h = transformed.shape[0]
        w = transformed.shape[1]
        d = transformed.shape[2]
        for i in range(0, h, N):
            for j in range(0, w, N):
                for k in range(d):
                    transformed[i:i + N, j:j + N, k] = sp.linalg.inv(T) * transformed[i:i + N, j:j + N, k] * sp.linalg.inv(T.transpose())

    else:
        h = transformed.shape[0]
        w = transformed.shape[1]
        for i in range(0, h, N):
            for j in range(0, w, N):
                transformed[i:i + N, j:j + N] = sp.linalg.inv(T) * transformed[i:i + N, j:j + N] * sp.linalg.inv(T.transpose())

    # eliminar files/columnes addicionals si s'han afegit previament
    newimg = transformed
    if rows > 0 and columns > 0:
        newimg = trim_image(newimg, rows, columns)
    return newimg


def main():
    parser = argparse.ArgumentParser(description="Transform image coding")
    parser.add_argument('image', help="path to image")
    parser.add_argument('-Q', type=int, help="N x N custom Transform matrix", metavar="Matrix")
    parser.add_argument('-q', type=int, help="Matriu quantització uniforme N x N", metavar="enter > 0")
    parser.add_argument('-H', type=int, help="Mida de la matriu Hadamard de transformació", metavar="N")
    parser.add_argument('-R', type=int, help="Mida de la matriu de quantització aleatoria", metavar="R")
    parser.add_argument('-I', type=int, help="Mida de la matriu identitat de transformació", metavar="I")
    parser.add_argument('-g', action='store_true', help="flag per a carregar imatge en escala de grisos")
    args = parser.parse_args()
    T = None
    Q = None
    if args.g is True:
        img = misc.imread(args.image, mode='L')
    else:
        img = misc.imread(args.image)
    if args.R is not None and args.H is not None:
        T = scipy.linalg.hadamard(args.H, dtype=float) * (1 / 2 * sp.sqrt(2))
        Q = sp.random.rand(args.R, args.R)
    if args.q is not None and args.H is not None:
        T = scipy.linalg.hadamard(args.H, dtype=float) * (1 / 2 * sp.sqrt(2))
        N = T.shape[0]
        Q = sp.ones((N, N), dtype=int) * args.q
    if args.I is not None and args.q is not None:
        T = sp.identity(args.I, dtype=float)
        N = T.shape[0]
        Q = sp.ones((N, N), dtype=int) * args.q

    if T is not None or Q is not None:
        newimg = lossy_transform(img, T, Q)

        fig = plt.figure()
        a = fig.add_subplot(1, 2, 1)
        a.set_title('Original')
        if args.g:
            plt.gray()
            plt.imshow(img)
        else:
            plt.imshow(img)
        a = fig.add_subplot(1, 2, 2)
        a.set_title('Processada')
        if args.g:
            plt.imshow(newimg)
        else:
            plt.imshow(newimg, cmap=plt.cm.get_cmap('gray'))
        plt.show()
    else:
        print("Matriu de transformació i/o quantització no definides")
    # if args.q is None:
    #     print("El valor per a la matriu de quantitzacio no s'ha definit [-q enter]")


if __name__ == '__main__':  # no tocar
    main()


    # Les imatges poden ser en escala de grisos, 1 únic canal si el paramtre "-q" s'ha donat per l'input o
    # imatges a color amb 3 canals si aquest flag no es dóna
