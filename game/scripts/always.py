#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

## always.py

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

################# Version pour histogram.blend #################


A partir de la 61ème frame, lancé à chaque frame durant tout le jeu.

### Ajout d'objets ###
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
'''


from time import time, sleep
from random import randint
from bge import logic as gl
from bge import events
from scripts.labtools import labgetobject as get_obj
import datetime

def main():
    keys()
    if not gl.pause:
        gl.tempoDict.update()

    game = get_obj.get_scene_with_name("Game")
    if game:
        game_obj = game.objects

    # ["always"] = 0 pour once.py
    if gl.tempoDict["always"].tempo == 1:
        initial_addition(game_obj)
        print("Initialisation de always")
        set_resolution_visible(game_obj)
        gl.tempoDict["day"].unlock()
        #Jolie bidouille
        gl.tempoDict["day"].tempo = -1
    else:
        if not gl.pause:
            if gl.tempoDict["day"].tempo == 0:
                set_resolution_visible(game_obj)
                get_day_data(game_obj)
                gl.lequel = 0

            # Toujours à partir de 1
            display_update(game_obj)
            histo_update(game_obj)
            set_spread(game_obj)

def keys():

    if gl.keyboard.events[events.SPACEKEY] == gl.KX_INPUT_JUST_ACTIVATED:
        # Space pour faire pause
        if gl.pause == 0:
            gl.pause = 1
        else:
            gl.pause = 0
        sleep(0.1)

    if gl.keyboard.events[events.UPARROWKEY] == gl.KX_INPUT_JUST_ACTIVATED:
        ##print("day_number", gl.day_number)
        ### UP pour avancer dans les jours
        ##gl.day_number += 1
        print("day_number", gl.day_number)
        # Reset
        gl.tempoDict["day"].tempo = -1
        sleep(0.1)

    if gl.keyboard.events[events.DOWNARROWKEY] == gl.KX_INPUT_JUST_ACTIVATED:
        # DOWN pour reculer dans les jours
        gl.day_number -= 2
        if gl.day_number < 0: gl.day_number = 0
        print("day_number", gl.day_number)
        # Reset
        gl.tempoDict["day"].tempo = -1
        sleep(0.3)

    if gl.keyboard.events[events.LEFTARROWKEY] == gl.KX_INPUT_JUST_ACTIVATED:
        # LEFT pour ralentir
        gl.day_frame += 360
        gl.tempoDict["day"].periode = gl.day_frame
        gl.tempoDict["day"].tempo = -1

    if gl.keyboard.events[events.RIGHTARROWKEY] == gl.KX_INPUT_JUST_ACTIVATED:
        # RIGHT pour accélérer
        gl.day_frame -= 360
        if gl.day_frame < 0: gl.day_frame = 0
        gl.tempoDict["day"].periode = gl.day_frame
        gl.tempoDict["day"].tempo = -1

def get_day_data(game_obj):
    '''Toutes les gl.frame,
    récup et affichage des prévisions d'un nouveau jour.
    '''

    if gl.day_number < len(gl.days):
        # Set du  jour en cours
        gl.current_day = gl.days[gl.day_number]

        # Affichage du jour en cours
        game_obj["day"]["Text"] = pretty_date(gl.current_day)
        game_obj["day.001"]["Text"] = pretty_date(gl.current_day)

        # Récup des datas du jour en cours
        # Dict des gaps pour le jour en cours
        gl.gaps = gl.meteo_data[gl.current_day]

        gl.day_list = []
        for k, v in gl.gaps.items():
            gl.day_list.append(k)
        gl.day_list.sort()
        print(  "Prévision du jour:", gl.current_day,
                "soit le jour", gl.day_number,
                "Nombre de prévisions:", len(gl.day_list))

        # Reset
        gl.counter = 0
        gl.plages = {   "mini":  [0,           0],
                        "maxi":  [0,           0],
                        "temps": [0,           0]}
    else:
         gl.restartGame()
    gl.day_number  += 1

def set_suivant(key1, key2):
    # le prochain sera à
    # Nombre d'heures entres 2 date du dict gl.gaps

    d = gl.meteo_tools.hours_between_date(key1, key2)
    gl.suivant = d * gl.tempoDict["day"].periode / 360

def set_origin():
    '''14 jours ou 336 h avant "2017_06_12"
    2017_06_12_16_59
    '''

    # Date reélle du jour courant
    real = gl.meteo_tools.get_real_date_time(gl.current_day + "_00_00")
    #print("jour courant =", real)  #2017-06-11 00:00:0
    # week_ago = today - datetime.timedelta(days=7)
    two_week_ago = real - datetime.timedelta(days=14)
    #print("Origine =", two_week_ago)  #2017-05-28 00:00:00
    gl.origin = gl.meteo_tools.get_date_hour_key_from_datetime(two_week_ago)

def display_update(game_obj):
    '''Pour un jour en cours, affichage successif des gaps de ce jour.
    le comptage dans cette phase d'affichage des prévisions pour un jour,
    est fait par la tempo "day"
                2017_06_12
    {
    '2017_06_12_00': [0, 1, 0],
    '2017_06_12_14': [0, 0, 0],
    '2017_06_11_18': [-1, 5, -8],
    '2017_06_12_11': [1, 1, 0]
    }
    ['2017_06_11_18', '2017_06_12_00', '2017_06_12_11', '2017_06_12_14']'''

    if gl.tempoDict["day"].tempo == 0:
        set_origin()
        k2 = gl.day_list[0]
        gl.suivant = 1
        print(  "Initialisation de", gl.current_day,
                "Origine", gl.origin)
    else:
        if gl.tempoDict["day"].tempo == gl.suivant:
            if gl.lequel != len(gl.day_list):
                k2 = gl.day_list[gl.lequel]
                set_suivant(gl.origin, k2)
                print(  "Numéro du jour joué", gl.lequel,
                        "Jour affiché", k2,
                        "Suivant =", gl.suivant)
                scale = get_scale(k2)
                scale_histo(game_obj, scale)
            gl.lequel += 1

def get_scale(day):
    # Récup du scale
    try:
        scale = gl.gaps[day]
    except:
        scale = [0, 0, 0]
    return scale

def scale_histo(game_obj, scale):
    '''Scale et position des barres.'''

    gl.plages["mini"][0] = max(scale[0], gl.plages["mini"][0])
    gl.plages["mini"][1] = min(scale[0], gl.plages["mini"][1])

    gl.plages["maxi"][0] = max(scale[1], gl.plages["maxi"][0])
    gl.plages["maxi"][1] = min(scale[1], gl.plages["maxi"][1])

    gl.plages["temps"][0] = max(scale[2], gl.plages["temps"][0])
    gl.plages["temps"][1] = min(scale[2], gl.plages["temps"][1])

    #note = scale[0] + scale[1] + scale[2]
    note = abs(scale[0]) + abs(scale[1]) + abs(scale[2])

    note = abs(note)
    note = int(note*36/30)
    if 0 <= note < 36:
        note = str(note)
        gl.sound[note].play()
        #print("note", note)

    # Set histo
    s0 = scale[0]/10
    s1 = scale[1]/10
    s2 = scale[2]/10

    if -0.01 < s0 < 0.01: s0 = 0.05
    if -0.01 < s1 < 0.01: s1 = 0.05
    if -0.01 < s2 < 0.01: s2 = 0.05

    game_obj["rose.001"].localScale = (1.0, 0, s0)
    game_obj["rose.002"].localScale = (1.0, 0, s1)
    game_obj["rose.003"].localScale = (1.0, 0, s2)

    # Set ampli
    m0 = gl.plages["mini"][0]/10
    M0 = gl.plages["mini"][1]/10
    game_obj["orange.001"].worldPosition[2] = m0
    game_obj[  "bleu.001"].worldPosition[2] = M0
    game_obj[ "mini haut"]["Text"] = gl.plages["mini"][0]
    game_obj[ "mini bas" ]["Text"] = gl.plages["mini"][1]

    m1 = gl.plages["maxi"][0]/10
    M1 = gl.plages["maxi"][1]/10
    game_obj["orange.002"].worldPosition[2] = m1
    game_obj[  "bleu.002"].worldPosition[2] = M1
    game_obj[ "maxi haut"]["Text"] = gl.plages["maxi"][0]
    game_obj[ "maxi bas" ]["Text"] = gl.plages["maxi"][1]

    m2 = gl.plages["temps"][0]/10
    M2 = gl.plages["temps"][1]/10
    game_obj["orange.003"].worldPosition[2] = m2
    game_obj[  "bleu.003"].worldPosition[2] = M2
    game_obj["temps haut"]["Text"] = gl.plages["temps"][0]
    game_obj["temps bas" ]["Text"] = gl.plages["temps"][1]

def pretty_date(date):
    '''Retourne une date à la française'''

    return gl.meteo_tools.get_pretty_date(date)

def print_fps():
    if gl.tempoDict["print"].tempo == 0:
        print(gl.getLogicTicRate())

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
            o.resolution = 32
        except:
            pass

def initial_addition(game_obj):
    '''Affichage initial des plans pour avoir x barres verticales roses.
    Le plan rose fait 1x1

    50 barres + 51 espaces = 101
    largeur des barres et des espaces
    0.033

    x de 17 to 23
    y = 0
    hauteur de -1.67 to 1.67
    '''

    empty = game_obj["Empty"]
    scene = gl.getCurrentScene()
    # Les plans roses sont ajoutés
    rose = "rose"

    for l in range(47):
        empty.worldPosition = ( 17.1 + 0.11*l, 0, -1.2)
        obj_added = scene.addObject(rose, empty, 0)
        obj_added.worldScale = (0.1, 0, 0.01)
        gl.histo_mini[l] = obj_added

        empty.worldPosition = ( 17.1 + 0.11*l, 0, -0.3)
        obj_added = scene.addObject(rose, empty, 0)
        obj_added.worldScale = (0.1, 0, 0.01)
        gl.histo_maxi[l] = obj_added

        empty.worldPosition = ( 17.1 + 0.11*l, 0, 1)
        obj_added = scene.addObject(rose, empty, 0)
        obj_added.worldScale = (0.1, 0, 0.01)
        gl.histo_temps[l] = obj_added

def histo_update(game_obj):
    '''    {
    '2017_06_12_00': [0, 1, 0],
    '2017_06_12_14': [0, 0, 0],
    '2017_06_11_18': [-1, 5, -8],
    '2017_06_12_11': [1, 1, 0]}
    '''

    reset_histo(game_obj)

    # Tri du dict des datas du jour
    new_dict = gl.meteo_tools.sort_dict(gl.gaps)

    mini_list = []
    for k, v in new_dict.items():
        mini_list.append(v[0])

    ##if gl.current_day == "2017_07_03":
        ##print(new_dict)
        ##print(mini_list)

    maxi_list = []
    for k, v in new_dict.items():
        maxi_list.append(v[1])
    temps_list = []
    for k, v in new_dict.items():
        temps_list.append(v[2])

    #c = min(len(mini_list), 47)
    c = len(mini_list)
    for l in range(c):
        m = mini_list[l]
        if -0.1 < m < 0.1: m = 0.5
        gl.histo_mini[l].localScale[2] = m/20

        M = maxi_list[l]
        if -0.1 < M < 0.1: M = 0.5
        gl.histo_maxi[l].localScale[2] = M/20

        t = temps_list[l]
        if -0.1 < t < 0.1: t = 0.5
        gl.histo_temps[l].localScale[2] = t/20

def reset_histo(game_obj):
    for l in range(47):
        gl.histo_mini[l].localScale[2] = 0  #0.0001
        gl.histo_maxi[l].localScale[2] = 0  #0.0001
        gl.histo_temps[l].localScale[2] = 0  #0.0001

def set_spread(game_obj):
    spread = [[0,0], [0,0], [0,0]]

    mini = []
    maxi = []
    temps = []
    for k, v in gl.gaps.items():
        mini.append(v[0])
        maxi.append(v[1])
        temps.append(v[2])

    mini.sort()
    spread[0][0] = mini[0]
    spread[0][1] = mini[-1]

    maxi.sort()
    spread[1][0] = maxi[0]
    spread[1][1] = maxi[-1]

    temps.sort()
    spread[2][0] = temps[0]
    spread[2][1] = temps[-1]

    game_obj["mini mini"]["Text"] = spread[0][0]
    game_obj["mini maxi"]["Text"] = spread[0][1]

    game_obj["maxi mini"]["Text"] = spread[1][0]
    game_obj["maxi maxi"]["Text"] = spread[1][1]

    game_obj["temps mini"]["Text"] = spread[2][0]
    game_obj["temps maxi"]["Text"] = spread[2][1]

