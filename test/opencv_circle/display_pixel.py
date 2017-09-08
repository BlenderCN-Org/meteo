#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

## display_pixel.py

import numpy as np
import cv2
from time import time

# Load an color image in grayscale
# 10 images dans un dict
src = []
for i in range(11):
    src.append(cv2.imread('images/gris' + str(i) + '.png', 0))

t_print = time()
nb = 0

lp = 8
lq = 10
li = 7
loop = 0

while True:
    loop += 1
    if loop > 10:
        loop = 0

    img = src[loop]
    for p in range(lp):
        for q in range(lq):
            truc = q + loop
            if truc > 10:
                truc = 0
            img = np.concatenate((img, src[truc]), axis=0)

    for i in range(li):
        img = np.concatenate((img, img), axis=1)

    # Display an image
    cv2.imshow('image', img)

    nb += 1
    res = time() - t_print

    if res > 1:
        freq = nb/(time() - t_print)
        print("Fréquence =", int(freq))
        t_print, nb = time(), 0

    # wait for esc key to exit
    key = np.int16(cv2.waitKey(33))
    if key == 27:  # Echap
        break

cv2.destroyAllWindows()
