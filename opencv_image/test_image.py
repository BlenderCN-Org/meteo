

## test_image.py


import numpy as np
import cv2
from time import time, sleep


# Variable globale qu'il ne faut pas modifier
LARG = 1200
HAUT = 800
# IMG est modifiée dans bitwise_operations
IMG = "bang_2.png"


def load_image_gray(image):
    """Chargement de l'image en gris."""

    return cv2.imread(image, 0)

def load_image_RVB(image):
    """Chargement de l'image en RVB"""

    return cv2.imread(image, 1)

def set_resolution(img, res):

    return cv2.resize(img, res, interpolation = cv2.INTER_AREA)

def scale_image(img, k):

    return cv2.resize(   img,
                        None,
                        fx=k,
                        fy=k,
                        interpolation=cv2.INTER_CUBIC)

def grab_image():
    """See below example for a shift of (100,50)"""

    img = cv2.imread('messi5.jpg', 0)
    rows,cols = img.shape

    M = np.float32([[1, 0, 100], [0, 1, 50]])
    dst = cv2.warpAffine(img, M, (cols, rows))

    cv2.imshow('img', dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def add_image(img1, img2):
    """Uniquement si taille images identiques"""

    img1 = cv2.add(img1, img2)
    return img1

def get_black_image():
    return np.zeros((HAUT, LARG, 1), np.uint8)

def display_image_bad(black, img):

    t_print = time()
    freq = 0

    print("Affichage des images superposées bad")

    k = 0.95
    while "Pas d'appui sur Echap":
        img = bitwise_operations(black, img)
        # Scale pour la prochaine boucle
        img = scale_image(img, k)

        # Affichage de l'image
        cv2.imshow('bang', img)

        freq += 1

        if time() - t_print > 1:
            print("Fréquence =", int(freq))
            t_print, freq = time(), 0

        # wait for esc key to exit
        key = np.int16(cv2.waitKey(33))  # défini ma fréquence maxi ~30 fps
        if key == 27:  # Echap
            break

def display_image(img):
    """img = image avec les ondes blanches"""

    t_print = time()
    freq = 0

    print("Affichage des images superposées")

    k = 0.95
    while "Pas d'appui sur Echap":
        blk = get_black_image()
        # Scale de
        img = scale_image(img, k)
        img = bitwise_operations(blk, img)

        # Affichage de l'image
        cv2.imshow('bang', img)

        freq += 1

        if time() - t_print > 1:
            print("Fréquence =", int(freq))
            t_print, freq = time(), 0

        # wait for esc key to exit
        key = np.int16(cv2.waitKey(33))  # défini ma fréquence maxi ~30 fps
        if key == 27:  # Echap
            break

def bitwise_operations(img1, img2):
    """bitwise de img2 sur img1."""

    # I want to put logo on top-left corner, So I create a ROI
    try:
        rows, cols, channels = img2.shape
    except:
        rows, cols = img2.shape

    roi = img1[0:rows, 0:cols]

    # Now create a mask of logo and create its inverse mask also
    #img2gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    img2gray = img2
    ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)

    # Now black-out the area of logo in ROI
    img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

    # Take only region of logo from logo image.
    img2_fg = cv2.bitwise_and(img2gray, img2gray, mask=mask)

    # Put logo in ROI and modify the main image
    dst = cv2.add(img1_bg, img2_fg)
    # L'exemple de la doc opencv serait fausse !
    #img1[0:rows, 0:cols] = dst
    # Shape 2 pour dst, 3 pour img1
    img1[0:rows, 0:cols, 0] = dst

    return img1

def test():
    print("Test bitwise = bit à bit")
    img = load_image_gray(IMG)
    blk = get_black_image()
    display_image_bad(blk, img)
    display_image(img)

if __name__ == "__main__":
    test()
