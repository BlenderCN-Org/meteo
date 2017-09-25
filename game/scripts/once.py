#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

## once.py

#############################################################################
# Copyright (C) Labomedia November 2012
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franproplin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
#############################################################################

'''
Ce script est appelé par main_init.main dans blender
Il ne tourne qu'une seule fois pour initier las variables
qui seront toutes des attributs du bge.logic (gl)
Seuls les attributs de logic sont stockés en permanence.

Un thread est crée pour recevoir le multicast, puis après avoir reçu l'adresse
ip du serveur sur ce multicast, lancement d'un socket TCP pour envoyer.

'''


import numpy as np
from collections import OrderedDict

from bge import logic as gl

from scripts.meteo_tools import MeteoTools
from scripts.labtools.labconfig import MyConfig
from scripts.labtools.labtempo import Tempo
from scripts.labtools.labsound import EasyAudio


def main():
    '''Lancé une seule fois à la 1ère frame au début du jeu par main_once.'''

    print("Initialisation des scripts lancée un seule fois au début du jeu.")

    # Récupére
    get_conf()
    var_from_ini()
    # Défini des variables
    variable_init()

    # Défini les tempo, les gris
    set_tempo()
    set_gris_table()

    # Récupére les datas dans le fichier gaps.txt
    # Défini gl.meteo_data
    get_gaps_file()

    # Défini gl.days, liste des jours triés
    get_days()

    # Crée le dict ordonné gl.chronologic
    set_chronologic()

    # Audio
    audio_init()

    # Pour les mondoshawan
    print("Excécution de once.py terminée")

def var_from_ini():
    '''Les pixels sont carrées.'''

    # TODO mettre dans ini
    gl.wide = 6 # largeur de l'écran en unité blender
    gl.L = 125  #125  # nombre de pixels en largeur
    gl.H = 70  #70  # nombre de pixels en hauteur
    gl.nb = gl.L * gl.H
    gl.largeur_pixel = gl.wide / gl.L
    gl.size = gl.largeur_pixel
    # Je pense que ça décale un peu les pixels par rapport
    # au bord inférieur gauche de la vue caméra
    gl.origin = (gl.size/2, gl.size/2)

    '''print(  "gl.size", gl.size,
            ##"gl.nb", gl.nb,
            ##"gl.origin", gl.origin,
            ##"gl.largeur_pixel", gl.largeur_pixel)'''

def set_chronologic():
    '''Crée un dict gl.chronologic
    la clé crée l'ordre
    Le nombre de clés = nombre de jours = len(gl.days)

    valeur = dict non ordonné, les barres de l'histogramme ne sont pas créées
    par ordre chronologique, seul l'affichage global compte !

    gl.chronologic[1] =
    [(-9, '2017_06_12_14', [-1, 0, 0]), (-6, '2017_06_12_17', [-1, 0, 0]), (-20, '2017_06_12_03', [0, 1, 0]), (0, '2017_06_12_23', [-1, -1, 0]), (-11, '2017_06_12_12', [-1, 0, 0]), (-25, '2017_06_11_22', [0, 1, 0]), (-17, '2017_06_12_06', [0, 0, 0]), (-26, '2017_06_11_21', [0, 1, 0]), (-22, '2017_06_12_01', [0, 1, 0]), (-2, '2017_06_12_21', [-1, -1, 0]), (-3, '2017_06_12_20', [-1, -1, 0]), (-29, '2017_06_11_18', [0, 1, 0]), (-19, '2017_06_12_04', [0, 1, 0]), (-5, '2017_06_12_18', [-1, -1, 0]), (-28, '2017_06_11_19', [0, 1, 0]), (-23, '2017_06_12_00', [0, 1, 0]), (-21, '2017_06_12_02', [0, 1, 0]), (-16, '2017_06_12_07', [0, 1, 0]), (-18, '2017_06_12_05', [0, 1, 0]), (-1, '2017_06_12_22', [-1, -1, 0]), (-4, '2017_06_12_19', [-1, -1, 0]), (-24, '2017_06_11_23', [0, 1, 0]), (-13, '2017_06_12_10', [-1, 0, 0]), (-8, '2017_06_12_15', [-1, 0, 0]), (-27, '2017_06_11_20', [0, 1, 0]), (-12, '2017_06_12_11', [-1, 0, 0]), (-14, '2017_06_12_09', [0, 1, 0]), (-15, '2017_06_12_08', [0, 1, 0]), (-7, '2017_06_12_16', [-1, 0, 0]), (-10, '2017_06_12_13', [-1, 0, 0])]
    '''

    # La clé fait l'ordre = int = cle
    gl.chronologic = {}

    cle = 0
    # Parcours de la liste des jours qui est sorted
    for day in gl.days:
        day_data = gl.meteo_data[day]

        # { 0: (hours, j_h, écarts)
        gl.chronologic[cle] = []

        try:
            for j_h, gap in day_data.items():
                hours = get_hour_gap(day, j_h)

                # Tuple car ne sera pas modifié
                gl.chronologic[cle].append((hours, j_h, gap))

        except:
            gl.chronologic[cle].append(None)

        cle += 1
    #print(gl.chronologic)

def get_hour_gap(current_day, day_hour):
    '''Retourne le nombre d'heures (int) entre jour courant à 23h et une
    date heure.
    '''

    hours = gl.meteo_tools.hours_between_date(current_day + "_23", day_hour)

    return hours

def get_conf():
    '''Récupère la configuration depuis le fichier *.ini.'''

    # Le dossier courrant est le dossier dans lequel est le *.blend
    # /media/data/3D/projets/meteo/game/
    current_dir = gl.expandPath("//")
    print("Dossier courant depuis once.py {}".format(current_dir))


    # TODO: trouver le *.ini en auto
    gl.ma_conf = MyConfig(current_dir + "scripts/bgb.ini")
    gl.conf = gl.ma_conf.conf

    print("\nConfiguration du jeu bgb:")
    print(gl.conf, "\n")

    # Le fichier des datas
    # /media/data/3D/projets/meteo/meteo_forecast/output/gapsploitation.txt
    # /media/data/3D/projets/meteo/game/
    gl.fichier = current_dir[:-5] + "meteo_forecast/output/" \
                                  + gl.conf["file"]["fichier"]

def set_gris_table():
    '''Table des objets blender plan en gris.'''
    gl.gris_table = ["gris0", "gris1", "gris2", "gris3", "gris4", "gris5",
                     "gris6","gris7", "gris8", "gris9", "gris10"]

def variable_init():

    gl.pause = 0
    gl.restart = 0

    # Nombre de barres histogramme
    gl.num = 50
    gl.histo_mini = [0]*gl.num
    gl.histo_maxi = [0]*gl.num
    gl.histo_temps = [0]*gl.num

    gl.time = gl.conf["rythm"]["time"]
    # Nombre de frame pour affichage des prévisions d'un jour
    gl.day_frame = gl.time

    # Dict des plages des mini, maxi, temps pour un jour à afficher
    #                        valeur haute, valeur basse
    gl.plages = {   "mini":  [0,           0],
                    "maxi":  [0,           0],
                    "temps": [0,           0]}

    # pour date_histo
    gl.obj_list = []
    gl.jour = "0"

def set_tempo():
    tempo_liste = [("always", -1), ("print", 60), ("day", gl.day_frame)]
    gl.tempoDict = Tempo(tempo_liste)
    gl.tempoDict["day"].lock()
    gl.tempoDict["print"].lock()

def get_gaps_file():
    gl.meteo_tools = MeteoTools()
    gl.meteo_data = gl.meteo_tools.get_json_file(gl.fichier)
    print("Fichier meto {}".format(gl.fichier))

def get_days():
    '''Défini tous les jours pour lesquels il y a des prévisions.'''

    # Le numéro du jour en cours dans la liste des jours
    # Dénini le numéro du 1er jour affiché
    gl.day_number = 0

    # la prévision affiché
    gl.lequel = 0
    gl.suivant = gl.day_frame
    gl.day_list = []

    # nouveau jour affiché
    gl.new_day = 1

    # La liste des jours
    gl.days = []

    for k, v in gl.meteo_data.items():
        gl.days.append(k)
    gl.days.sort()

    print("\n\nNombre de jours avec prévisions y compris les None:", len(gl.days))

def audio_init():
    soundList = []
    path = "//samples/"
    for i in range(36):
        soundList.append(str(i))
    gl.sound = EasyAudio(soundList, path)

