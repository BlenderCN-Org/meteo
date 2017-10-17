#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

## icons.py

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


from time import sleep
from bge import logic as gl
from bge import events
from scripts.labtools import labgetobject as get_obj


"""
Pour la clé: "2017_06_12":
la valeur est:
data = {
"2017_06_11_21": [0, 1, "soleil"],
"2017_06_12_13": [-1, 0, "soleil"],
"2017_06_12_12": [-1, 0, "soleil"]}
"""

ICONS = [   "soleil",
            "ciel_voile",
            "eclaircie",
            "tres_nuageux",
            "brouillard",
            "brouillard_givrant",
            "pluie_faible",
            "pluies_orageuses",
            "pluie_eparse",
            "pluie_averses",
            "pluie_verglassante",
            "pluie_forte",
            "quelques_flocons",
            "pluie_et_neige",
            "neige",
            "neige_forte",
            "risque_de_grele",
            "orages",
            "risque_d_orages",
            None]


def main(game_obj):
    data = get_day_data()
    gl.icons_list = get_icons(data)
    set_icon_position(gl.icons_list, game_obj)

def get_day_data():
    """[(-23, '2017_06_12_00', [0, 1, 'soleil']),
        (-19, '2017_06_12_04', [0, 1, 'soleil']),
        (-20, '2017_06_12_03', [0, 1, 'soleil']), etc ....]
    """

    return gl.chronologic[gl.day_number]

def get_icons(data):
    """Je récupère les type de temps à 14 h

    Si gl.current_day = "2017_06_12"

    je veux l'icone de
        2017_06_11_14
        2017_06_10_14
        2017_06_09_14
        etc ....
    dans une liste [ ("2017_06_12", "soleil"),
                     ("2017_06_11_14", "soleil"),
                     (2017_06_10_14, "ciel_voile")
                     , etc ....]
    classé de j à j -14
    """

    icons_list = []
    if data:
        for tup in data:
            if tup[1][-3:] == "_14":
                try:
                    icons_list.append((tup[1][:-3], tup[2][2]))
                except:
                    icons_list.append((tup[1][:-3], None))

    icons_list.sort()

    icons_list = icons_list_completion(icons_list)

    return icons_list

def get_fourteen_days_before():
    """ si gl.current_day = 2017_10_06
    les 13 jours précédents sont
    2017_10_05, 2017_10_04, ....., 2017_10_01, 2017_09_30, ....
    """

    # today = 2017-07-29 01:00:00
    real = gl.meteo_tools.get_real_date_time(gl.current_day + "_00_01")
    thirteen_days = gl.meteo_tools.get_thirteen_days_before(real)

    thirteen_days.insert(0, gl.current_day)
    fourteen_days = thirteen_days
    fourteen_days.reverse()

    return fourteen_days

def icons_list_completion(icons_list):
    """len de = 14 icons_list en ajoutant le jour courrant."""

    fourteen_days = get_fourteen_days_before()
    icons_list_new = [None]*14

    for i in range(14):
        icons_list_new[i] = (fourteen_days[i], None)

        for d in icons_list:
            if d[0] == fourteen_days[i]:
                icons_list_new[i] = d

    return icons_list_new

def set_icon_position(icons_list, game_obj):
    """ Z = 0
        Y = 0
        X de 27 à 33 pour 14 icones
        14 intervales
        6/14 = 0.42857
    """


    # pour ajout des objets
    empty = game_obj["Empty"]
    scene = gl.getCurrentScene()

    Y = 0
    Z = -0.2
    life =  gl.time - gl.correction

    for i in range(len(icons_list)):
        X = 33 - i*0.42857 - 0.42857/2

        empty.worldPosition = (X, Y, Z)

        icon = icons_list[len(icons_list) -i -1][1]
        if icon:
            obj_added = scene.addObject(icon, empty, life)
            obj_added.worldScale = (1,1,1)

def icons_note():
    if gl.tempoDict["note"].tempo == 5:
        # len de gl.icons_list=14, gl.icon_index=maxi 13
        if gl.icon_index < 14:
            current_icon = gl.icons_list[gl.icon_index][1]
            note = ICONS.index(current_icon)

            if gl.current_note != note:
                if 0 <= note < 36:
                    new_note = str(note + 15)
                    print("Note des icones:", new_note, current_icon)
                    gl.sound[new_note].play()

            gl.current_note = note

            gl.icon_index += 1
