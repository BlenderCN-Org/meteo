#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

## explosion.py

#import matplotlib.pyplot as plt
import operator
import numpy as np
import cv2
from time import time, sleep


class WaveCurve:
    '''Onde faite de segments de droite.'''

    def __init__(self, O, start, end, ampli):
        '''Onde:
        O = centre du dessin = (x, y)
        start = début
        end = fin
        ampli = amplitude verticale
        '''

        self.start = start
        self.end = end
        self.ampli = ampli
        # Tous les points devront être corrigés de O
        self.O = O

        self.set_variables()

    def set_variables(self):

        self.delta = (self.end - self.start) / 4.5
        self.A = self.start, 0
        self.B = int(self.start + self.delta), - self.ampli
        self.C = int(self.start * self.delta/28), 0

    def get_curve(self, img):

        #draw_line(img, self.O, t_s(self.A, self.O))
        draw_line(img, t_s(self.A, self.O), t_s(self.B, self.O))
        draw_line(img, t_s(self.B, self.O), t_s(self.C, self.O))

def t_s(a, b):
    return tuple(map(operator.add, a, b))


def draw_line(img, X, Y):
    # Origine en haut à gauche
    # Draw a white line, from X to Y, thickness of 2 px
    cv2.line(img, (int(X[0]), int(X[1])), (int(Y[0]), int( Y[1])), (255, 255, 255), 2)

def get_black_image():
    return np.zeros((800, 1200, 1), np.uint8)

def display():
    img = get_black_image()

    wc = WaveCurve((200, 400), 350, 500, 200)
    wc.get_curve(img)

    while True:

        # Display an image
        cv2.imshow('image', img)

        # wait for esc key to exit
        key = np.int16(cv2.waitKey(33))
        if key == 27:  # Echap
            break

    cv2.destroyAllWindows()



def get_droite_coeff(x1, y1, x2, y2):

    a = (y1 - y2) / (x1 - x2)

    b = y1 - a * x1

    return a, b

def main():
    #print(get_droite_coeff(1, 1, 4, 2))
    display()


if __name__ == "__main__":
    main()
