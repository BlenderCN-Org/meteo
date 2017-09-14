

## bang_image.py


import os
import numpy as np
import cv2
from time import time, sleep
from random import randint

## Variable globale qu'il ne faut pas modifier

# Gray sans alpha
IMG = "bang_2.png"

LARG = 1200
HAUT = 800

# (scale de départ, scale à chaque frame)
SCALE = (0.1, 1.04)


def load_image_default(image):
    '''Chargement de l'image en gris.
    cv2.IMREAD_COLOR : Loads a color image.
        Any transparency of image will be neglected. It is the default flag=1
    cv2.IMREAD_GRAYSCALE : Loads image in grayscale mode, flag=0
    cv2.IMREAD_UNCHANGED : Loads image as such including alpha channel flag=-1
    '''

    return cv2.imread(image, 1)

def load_image_gray(image):
    '''Chargement de l'image en gris.
    cv2.IMREAD_COLOR : Loads a color image.
        Any transparency of image will be neglected. It is the default flag=1
    cv2.IMREAD_GRAYSCALE : Loads image in grayscale mode, flag=0
    cv2.IMREAD_UNCHANGED : Loads image as such including alpha channel flag=-1
    '''

    return cv2.imread(image, 0)

def load_image_RVB(image):
    '''Chargement de l'image en RVB
    cv2.IMREAD_COLOR : Loads a color image.
        Any transparency of image will be neglected. It is the default flag=1
    cv2.IMREAD_GRAYSCALE : Loads image in grayscale mode, flag=0
    cv2.IMREAD_UNCHANGED : Loads image as such including alpha channel flag=-1
    '''

    return cv2.imread(image, -1)

def scale_image(img, k):
    '''Pour interpolation doc à https://goo.gl/9zNK7e'''
    return cv2.resize(   img,
                        None,
                        fx=k,
                        fy=k,
                        interpolation=cv2.INTER_LINEAR)

def get_black_image():
    return np.zeros((HAUT, LARG, 1), np.uint8)

def get_blank_image():
    img = np.zeros((HAUT, LARG, 4), np.uint8)
    img[:] = (255, 255, 255, 0)
    return  img

def crop_xs(foreground, a, b):
    '''Coupe ce qui dépasse du background à droite et en bas'''

    y, x = foreground.shape
    if x + a > LARG:
        # Coupe à droite
        ca = x + a - LARG
        foreground = right_crop(foreground, ca)
        #print("Coupe à droite de ", ca, ", reste", foreground.shape[1])

    if y + b > HAUT:
        # Coupe en bas
        cb = y + b - HAUT
        foreground = down_crop(foreground, cb)
        #print("Coupe en bas", cb, ", reste", foreground.shape[0])

    return foreground

def up_crop(img, c):
    c = abs(c)
    return img[c:, :]

def left_crop(img, c):
    c = abs(c)
    return img[:, c:]

def down_crop(img, c):
    c = abs(c)
    return img[:-c, :]

def right_crop(img, c):
    c = abs(c)
    return img[:, :-c]

def center_to_origin(img, C):
    '''C = cx, cy'''

    h, w = img.shape
    cx = C[0]
    cy = C[1]
    a = cx - int(w/2)
    b = cy - int(h/2)

    return a, b

def position_1(foreground, a, b):
    ''' haut, gauche: a < 0 ; b < 0
    Origine en A
    '''

    decal = 0, 0

    # Coupe haut et gauche
    img = left_crop(foreground, a)
    img = up_crop(img, b)

    # Coupe de l'excès
    img = crop_xs(img, decal[0], decal[1])

    return img, decal

def position_2(foreground, a, b):
    ''' haut: 0 < a < L ; b < 0
    Origine sur AB
    '''

    decal = a, 0

    # Coupe haut
    img = up_crop(foreground, b)

    # Coupe de l'excès
    img = crop_xs(img, a, 0)

    return img, decal

def position_9(foreground, a, b):
    ''' 0 < a < L ; 0 < b < H soit dans background'''

    decal = a, b
    # Coupe de l'excès
    img = crop_xs(foreground, a, b)

    return img, decal

def selection_position(foreground, a, b):
    '''Retourne l'image foreground et  le décalage à appliquer.
    En fonction de la position du point A d'application du foreground,
    position_x rogne foreground et calcul le décalage.
    '''

    if a < 0 and b < 0:
        foreground, decal = position_1(foreground, a, b)
    elif 0 < a < LARG and b < 0:
        foreground, decal = position_2(foreground, a, b)
    elif 0 <= a <= LARG and 0 <= b <= HAUT:
        foreground, decal = position_9(foreground, a, b)
    else:
        foreground, decal = None, None

    return foreground, decal

def superposition(background, foreground, decal):
    '''Superposition de foreground sur background,
    foreground en gray sans alpha
    decal = (a, b) tuple position du coin haut gauche
    '''

    # Dimension de foreground
    rows_fg, cols_fg = foreground.shape

    a = decal[0]
    b = decal[1]
    # roi est la partie d'image du background où sera ajouté le foreground

    l = cols_fg + a
    h = rows_fg + b

    roi = background[b:h, a:l]

    # Now create a mask of foreground and create its inverse mask also
    img2gray = foreground
    ret, mask = cv2.threshold(img2gray, 1, 255, cv2.THRESH_BINARY)

    mask_inv = cv2.bitwise_not(mask)

    # Now black-out the area of foreground in roi
    bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

    # Take only region of foreground
    fg = cv2.bitwise_and(img2gray, img2gray, mask=mask)

    # Put fg on bg
    dst = cv2.add(bg, fg)

    # Shape 2 pour dst, 3 pour background
    background[b:h, a:l, 0] = dst

    return background

def display_image():

    print("Affichage des images superposées")

    t_print = time()
    freq = 0
    background = get_black_image()
    wave_ori = load_image_gray(IMG)

    # Scale initial
    wave = scale_image(wave_ori.copy(), SCALE[0])

    C = (randint(0, 1200), randint(0, 800))
    t_init = time()

    while "Pas d'appui sur Echap":
        if time() - t_init > 0.5:
            t_init = time()
            wave = scale_image(wave_ori.copy(), SCALE[0])
            C = (randint(0, 1200), randint(0, 800))

        bg_img = background.copy()
        # Scale à chaque frame
        wave = scale_image(wave, SCALE[1])

        a, b = center_to_origin(wave, C)
        foreground, decal = selection_position(wave, a, b)

        if decal:
            # Image finale
            img = superposition(bg_img, foreground, decal)

            # Affichage de l'image
            cv2.imshow('bang', img)

            # Fréquence
            freq += 1
            if time() - t_print > 1:
                print("Fréquence =", int(freq))
                t_print, freq = time(), 0

            # Wait for esc key to exit
            key = np.int16(cv2.waitKey(1))  # défini ma fréquence maxi ~50 fps
            if key == 27:  # Echap
                break


if __name__ == "__main__":
    display_image()



