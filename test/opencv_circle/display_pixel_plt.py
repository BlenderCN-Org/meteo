#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

## display_pixel.py

import numpy as np
import cv2
from time import time
from matplotlib import pyplot as plt
from matplotlib import animation as animation
from matplotlib import interactive


fig = plt.figure() # make a figure
interactive(True)

src = []
for i in range(11):
    src.append(cv2.imread('images/gris' + str(i) + '.png', 0))  # 0 = gray

lp = 3
lq = 10
li = 5

a = 0
b = 0

img = src[0]
for p in range(lp):
    for q in range(lq):
        b += a
        if b >= 11:
            b = 0
        img = np.concatenate((img, src[b]), axis=0)
        a += 1
        if a >= 11:
            a = 0

for i in range(li):
    img = np.concatenate((img, img), axis=1)

#ani = animation.ArtistAnimation(fig, img_list)

plt.show()
plt.pause(0.001)
