#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

## once.py

#############################################################################
# Copyright (C) Labomedia June 2017
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


# Ce script est appelé par main_init.main dans blender
# Il ne tourne qu'une seule fois pour initier las variables
# qui seront toutes des attributs du bge.logic (gl)
# Seuls les attributs de logic sont stockés en permanence.


import numpy as np
from collections import OrderedDict

from bge import logic as gl

from scripts.meteo_tools import MeteoTools
from scripts.labtools.labconfig import MyConfig
from scripts.labtools.labtempo import Tempo
from scripts.labtools.labsound import EasyAudio


def main():
    """Lancé une seule fois à la 1ère frame au début du jeu par main_once."""

    print("Initialisation des scripts lancée un seule fois au début du jeu.")

    # Récupére
    get_conf()
    var_from_conf()

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

    get_one_day_gap()
    get_seven_days_gap()

    # Audio
    audio_init()

    # Pour les mondoshawan
    print("Excécution de once.py terminée")


def var_from_conf():
    gl.control = gl.conf["test"]["control"]

    gl.time = gl.conf["rythm"]["time"]
    # Nombre de frame pour affichage des prévisions d'un jour
    gl.day_frame = gl.time


def set_chronologic():
    '''Crée un dict gl.chronologic
    la clé crée l'ordre
    Le nombre de clés = nombre de jours = len(gl.days)

    valeur = dict non ordonné, les barres de l'histogramme ne sont pas créées
    par ordre chronologique, seul l'affichage global compte !

    gl.chronologic =
    {0: [None],
            26=nombre d'heures avant le curent day
     1: [   (-26, '2017_06_11_21', [0, 1, 0]),
            (-27, '2017_06_11_20', [0, 1, 0]),
             .... ],
     2: [....}
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


def get_one_day_gap():
    '''168 heures avant le jour courrant'''

    somme = 0
    p = 0
    for i in range(len(gl.chronologic)):
        for gap in gl.chronologic[i]:
            try:
                if gap[0] == -24:
                    p += 1
                    somme += abs(gap[2][1])
            except:
                pass

    print("\n", "Nombre de jours avec écart à 1 jours:", p)
    print("Somme des écarts à 1 jours:", somme)
    print("Moyenne des écarts à 1 jours", somme / p, "\n")


def get_seven_days_gap():
    '''168 heures avant le jour courrant'''

    somme = 0
    p = 0
    for i in range(len(gl.chronologic)):
        for gap in gl.chronologic[i]:
            try:
                if gap[0] == -168:
                    p += 1
                    somme += abs(gap[2][1])
            except:
                pass

    print("Nombre de jours avec écart à 7 jours:", p)
    print("Somme des écarts à 7 jours:", somme)
    print("Moyenne des écarts à 7 jours", somme / p, "\n")


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
                     "gris6", "gris7", "gris8", "gris9", "gris10"]


def variable_init():
    gl.manual = 0
    gl.restart = 0
    gl.note = 0

    # Nombre de barres histogramme
    gl.num = 50
    gl.histo_mini = [0] * gl.num
    gl.histo_maxi = [0] * gl.num
    gl.histo_temps = [0] * gl.num

    # Dict des plages des mini, maxi, temps pour un jour à afficher
    #                        valeur haute, valeur basse
    gl.plages = {"mini" : [0, 0],
                 "maxi" : [0, 0],
                 "temps": [0, 0]}

    # pour date_histo
    gl.obj_list = []
    gl.jour = "0"


def set_tempo():
    tempo_liste = [("always", -1),
                   ("print", 60),
                   ("day", gl.day_frame),
                   ("note", int(gl.time / 14))]

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

    print("\n\nNombre de jours avec prévisions y compris les None:", len(gl.days))


def audio_init():
    soundList = []
    path = "//samples/"

    for i in range(36):
        soundList.append(str(i))

    gl.sound = EasyAudio(soundList, path)

    # la note des icones en cours
    gl.note_index = 0
    gl.icons_list = [0] * 14
    gl.current_note = 0
