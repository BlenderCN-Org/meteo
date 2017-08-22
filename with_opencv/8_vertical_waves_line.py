#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

## explosion.py


import os
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
        self.line = []

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
        img, line1 = draw_line(img, a, b)
        # Droite de B à C
        img, line2 = draw_line(img, b, c)

        # La liste des points des2 lignes
        self.line = line1 + line2

        return img


class Waves(dict):
    '''self hérite de dict: attributs et méthodes
    n maxi 10
    '''

    def __init__(self, n, O, start, gap, ampli):
        self.n = n
        self.start = start
        self.gap = gap
        self.ampli = ampli
        self.O = O
        self.lines = []

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
        start = self.start
        gap = self.gap

        points = [(start, gap)]
        for i in range(7):
            toto = points[i][0] + points[i][1], gap*(1-0.1*(i+1))
            points.append(toto)

        return points

    def draw(self, img):  #, centre):

        # Les demi courbes
        for i in range(self.n):
            img = self[i].draw_half_wave(img)
            self.lines = self.lines + self[i].line

        return img


def draw_line(img, A, B):
    '''Dessine la droite entre A et B.'''

    a, b = get_droite_coeff(A[0], A[1], B[0], B[1])

    line = []
    for i in range(int(A[0]), int(B[0])):
        x = i
        y = int(a*x + b)
        if 0 < x < LARG and 0 < y < HAUT:
            img[y][x] = [255]
            line.append([x, y])

    return img, line

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

def line_to_real_wave1(img, lines):
    for point in lines:
        x = point[0]
        y = point[1]
        for i in range(HAUT):
            img[i][x] = [int(y/6)]
    return img

def line_to_real_wave2(img, lines, ampli):
    ''' HAUT/2 --> 0
        HAUT/2 + ampli --> 255
        (y/ampli)*255
    '''

    for point in lines:
        x = point[0]
        ##print(point[1])
        ##sleep(0.05)

        y = point[1]
        try:
            yr = abs(y - HAUT/2)
            color = (yr/2*ampli)*255
            color = min(int(yr), 255)
            #print(color)
        except:
            color = 255

        X = x, 0
        Y = x, HAUT
        if x % 2 == 0:
            img = draw_opencv_line(img, X, Y, color)

    return img

def draw_opencv_line(img, X, Y, color):
    # Origine en haut à gauche
    # Draw a white line, from X to Y, thickness of 2 px
    img = cv2.line(img,   (int(X[0]), int(X[1])),
                    (int(Y[0]), int( Y[1])),
                    [color],
                     2)
    return img

def display():
    a = 0
    black = get_black_image()
    t_zero = time()
    freq = 0

    while True:
        a += 1
        freq += 1
        if time() - t_zero > 1:
            t_zero = time()
            print("Fréquence", freq)
            freq = 0

        img = black.copy()
        rytm = 1
        ampli = max(100 - rytm*a, 0)
        wave = Waves(8, (LARG/5 + rytm*a, HAUT/2), 50, 300, ampli)

        img = wave.draw(img)
        img = line_to_real_wave2(img, wave.lines, ampli)

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
