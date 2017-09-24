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


from time import sleep
from bge import logic as gl
from bge import events
from scripts.labtools import labgetobject as get_obj
from datetime import timedelta

def main():
    # Maj entrée clavier
    keys()

    if not gl.pause:
        gl.tempoDict.update()

    game = get_obj.get_scene_with_name("Game")
    if game:
        game_obj = game.objects

    # Init ["always"] = 0 pour once.py
    if gl.tempoDict["always"].tempo == 1:
        print("Initialisation\n")

        # Reset pour la suite
        gl.tempoDict["day"].unlock()
        gl.tempoDict["day"].tempo = -1  # jolie bidouille

        # Traits verticaux du histo avec date
        traits_display(game_obj)

    # ensuite toujours à partir de 1
    else:
        if not gl.pause:
            if gl.tempoDict["day"].tempo == 0:
                set_resolution_visible(game_obj)

                # Maj de gl.day_number
                set_day_number()

                if not gl.restart:
                    # Maj
                    pretty_date_display(game_obj)
                    set_spread(game_obj)
                    update_number_between_trait(game_obj)
                    update_chronologic_histo(game_obj)

def update_chronologic_histo(game_obj):
    '''Affichge de la temp maxi positionné en horizontal par rapport
    à un point fixe à droite, le jour affiché=current_day à 23h.
    '''

    # pour ajout des objets
    empty = game_obj["Empty"]
    scene = gl.getCurrentScene()

    datas = gl.chronologic[gl.day_number]
    print("Nombre de barres soit nombre d'écart pour ce jour", len(datas))

    for val in datas:
        if val:
            X = 0.01666 * val[0] + 33.0
            X = int(100*X)/100
            # Ajout
            empty.worldPosition = (X, 0, 0)
            obj_added = scene.addObject("rose", empty, gl.day_frame - 30)

            # Scale
            try:
                sz = val[2][1]/10
                if -0.001 < sz < 0.001:
                    sz = 0.01
                obj_added.worldScale = (0.02, 0, sz)
            except:
                obj_added.worldScale = (0.02, 0, 0)

def update_number_between_trait(game_obj):
    # pour ajout des objets
    empty = game_obj["Empty"]
    scene = gl.getCurrentScene()

    # la date entre les traits
    for i in range(14):
        X = 0.425*i + 27.1
        empty.worldPosition = (X, 0, -1.4)

        try: # TODO à revoir
            obj_added = scene.addObject("jour", empty, gl.day_frame - 30)
            # Rotation sur x de 90°
            obj_added.applyRotation((90, 0, 0), 0)
            obj_added.resolution = 32

            # Text
            j = gl.jour.split()
            d = 0
            if len(j) > 1:
                d = int(j[1]) - 13 + i

            obj_added["Text"] = str(d)
            #print("Ajout texte ok")
        except:
            pass

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

def set_day_number():
    '''Toutes les gl.frame,
    récup et affichage des prévisions d'un nouveau jour,
    pour histogramm dynamic.
    '''

    # Bidouille pour partir à gl.day_number de once.py
    if gl.tempoDict["always"].tempo == 1:
        gl.day_number -= 1

    gl.day_number += 1

    if gl.day_number < len(gl.days):
        print("\nNuméro du jour en cours =", gl.day_number)
    else:
         gl.restartGame()
         gl.restart = 1

def pretty_date(date):
    '''Retourne une date à la française'''

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

def pretty_date_display(game_obj):
    if gl.day_number < len(gl.days):
        # Set du  jour en cours
        gl.current_day = gl.days[gl.day_number]

        # Affichage du jour en cours
        gl.jour = pretty_date(gl.current_day)
        game_obj["day"]["Text"] = gl.jour
        game_obj["day.001"]["Text"] = pretty_date(gl.current_day)

def set_spread(game_obj):
    spread = [[0,0], [0,0], [0,0]]

    mini = []
    maxi = []
    temps = []

    if gl.day_number < len(gl.days):
        for val in gl.chronologic[gl.day_number]:
            if val:
                # k = int, v = [None] ou [(-161, '2017_09_16_06', [-1, -2, -2]), ....
                mini.append(val[2][0])
                maxi.append(val[2][1])
                temps.append(val[2][2])

    try:
        mini.sort()
        spread[0][0] = mini[0]
        spread[0][1] = mini[-1]

        maxi.sort()
        spread[1][0] = maxi[0]
        spread[1][1] = maxi[-1]

        temps.sort()
        spread[2][0] = temps[0]
        spread[2][1] = temps[-1]
    except:
        print("Erreur spread")
        spread[0][0] = 0
        spread[0][1] = 0
        spread[1][0] = 0
        spread[1][1] = 0
        spread[2][0] = 0
        spread[2][1] = 0

        game_obj["maxi mini.001"]["Text"] = spread[1][0]
        game_obj["maxi maxi.001"]["Text"] = spread[1][1]


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
        gl.day_frame += gl.time
        gl.tempoDict["day"].periode = gl.day_frame
        gl.tempoDict["day"].tempo = -1

    if gl.keyboard.events[events.RIGHTARROWKEY] == gl.KX_INPUT_JUST_ACTIVATED:
        # RIGHT pour accélérer
        gl.day_frame -= gl.time
        if gl.day_frame < 0: gl.day_frame = 0
        gl.tempoDict["day"].periode = gl.day_frame
        gl.tempoDict["day"].tempo = -1

def print_fps():
    if gl.tempoDict["print"].tempo == 0:
        print(gl.getLogicTicRate())
