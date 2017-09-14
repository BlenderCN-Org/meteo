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
from bge import logic as gl

from scripts.meteo_tools import MeteoTools
from scripts.labtools.labconfig import MyConfig
from scripts.labtools.labtempo import Tempo
from scripts.labtools.labsound import EasyAudio

def get_conf():
    '''Récupère la configuration depuis le fichier *.ini.'''

    # Le dossier courrant est le dossier dans lequel est le *.blend
    current_dir = gl.expandPath("//")
    print("Dossier courant depuis once.py {}".format(current_dir))
    # /media/data/3D/projets/meteo/game/

    # TODO: trouver le *.ini en auto
    gl.ma_conf = MyConfig(current_dir + "scripts/bgb.ini")
    gl.conf = gl.ma_conf.conf

    print("\nConfiguration du jeu bgb:")
    print(gl.conf, "\n")

    # Le fichier meteo à lire à mettre dans scripts
    gl.fichier = current_dir + gl.conf["file"]["fichier"]

def set_gris_table():
    '''Table des objets blender plan en gris.'''
    gl.gris_table = ["gris0", "gris1", "gris2", "gris3", "gris4", "gris5",
                     "gris6","gris7", "gris8", "gris9", "gris10"]

def variable_init():

    gl.pause = 0

    # Nombre de barres histogramme
    gl.num = 3
    gl.histo_mini = [0]*50
    gl.histo_maxi = [0]*50
    gl.histo_temps = [0]*50

    lenteur = gl.conf["rythm"]["lenteur"]
    # Nombre de frame pour affichage des prévisions d'un jour
    gl.day_frame = 360 * lenteur

    # Dict des plages des mini, maxi, temps pour un jour à afficher
    #                        valeur haute, valeur basse
    gl.plages = {   "mini":  [0,           0],
                    "maxi":  [0,           0],
                    "temps": [0,           0]}

def set_tempo():
    tempo_liste = [("always", -1), ("print", 60), ("day", gl.day_frame)]
    gl.tempoDict = Tempo(tempo_liste)
    gl.tempoDict["day"].lock()
    gl.tempoDict["print"].lock()

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

def get_gapsploitation():
    gl.meteo_tools = MeteoTools()
    gl.meteo_data = gl.meteo_tools.get_json_file(gl.fichier)
    print("Fichier meto {}".format(gl.fichier))

def get_days():
    '''Défini tous les jours pour lesquels il y a des prévisions.'''

    # Le numéro du jour en cours dans la liste des jours
    gl.day_number = 0

    # Le jour en cours
    gl.current_day = "2017_06_11"
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

    print("\nNombre de jours avec prévisions:", len(gl.days))

def audio_init():
    soundList = []
    path = "//samples/"
    for i in range(36):
        soundList.append(str(i))
    gl.sound = EasyAudio(soundList, path)

def main():
    '''Lancé une seule fois à la 1ère frame au début du jeu par main_once.'''

    print("Initialisation des scripts lancée un seule fois au début du jeu.")

    get_conf()

    var_from_ini()

    variable_init()

    set_tempo()

    set_gris_table()

    get_gapsploitation()
    get_days()

    audio_init()

    # Pour les mondoshawan
    print("ok once.py")
