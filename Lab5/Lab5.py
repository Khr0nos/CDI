# coding=utf-8
"""
Javier Garcia Sanchez
47179375-G
"""
import argparse

import matplotlib.pyplot as plt
import scipy.linalg
from scipy import misc


def fit_image(image, N):          #ajustar imatge per a tenir un nombre de files/columnes multiple de N
    rows = columns = 0
    h = image.shape[0]
    w = image.shape[1]
    last_row = image[h - 1]
    last_column = image[:, w - 1]
    print(last_row.shape)
    # while h % N != 0 and w % N != 0:
    #     image = np.concatenate((image, last_row), 0)
    #     rows += 1
    #     if h % N == 0:
    #         break
    #     image = np.concatenate((image, last_column), 1)
    #     columns += 1

    return rows, columns


def lossy_transform(img, T, Q):
    image = misc.imread(img)
    N = T.shape[0]
    original_shape = image.shape
    print(original_shape)
    if original_shape[0] % N != 0 or original_shape[1] % N != 0:
        rows, columns = fit_image(image, N)
        print(rows, columns)
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
