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

    def tuple_sym(self,a, b):

        d = (self.O[0] - b[0], b[1])
        new = tuple(map(operator.add, a, d))

        return  new

    def symetric_draw_half_wave(self, img):
        '''Droite de A à B et de B à C'''

        a = self.tuple_sym(self.A, self.O)
        b = self.tuple_sym(self.B, self.O)
        c = self.tuple_sym(self.C, self.O)

        # Droite de A à B
        img = draw_line(img, a, b)
        # Droite de B à C
        img = draw_line(img, b, c)

        return img


class Waves(dict):
    '''self n'est pas de type dict mais hérite de dict: attributs et méthodes
    n maxi 10
    '''

    def __init__(self, n, O, start, gap, ampli):
        self.n = n
        self.start = start
        self.gap = gap
        self.ampli = ampli
        self.O = O

        points = self.get_points()

        # Pour OA
        self.A = (self.start, 0)
        # Pour fin
        self.F = (points[7][0]+gap*0.3, 0)

        for i in range(self.n):
            if i % 2 == 0:
                sens = 0
            else:
                sens = 1

            # O, start, gap, ampli, sens=0
            self[i] = HalfWave( self.O,
                                points[i][0],
                                points[i][1],
                                self.ampli*0.8**i,
                                sens)

    def get_points(self):
        ##l = [start, gap]
        ##for i in range(self.n - 1):
            ##toto = (l[i][0] + l[i][1], (1-0.1*i)*gap)
            ##print(toto)
            ##l.append(toto)

        start = self.start
        gap = self.gap
        points = [  (start + 0   * gap, gap*1),
                    (start + 1   * gap, gap*0.9),
                    (start + 1.9 * gap, gap*0.8),
                    (start + 2.7 * gap, gap*0.7),
                    (start + 3.4 * gap, gap*0.6),
                    (start + 4.0 * gap, gap*0.5),
                    (start + 4.5 * gap, gap*0.4),
                    (start + 4.9 * gap, gap*0.3)  ]

        return points

    def draw(self, img):
        # OA
        #img = draw_line(img, self.O, t_s(self.A, self.O))

        # Les demi courbes
        for i in range(self.n):
            img = self[i].draw_half_wave(img)

        # Fin
        #img = draw_line(img, t_s(self.F, self.O), (LARG, self.O[1]))

        return img

    def symetric_draw(self, img):

        # OA
        #img = draw_line(img, self.O, t_s(self.A, self.O))

        # Les demi courbes
        for i in range(self.n):
            img = self[i].symetric_draw_half_wave(img)

        # Fin
        #img = draw_line(img, t_s(self.F, self.O), (LARG, self.O[1]))

        return img


def draw_line(img, A, B):
    '''Dessine la droite entre A et B.'''

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

    if x2 - x1 != 0:
        a = (y2 - y1) / (x2 - x1)
        b = y1 - a * x1
    else:
        a, b = None, None

    return a, b

def get_black_image():
    return np.zeros((HAUT, LARG, 1), np.uint8)

def display():
    a = 0
    t_zero = time()
    freq = 0
    black = get_black_image()

    while True:
        img = black.copy()
        ampli = max(100 - 0.5*a, 0)

        # Un object farique à chaque frame
        #             n,         O,            start, gap, ampli
        waves = Waves(8, (LARG/2 + a, HAUT/2), 50,    50,  ampli)

        a += 1
        freq += 1
        if time() - t_zero > 1:
            print("Fréquence", freq)
            freq = 0
            t_zero = time()

        img = waves.draw(img)
        img = waves.symetric_draw(img)

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
