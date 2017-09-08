#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

## bangs.py


import os
import random
import operator
import threading
import numpy as np
import cv2
from time import time, sleep
print("Version OpenCV", cv2.__version__)

LARG = 1200
HAUT = 800


def get_black_image():
    return np.zeros((HAUT, LARG, 1), np.uint8)

# BANGS = { 1: DynamicBang() du bang 1,
#           2: DynamicBang() du bang 2}
BANGS = {}


class HalfWave:
    '''Une demi onde: O A B C'''

    def __init__(self, O, start, gap, ampli, sens=0):
        '''O est l'origine = tuple x, y
        start = début de l'onde = OA
        gap = décalage du point C = AC
        ampli = amplitude de l'onde
        sens = vers le haut ou vers le bas
        draw = 1 pour réellement dessiner la courbe
        '''

        self.start = int(start)
        self.gap = int(gap)
        self.ampli = int(ampli)

        if sens not in [0, 1]:
            self.sens = 1
        else:
            self.sens = sens

        # Tous les points devront être corrigés de O(Ox, Oy)
        self.O = O

        self.set_ABC()

    def set_ABC(self):
        '''Les points sont comptés à partir de O'''

        self.A = (self.start, 0)

        if self.sens:
            self.B = (int(self.start + self.gap/2), - self.ampli)
        else:
            self.B = (int(self.start + self.gap/2), self.ampli)

        self.C = (self.start + self.gap, 0)

    def get_3_line(self):
        '''Droite de A à B et de B à C'''

        a = t_s(self.A, self.O)
        b = t_s(self.B, self.O)
        c = t_s(self.C, self.O)

        # Droite de A à B
        line1 = get_line(a, b)
        # Droite de B à C
        line2 = get_line(b, c)

        # La liste des points des 2 lignes
        line = line1 + line2

        return line

    def draw_half_wave(self, img):
        '''Droite de A à B et de B à C'''

        a = t_s(self.A, self.O)
        b = t_s(self.B, self.O)
        c = t_s(self.C, self.O)

        # Droite de A à B
        img= draw_line(img, a, b)
        # Droite de B à C
        img= draw_line(img, b, c)

        return img


class Wave(dict):
    '''Onde de n demi-sinusoïdal static
    self hérite de dict: attributs et méthodes
    n maxi 10
    Les points sont les sommets de chaque demi-sinusoïdale
    line = liste des points d'une demi-sinusoïdales
    lines = liste des tous les points de toutes les demi-sinusoïdales
    '''

    def __init__(self, O, n, start, gap, ampli):
        super().__init__()

        self.O = O
        self.n = n
        self.start = start
        self.gap = gap
        self.ampli = ampli
        self.forme = 0.6

        # Les points sommets de toutes les demi-sinusoïdales
        wave_points = self.get_wave_points()

        for i in range(self.n):
            if i % 2 == 0:
                sens = 0
            else:
                sens = 1

            # O, start, gap, ampli, sens=0
            self[i] = HalfWave( self.O,
                                wave_points[i][0],
                                wave_points[i][1],
                                self.ampli*self.forme**i,
                                sens )

    def get_wave_points(self):
        start = self.start
        gap = self.gap

        points = [(start, gap)]
        for i in range(self.n-1):
            toto = points[i][0] + points[i][1], gap*(1-0.1*(i+1))
            points.append(toto)

        return points

    def get_lines(self):
        '''Retourne l'image avec le dessin des points,
        et crée la liste des points de toutes les courbes.'''

        lines = []
        for i in range(self.n):
            line = self[i].get_3_line()
            lines = lines + line

        return lines

    def draw_waves(self, img):
        '''Retourne l'image avec le dessin des points,
        et crée la liste des points de toutes les courbes.'''

        for i in range(self.n):
            img = self[i].draw_half_wave(img)

        return img


class StaticBang:
    '''Chaque point de Wave devient un cercle de couleur de l'amplitude.'''

    def __init__(self, O, n, start, gap, ampli, pixel):
        '''points = liste de point (x, y).
        O centre
        n nombre de demi-sinusoïdales
        start point A = début par rapport à O
        gap ecart entre A et C
        ampli amplitude de la première demi-sinusoïdales
        pixel epaisseur des cercles
        '''

        self.O = O
        self.n = n
        self. start = start
        self.gap = gap
        self.ampli = ampli
        self.pixel = pixel
        self.get_lines()

    def get_lines(self):
        self.sinus = Wave(  self.O,
                            self.n,
                            self. start,
                            self.gap,
                            self.ampli)

        self.lines = self.sinus.get_lines()

    def draw_opencv_circle(self, img, C, color, radius):

        centre = tuple(C)
        thickness = self.pixel

        # antialiased line
        lt = cv2.LINE_4

        img = cv2.circle(img, centre, radius, color, thickness, lineType=lt)

        return img

    def lines_to_circle(self, img):
        #print("len(self.lines)", len(self.lines))
        for point in self.lines:
            x = point[0]
            y = point[1]
            if self.ampli != 0:
                color = abs(y - self.O[1])/(self.ampli) * 255
                color = min(color, 255)
                color = max(color, 0)
                color = int(color)
            else:
                color = 0

            ##if color == 0:
                ##color = 50

            if x % self.pixel == 0:
                radius = int(x - self.O[0])
                img = self.draw_opencv_circle(img, self.O, color, radius)

        return img


class DynamicBang:
    '''Les cercles créés par StaticBang explosent !!'''

    def __init__(self, O, n, start, gap, ampli, pixel, slide, decrease):

        self.O = O
        self.n = n
        self.start = start
        self.gap = gap
        self.ampli = ampli
        self.pixel = pixel
        self.slide = slide
        self.t_zero = time()
        self.decrease = decrease

    def get_lines_at_t(self):

        delta_t = time() - self.t_zero

        # Glissement=slide du point origine
        self.O[0] += int((self.slide[0])*delta_t)
        self.O[1] += int((self.slide[1])*delta_t)
        C = [self.O[0], self.O[1]]

        # Décroissance du bang
        self.start += (self.slide[1]/60)*delta_t
        self.gap   -= (self.slide[1]/60)*delta_t
        self.ampli = self.ampli - (self.decrease/30)*delta_t

        # self.ampli = 0 va provoquer le del dans BANGS
        if self.ampli < 0:
            self.ampli = 0
            #os._exit(0)

        self.static_bang = StaticBang(  C,
                                        self.n,
                                        self.start,
                                        self.gap,
                                        self.ampli,
                                        self.pixel)

        return self.static_bang.lines

    def get_bang_img(self, img):

        lines = self.get_lines_at_t()
        img = self.static_bang.lines_to_circle(img)
        #print("get_bang_img dans DynamicBang")
        return img


class Bangs:
    '''Affichage de plusieurs bangs dans une image avec OpenCV.'''

    comptage = -1

    def __init__(self, bang_list):

        self.bang_list = bang_list

    def update_freq(self):
        '''Calcul et affichage du fps.'''

        self.freq += 1

        if time() - self.t_zero > 1:
            self.t_zero = time()
            print("Fréquence =", self.freq)
            self.freq = 0

    def create_bang(self, bang, numero):
        '''Création d'un bang et gestion avec BANGS'''

        global BANGS

        n           = bang["n"]
        O           = bang["O"]
        start       = bang["start"]
        gap         = bang["gap"]
        ampli       = bang["ampli"]
        pixel       = bang["pixel"]
        slide       = bang["slide"]
        decrease    = bang["decrease"]

        # Création d'une bang
        # Lancé à BANGS[numero].t_zero
        BANGS[numero] = DynamicBang(O, n, start, gap, ampli,
                                    pixel, slide, decrease)
        print("Lancement de DynamicBang pour", BANGS[numero], "numero", numero)

    def get_image(self):
        '''Retourne l'image avec les cercles de tous les bangs en cours.'''

        global BANGS

        img = get_black_image()
        key_list_to_remove = []

        for k, v in BANGS.items():
            #print("get_image pour ", k, v)
            img = BANGS[k].get_bang_img(img)

            # Suppression des bangs finis si ampli=0
            if v.ampli == 0:
                print("BANGS[{}] à supprimer: {}".format(k, v))
                key_list_to_remove.append(k)

        # Interdiction de supprimer une clé en cours de parcours
        for i in key_list_to_remove:
            print("Suppression du BANGS[{}]".format(i))
            del BANGS[i]

        return img

    def bangs_government(self):
        '''A chaque nouvelle image, relit la liste des bangs pour lancer
        les nouveaux bangs arrivés dans la liste self.bang_list
        '''

        global BANGS

        bang_to_remove = []
        for bg in self.bang_list:
            # Comptage des bangs
            Bangs.comptage += 1
            numero = Bangs.comptage

            # Création du bang avec DynamicBang
            print("Création du bang numéro:", numero)
            self.create_bang(bg, numero)

            # Le bang est lancé, on ne veut plus le voir
            bang_to_remove.append(bg)

        # Supprression des bangs lancés
        for b in bang_to_remove:
            print("Suppression du bang:", b)
            self.bang_list.remove(b)

    def frame_update(self):
        '''Maj à chaque frame'''

        # Toujours cette emprise étatique et colbertienne
        self.bangs_government()

        # Recalcul de l'image à partir de 0 avec toutes les lines
        img = self.get_image()

        return img


class Display(Bangs):
    def __init__(self, bang_list):
        super().__init__(bang_list)

        # La boucle d'affichage
        self.loop = 1
        # Calcul du fps
        self.t_zero = time()
        self.freq = 0

        # Lancement de la fenêtre OpenCV
        self.display_thread()

    def display(self):

        while self.loop:
            self.update_freq()

            #print("update img")
            img = self.frame_update()

            cv2.imshow("Ceci n'est pas une image", img)

            # wait for esc key to exit
            key = np.int16(cv2.waitKey(1))
            if key == 27:  # Echap
                break

        cv2.destroyAllWindows()

    def display_thread(self):
        '''Lancement du thread d'affichage OpenCV'''

        print("Lancement du thread d'affichage OpenCV")
        thread_d = threading.Thread(target=self.display)
        thread_d.start()


def t_s(a, b):
    return tuple(map(operator.add, a, b))

def get_droite_coeff(x1, y1, x2, y2):

    if x2 - x1 != 0:
        a = (y2 - y1) / (x2 - x1)
        b = y1 - a * x1
    else:
        a, b = None, None

    return a, b

def draw_line(img, A, B):
    '''Retourne l'image avec le dessin de la droite entre A et B.'''

    a, b = get_droite_coeff(A[0], A[1], B[0], B[1])

    for i in range(int(A[0]), int(B[0])):
        x = i
        y = int(a*x + b)
        if 0 < x < LARG and 0 < y < HAUT:
            img[y][x] = [255]

    return img

def get_line(A, B):
    '''Retourne la liste des points de cette droite'''

    a, b = get_droite_coeff(A[0], A[1], B[0], B[1])

    points = []
    for i in range(int(A[0]), int(B[0])):
        x = i
        y = int(a*x + b)
        if 0 < x < LARG and 0 < y < HAUT:
            points.append([x, y])

    return points

def test_halfwave():
    print("Test de HalfWave")
    O, start, gap, ampli, sens = [300, 500], 100, 500, 300, 1
    hw = HalfWave(O, start, gap, ampli, sens)
    img = get_black_image()
    img = hw.draw_half_wave(img)

    toto = 1
    t = time()
    while toto:
        cv2.imshow("Ceci n'est pas une image", img)

        if time() - t > 1:
            toto = 0

        # wait for esc key to exit
        key = np.int16(cv2.waitKey(5))
        if key == 27:  # Echap
            break

    cv2.destroyAllWindows()

def test_wave():
    print("Test de Wave")
    O, n, start, gap, ampli =[60, 500], 12, 30, 90, 250
    w = Wave(O, n, start, gap, ampli)
    img = get_black_image()
    img = w.draw_waves(img)

    toto = 1
    t = time()
    while toto:
        cv2.imshow("Ceci n'est pas une image", img)

        if time() - t > 1:
            toto = 0

        # wait for esc key to exit
        key = np.int16(cv2.waitKey(5))
        if key == 27:  # Echap
            break

    cv2.destroyAllWindows()

def test_staticbang():
    O, n, start, gap, ampli, pixel = [600, 400], 6, 30, 70, 200, 1

    sb = StaticBang(O, n, start, gap, ampli, pixel)
    img = get_black_image()
    img = sb.lines_to_circle(img)

    toto = 1
    t = time()
    while toto:
        cv2.imshow("Ceci n'est pas une image", img)

        if time() - t > 100:
            toto = 0

        # wait for esc key to exit
        key = np.int16(cv2.waitKey(5))
        if key == 27:  # Echap
            break

    cv2.destroyAllWindows()

def test_dynamicbang():
    print("Test de DynamicBang")
    O, n, start, gap, ampli, pixel = [100, 200], 8, 50, 100, 300, 2
    slide, decrease = (10, 10), 10
    db = DynamicBang(O, n, start, gap, ampli, pixel, slide, decrease)

    toto = 1
    t = time()
    while toto:
        img = get_black_image()
        img = db.get_bang_img(img)

        cv2.imshow("Ceci n'est pas une image", img)

        if time() - t > 2:
            toto = 0

        # wait for esc key to exit
        key = np.int16(cv2.waitKey(66))
        if key == 27:  # Echap
            break

    cv2.destroyAllWindows()

def test_bangs():
    print("Test de Bangs")
    bang_list = [{   "n":        8,
                    "O":        [200, 400],
                    "start":    20,
                    "gap":      4,
                    "ampli":    6,
                    "pixel":    2,
                    "slide":    (0.1, 1),
                    "decrease": 10  },
                {   "n":        5,
                    "O":        [600, 800],
                    "start":    50,
                    "gap":      8,
                    "ampli":    10,
                    "pixel":    2,
                    "slide":    (1, -1),
                    "decrease": 10   },
                {   "n":        3,
                    "O":        [300, 300],
                    "start":    50,
                    "gap":      4,
                    "ampli":    15,
                    "pixel":    2,
                    "slide":    (1, 0),
                    "decrease": 20   }]

    liste_de_bang_initiale = [bang_list[0]]
    bangs = Display([])

    print("Lancement de nouveau bang")

    t = time()
    ok1, ok2, ok3 = 1, 1, 1

    while 1:
        if time() - t > 1 and ok1 == 1:
            print("bang 1")
            bangs.bang_list.append(bang_list[0])
            ok1 = 0

        elif time() - t > 5 and ok2 == 1:
            print("bang 2")
            bangs.bang_list.append(bang_list[1])
            ok2 = 0

        elif time() - t > 6 and ok3 == 1:
            print("bang 3")
            bangs.bang_list.append(bang_list[2])
            ok3 = 0

        elif time() - t > 10:
            print("Relance")
            print("La liste doit être vide", bangs.bang_list)
            # fin du thread
            #bangs.loop = 0
            t = time()
            ok1, ok2, ok3 = 1, 1, 1

def test_global():
    test_halfwave()
    test_wave()
    test_staticbang()
    test_dynamicbang()
    test_bangs()

if __name__ == "__main__":
    test_global()
