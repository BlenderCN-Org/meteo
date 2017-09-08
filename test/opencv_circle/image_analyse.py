#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

## image_analyse.py

from time import time
import numpy as np
import cv2


#res = 192, 120
# Résolution pour les bidouilles sur l'image
res = 320, 180
print(
    "l =", res[0],
    "h =",  res[1],
    "Nombre de pixels =", res[0]*res[1],
    "ratio", res[0]/res[1]
    )

# Aggrandissemnt pour affichage en fonction de la résolution de l'écran
aggr = 6

def load_image(image):
    """Chargement de l'image en gris."""

    return cv2.imread(image, 0)


def set_resolution(img, res):

    return cv2.resize(img, res, interpolation = cv2.INTER_AREA)


def vertical_bidouille(img):
    """Glissement sur x de l'image.

    Get columns 1 and 9:
        extractedData = data[:,[1,9]]

    """

    l, h = res
    new_img = img.copy()

    for u in range(h):
        ##print(new_img.shape)
        ##print(img[u, :].shape)
        ##print(new_img[h-u-1, :].shape)

        # Glissement par remplacement de u par h-u-1
        new_img[h-u-1, :] = img[u, :]

    return new_img


def horizontal_bidouille(img):
    """data[:,[1,9]] 1 à 9"""

    l, h = res
    new_img = img.copy()

    for u in range(l):
        ##print(new_img.shape)
        ##print(new_img[:,[u]].shape)
        ##print(new_img[:,[l-u-1]].shape)

        new_img[:,[u]] = img[:,[l-u-1]]

    return new_img


def glissement(img):
    l, h = res
    new_img = img.copy()

    for u in range(l):
        # Glissement
        if u < l:
            new_img[:,[u-1]] = img[:,[u]]
        else:
            new_img[:,[u]] = img[:,[0]]

    return new_img


def display_image(img):

    t_print = time()
    nb = 0

    while "Pas d'appui sur Echap":
        nb += 1

        # bidouille sur l'image
        ##img = horizontal_bidouille(img)
        ##img = vertical_bidouille(img)
        img = glissement(img)
        # Agrandissement de l'image pour affichage
        big_img = set_resolution(img, (res[0]*aggr, res[1]*aggr))

        # Affichage de l'image
        cv2.imshow('image', big_img)

        nb += 1
        dif = time() - t_print

        if dif > 1:
            freq = nb/(time() - t_print)
            print("Fréquence =", int(freq))
            t_print, nb = time(), 0

        # wait for esc key to exit
        key = np.int16(cv2.waitKey(33))
        if key == 27:  # Echap
            break


def save_image(img):
    filename = "images/test_resize.png"
    cv2.imwrite(filename, img)


def main():
    image = 'images/coucher_2.jpg'
    img = load_image(image)

    img = set_resolution(img, res)
    display_image(img)


if __name__ == "__main__":
    main()
