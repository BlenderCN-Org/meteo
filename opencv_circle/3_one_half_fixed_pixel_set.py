#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

## explosion.py

import operator
import numpy as np
import cv2
from time import time, sleep

LARG = 1200
HAUT = 800


class HalfWave:
    '''Une demi onde: A B C'''

    def __init__(self, O, start, gap, ampli, sens=0):
        '''O est l'origine = tuple x, y
        start = début de l'onde
        gap = décalage du point C
        ampli = amplitude de l'onde
        sens = vers le haut ou vers le bas
        '''

        # TODO sens est faux
        self.start = int(start)
        self.gap = int(gap)
        self.ampli = int(ampli)

        if sens not in [0, 1]:
            self.sens = 1
        else:
            self.sens = sens

        # Tous les points devront être corrigés de O(Ox, Oy)
        self.O = O

        self.set_variables()

    def set_variables(self):
        '''Les points sont comptés à partir de O'''

        self.A = (self.start, 0)

        if self.sens:
            self.B = (int(self.start + self.gap/2), - self.ampli)
        else:
            self.B = (int(self.start + self.gap/2), self.ampli)

        self.C = (self.start + self.gap, 0)

    def draw_half_wave(self, img):
        '''Droite de A à B et de B à C'''

        a = t_s(self.A, self.O)
        b = t_s(self.B, self.O)
        c = t_s(self.C, self.O)

        # Droite de A à B
        img = draw_line(img, a, b)
        # Droite de B à C
        img = draw_line(img, b, c)

        return img

def draw_line(img, A, B):
    '''Dessine la droite entre A et B.
    (1, 250)
    (-2, 1160)
    (1, 90)
    (-2, 1688)
    (1, -38)
    (-2, 2094)
    (1, -140)
    (-2, 2407)
    (1, -221)
    (-2, 2653)
    '''

    a, b = get_droite_coeff(A[0], A[1], B[0], B[1])
    for i in range(int(A[0]), int(B[0])):
        x = i
        y = int(a*x + b)
        if 0 < x < LARG and 0 < y < HAUT:
            img[y][x] = [255]

    return img

def t_s(a, b):
    return tuple(map(operator.add, a, b))

def get_droite_coeff(x1, y1, x2, y2):

    a = (y2 - y1) / (x2 - x1)

    b = y1 - a * x1

    return a, b

def get_black_image():
    return np.zeros((HAUT, LARG, 1), np.uint8)

def display():
    img = get_black_image()

    wv = HalfWave((50, 400), 100, 100, 200)
    img = wv.draw_half_wave(img)

    while True:

        # Display an image
        cv2.imshow('image', img)

        # wait for esc key to exit
        key = np.int16(cv2.waitKey(33))
        if key == 27:  # Echap
            break

    cv2.destroyAllWindows()

def main():
    display()


if __name__ == "__main__":
    main()
