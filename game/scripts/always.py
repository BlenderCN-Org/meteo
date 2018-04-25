#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

## always.py

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

"""
A partir de la 61ème frame, lancé à chaque frame durant tout le jeu.

Ajout d'objets
Ne marche qu'avec une seule scène, qui sera la scène courante.
L'object ajouté est simplement défini par son nom, pas besoin de récupérer
l'objet lui-même.

https://www.blender.org/api/blender_python_api_2_67_1/bge.types.KX_Scene.html
addObject(object, other, time=0)
    Adds an object to the scene like the Add Object Actuator would.
    Parameters:
        object (KX_GameObject or string) – The object to add
        other (KX_GameObject or string) – The object’s center to use
                                            when addind the object
        time (integer) – The lifetime of the added object, in frames.
                         A time of 0 means the object will last forever.

    Returns:    The newly added object.
"""


from time import sleep
from datetime import timedelta

from bge import logic as gl
from bge import events

from scripts.labtools import labgetobject as get_obj
from scripts import icons


def main():
    # Maj de toutes les tempos
    gl.tempoDict.update()

    # Maj entrée clavier
    keys()

    game = get_obj.get_scene_with_name("Game")
    if game:
        game_obj = game.objects

    # Init ["always"] = 0 pour once.py
    if gl.tempoDict["always"].tempo == 1:
        print("Initialisation de always.py")

        # Reset pour la suite
        gl.tempoDict["day"].unlock()
        gl.tempoDict["day"].tempo = -1  # jolie bidouille

        # Traits verticaux du histo avec date
        traits_display(game_obj)
        print("Initialisation ok\n")

    # ensuite toujours à partir de 1
    else:
        if gl.tempoDict["day"].tempo == 0:

            # Maj de gl.day_number
            set_day_number(game_obj)
            gl.icon_index = -1

            # Pour text
            set_resolution_visible(game_obj)
            update_chronologic_histo(game_obj)
            icons.main(game_obj)
            set_spread(game_obj)
            # au changement de jour
            play_note()
        else:
            # à chaque changement d'icone
            icons.icons_note()

def update_chronologic_histo(game_obj):
    """Affichge des temp mini et maxi positionné en horizontal par rapport
    à un point fixe à droite, le jour affiché=current_day à 23h.
    """

    # pour ajout des objets
    empty = game_obj["Empty"]
    scene = gl.getCurrentScene()

    # data du jour courant
    datas = gl.chronologic[gl.day_number]
    datas.sort()

    life =  gl.time - gl.correction

    for val in datas:
        if val:
            # 6/336 = 0,017857
            X = 0.017857 * val[0] + 33.0

            # Ajout des minis
            Z = -0.90
            indice = 0
            add_rose(val, empty, scene, X, Z, life, indice)

            # Ajout des maxis
            Z = 0.52
            indice = 1
            add_rose(val, empty, scene, X, Z, life, indice)

def add_rose(val, empty, scene, X, Z, life, indice):
    """Ajout des minis ou des maxis"""

    empty.worldPosition = (X, 0, Z)
    obj_added = scene.addObject("rose", empty, life)

    larg = 0.01

    if val and val[2]:
        if val[2][indice]:
            sz = val[2][indice]/10
            if -0.001 < sz < 0.001:
                sz = 0.006
            obj_added.worldScale = (larg, 0, sz)
        else:
            obj_added.worldScale = (larg, 0, 0.006)
    else:
        obj_added.worldScale = (larg, 0, 0.006)

def traits_display(game_obj):
    # pour ajout des objets
    empty = game_obj["Empty"]
    scene = gl.getCurrentScene()

    # les 15 traits verticaux
    for i in range(15):
        X = 0.428*i + 27.00
        empty.worldPosition = (X, 0.1, 0)
        obj_added = scene.addObject("gris5", empty, 0)
        obj_added.worldScale = (0.02, 0, 4)

def set_day_number(game_obj):
    """Toutes les gl.frame,
    récup et affichage des prévisions d'un nouveau jour,
    pour histogramm dynamic.
    """

    # Bidouille pour partir à and de once.py
    if gl.tempoDict["always"].tempo == 1:
        gl.day_number -= 1

    if not gl.manual:
        gl.day_number += 1

    pretty_date_display(game_obj)

    if gl.day_number < len(gl.days):
        print("\nJour en cours {} numéro {} ".format(gl.current_day,
                                                        gl.day_number))
    else:
        gl.day_number = 0

def pretty_date_display(game_obj):
    if gl.day_number < len(gl.days):
        # Set du  jour en cours, soit "2017_06_15"
        gl.current_day = gl.days[gl.day_number]

        # Affichage du jour en cours
        gl.jour = pretty_date(gl.current_day)
        game_obj["day.001"]["Text"] = pretty_date(gl.current_day)

def set_spread(game_obj):
    spread = [[0,0], [0,0], [0,0]]

    mini = []
    maxi = []

    if gl.day_number < len(gl.days):
        for val in gl.chronologic[gl.day_number]:
        # k = int, v = [None] ou [(-161, '2017_09_16_06', [-1, -2, -2]), ....
            try:
                mini.append(val[2][0])
                maxi.append(val[2][1])
            except:
                mini.append(0)
                maxi.append(0)

        mini.sort()
        spread[0][0] = mini[0]
        spread[0][1] = mini[-1]

        maxi.sort()
        spread[1][0] = maxi[0]
        spread[1][1] = maxi[-1]

    game_obj["mini mini"]["Text"] = spread[0][0]
    game_obj["mini maxi"]["Text"] = spread[0][1]

    game_obj["maxi mini"]["Text"] = spread[1][0]
    game_obj["maxi maxi"]["Text"] = spread[1][1]

    gl.note =   abs(spread[0][0]) + abs(spread[0][1]) \
                + abs(spread[1][1]) + abs(spread[1][1])

def keys():

    if gl.keyboard.events[events.SPACEKEY] == gl.KX_INPUT_JUST_ACTIVATED:
        # Space pour faire pause
        if gl.manual == 0:
            gl.manual = 1
        else:
            gl.manual = 0
        sleep(0.1)

    if gl.keyboard.events[events.UPARROWKEY] == gl.KX_INPUT_JUST_ACTIVATED:
        # UP pour avancer dans les jours
        gl.day_number += 1

        if gl.day_number >= len(gl.days):
            gl.day_number = 0

        print("day number", gl.day_number)

        # Reset
        gl.tempoDict["day"].tempo = -1
        sleep(0.1)

    if gl.keyboard.events[events.DOWNARROWKEY] == gl.KX_INPUT_JUST_ACTIVATED:
        # DOWN pour reculer dans les jours
        gl.day_number -= 1

        if gl.day_number < 0:
            gl.day_number = 0

        print("day number", gl.day_number)

        # Reset
        gl.tempoDict["day"].tempo = -1
        sleep(0.3)

    if gl.keyboard.events[events.LEFTARROWKEY] == gl.KX_INPUT_JUST_ACTIVATED:
        # DOWN pour reculer dans les jours
        gl.day_number -= 10

        if gl.day_number < 0:
            gl.day_number = 0

        print("day number", gl.day_number)

        gl.tempoDict["day"].periode = gl.day_frame
        gl.tempoDict["day"].tempo = -1

    if gl.keyboard.events[events.RIGHTARROWKEY] == gl.KX_INPUT_JUST_ACTIVATED:
        # DOWN pour reculer dans les jours
        gl.day_number += 10

        if gl.day_number < 0:
            gl.day_number = 0

        print("day number", gl.day_number)

        if gl.day_frame < 0: gl.day_frame = 0
        gl.tempoDict["day"].periode = gl.day_frame
        gl.tempoDict["day"].tempo = -1

def play_note():
    """Joue la note au changement de jour,
    somme des valeurs absolues des écarts
    """

    note = gl.note
    note = int(note*36/30)
    if 0 <= note < 36:
        print("Note spread du jour:", note)
        note = str(note)
        gl.sound[note].play()

def pretty_date(date):
    """Retourne une date à la française"""

    return gl.meteo_tools.get_pretty_date(date)

def set_resolution_visible(game_obj):
    for o in game_obj:
        try:
            o.visible = True
        except:
            pass

    # Le cube avec logo reste invisible
    game_obj["Cube"].visible = False

    for o in game_obj:
        try:
            if o["Text"]:
                o.resolution = 32
        except:
            pass
