

## bang_image.py


import os
import numpy as np
import cv2
from time import time, sleep


## Variable globale qu'il ne faut pas modifier

# Gray sans alpha
IMG = "bang_2.png"

# Gray avec alpha
#IMG = "bang_4.png"

# RVB avec canal alpha
#IMG = "bang_3.png"

#cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)

LARG = 1200
HAUT = 800

# (scale de départ, scale à chaque frame)
SCALE = (0.5, 1.005)


def image_translation(img, direction):
    """Décale l'image dans sa sa fenêtre,
    tutorial_py_geometric_transformations
    https://goo.gl/dmipSH
    """

    # Translation sur x et y
    tx,ty = direction[0], direction[1]

    # Taille de l'image
    rows, cols, _rien = img.shape

    M = np.float32([[1, 0, tx], [0, 1, ty]])

    return cv2.warpAffine(img, M, (cols, rows))

def load_image_default(image):
    """Chargement de l'image en gris.
    cv2.IMREAD_COLOR : Loads a color image.
        Any transparency of image will be neglected. It is the default flag=1
    cv2.IMREAD_GRAYSCALE : Loads image in grayscale mode, flag=0
    cv2.IMREAD_UNCHANGED : Loads image as such including alpha channel flag=-1
    """

    return cv2.imread(image, 1)

def load_image_gray(image):
    """Chargement de l'image en gris.
    cv2.IMREAD_COLOR : Loads a color image.
        Any transparency of image will be neglected. It is the default flag=1
    cv2.IMREAD_GRAYSCALE : Loads image in grayscale mode, flag=0
    cv2.IMREAD_UNCHANGED : Loads image as such including alpha channel flag=-1
    """

    return cv2.imread(image, 0)

def load_image_RVB(image):
    """Chargement de l'image en RVB
    cv2.IMREAD_COLOR : Loads a color image.
        Any transparency of image will be neglected. It is the default flag=1
    cv2.IMREAD_GRAYSCALE : Loads image in grayscale mode, flag=0
    cv2.IMREAD_UNCHANGED : Loads image as such including alpha channel flag=-1
    """

    return cv2.imread(image, -1)

def scale_image(img, k):
    """Pour interpolation doc à https://goo.gl/9zNK7e"""
    return cv2.resize(   img,
                        None,
                        fx=k,
                        fy=k,
                        interpolation=cv2.INTER_LINEAR)

def get_black_image():
    return np.zeros((HAUT, LARG, 1), np.uint8)

def test_translation():

    wave = load_image_default(IMG)
    direction = 200, 100
    img = image_translation(wave, direction)

    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def crop(img, vertex, c):
    """Coupe en vertex = A B C D
    A haut gauche
    B haut droit
    C bas gauche
    D bas droit
    cut = (100, 200) vertical, horizontal
    """

    if vertex == "A":
        #img = img[cut[0]:, cut[1]:]
        img = up_crop(img, c[1])
        img = left_crop(img, c[0])

    if vertex == "B":
        #img = img[cut[0]:, :-cut[1]]
        img = up_crop(img, c[1])
        img = right_crop(img, c[0])

    if vertex == "C":
        #img = img[:-cut[0], :-cut[1]]
        img = down_crop(img, c[1])
        img = right_crop(img, c[0])

    if vertex == "D":
        #img = img[:-cut[0], cut[1]:]
        img = down_crop(img, c[1])
        img = left_crop(img, c[0])

    return img

def test_crop():

    for vertex in ["A", "B", "C", "D"]:
        img = load_image_default(IMG)
        cut = 200, 200
        img = crop(img, vertex, cut)

        cv2.imshow('img', img)
        cv2.waitKey(0)

def position_1(foreground, a, b):
    """ haut, gauche: a < 0 ; b < 0
    Origine en A
    """

    #print("Position 1")

    decal = 0, 0
    # Coupe haut et gauche
    img = left_crop(foreground, a)
    img = up_crop(img, b)

    # Coupe de l'excès
    img = crop_xs(img, decal[0], decal[1])

    return img, decal

def position_2(foreground, a, b):
    """ haut: 0 < a < L ; b < 0
    Origine sur AB
    """

    #print("Position 2")

    decal = a, 0
    # Coupe haut
    img = up_crop(foreground, b)
    #print(img.shape)
    # Coupe de l'excès
    img = crop_xs(img, a, 0)

    return img, decal

def position_8(foreground, a, b):
    """a < 0 ; 0 < b < LARG
    Origine sur AD, a = 0
    """

    #print("Position 2")

    decal = 0, b
    # Coupe gauche
    img = left_crop(foreground, b)
    # Coupe de l'excès
    img = crop_xs(img, 0, b)

    return img, decal

def position_9(foreground, a, b):
    """ 0 < a < L ; 0 < b < H soit dans background"""

    #print("Selection position 9")
    decal = a, b
    # Coupe de l'excès
    img = crop_xs(foreground, a, b)

    return img, decal

def selection_position(foreground, a, b):
    """Retourne l'image foreground et  le décalage à appliquer.
    En fonction de la position du point A d'application du foreground,
    position_x rogne foreground et calcul le décalage.
    """

    if a < 0 and b < 0:
        #print("\nSélection Position 1")
        foreground, decal = position_1(foreground, a, b)
    elif 0 < a < LARG and b < 0:
        #print("\nSélection Position 2")
        foreground, decal = position_2(foreground, a, b)
    ##elif a >= LARG:
        ##print("\nSélection Position 3 4 5")
        ##foreground, decal = None, None
    ##elif a < LARG and b >= HAUT:
        ##print("\nSélection Position 6 7")
        ##foreground, decal = None, None
    ##elif a < 0 and 0 < b < HAUT:
        ##print("\nSélection Position 8")
        ##foreground, decal = None, None
    elif 0 <= a <= LARG and 0 <= b <= HAUT:
        #print("\nSélection Position 9")
        foreground, decal = position_9(foreground, a, b)
    else:
        #print("Image en dehors du terrain de jeu")
        foreground, decal = None, None

    return foreground, decal

def crop_xs(foreground, a, b):
    """Coupe ce qui dépasse du background à droite et en bas"""

    y, x = foreground.shape
    print("Avant crop_xs foreground.shape", x, y, "décalage", a, b)
    if x + a > LARG:
        # Coupe à droite
        ca = x + a - LARG
        foreground = right_crop(foreground, ca)
        print("Coupe à droite de ", ca, ", reste", foreground.shape[1])

    if y + b > HAUT:
        # Coupe en bas
        cb = y + b - HAUT
        foreground = down_crop(foreground, cb)
        print("Coupe en bas", cb, ", reste", foreground.shape[0])

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

def test_simple_crop(foreground):
    foreground = load_image_default(IMG)
    img = left_crop(foreground, 100)
    img = up_crop(img, 100)
    img = down_crop(img, 100)
    img = right_crop(img, 100)
    cv2.imshow('Mix', img)
    cv2.waitKey(0)

def superposition(background, foreground, decal):
    """Superposition de foreground sur background,
    foreground en gray sans alpha
    decal = (a, b) tuple position du coin haut gauche
    """

    # Dimension de foreground
    rows_fg, cols_fg = foreground.shape

    a = decal[0]
    b = decal[1]
    print("\nSuperposition")
    print("rows_fg:", rows_fg, "cols_fg:", cols_fg, "Décalage:", a, b)

    # roi est la partie d'image du background où sera ajouté le foreground

    l = min(cols_fg + a, LARG)
    h = min(rows_fg + b, HAUT)
    print("l:", l, "h:", h)

    # Coupe de a, b et coupe de
    print("foreground.shape", foreground.shape)
    roi = background[b:h, a:l]
    print("roi.shape", roi.shape, "\n")

    # Now create a mask of foreground and create its inverse mask also
    #img2gray = cv2.cvtColor(foreground, cv2.COLOR_BGR2GRAY)
    img2gray = foreground
    ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    print("mask.shape", mask.shape)
    # Now black-out the area of foreground in roi
    bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

    # Take only region of foreground
    fg = cv2.bitwise_and(img2gray, img2gray, mask=mask)

    # Put fg on bg
    dst = cv2.add(bg, fg)

    # Shape 2 pour dst, 3 pour background
    background[b:h, a:l, 0] = dst

    return background

def test_position():
    d = (500, 600)
    background = get_black_image()
    foreground = load_image_gray(IMG)

    foreground, decal = selection_position(foreground, d[0], d[1])

    if decal:
        print("dans test_position foreground.shape, decal", foreground.shape, decal)
        img = superposition(background, foreground, decal)

        cv2.imshow('Mix', img)

        cv2.waitKey(0)

def center_to_origin():
    pass

def display_image():

    print("Affichage des images superposées")

    t_print = time()
    freq = 0
    background = get_black_image()
    wave = load_image_gray(IMG)

    # Scale initial
    wave = scale_image(wave, SCALE[0])

    while "Pas d'appui sur Echap":
        bg_img = background.copy()
        # Scale à chaque frame
        wave = scale_image(wave, SCALE[1])

        try:
            # Image finale
            img = superposition(bg_img, wave, (20,10))
            # Affichage de l'image
            cv2.imshow('bang', img)

            # Fréquence
            freq += 1
            if time() - t_print > 1:
                print("Fréquence =", int(freq))
                t_print, freq = time(), 0

            # Wait for esc key to exit
            key = np.int16(cv2.waitKey(16))  # défini ma fréquence maxi ~50 fps
            if key == 27:  # Echap
                break
        except:
            break


if __name__ == "__main__":
    display_image()



