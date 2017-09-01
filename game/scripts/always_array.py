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

"""

################# Version avec numpy array #################


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
"""

import numpy as np
from time import time
from random import randint
from bge import logic as gl
from scripts.labtools import labgetobject as get_obj


def main():
    get_obj.get_all_scenes()

    game = get_obj.get_scene_with_name("Game")
    if game:
        game_obj = game.objects
        #print(game_obj)

    if not gl.display_init:
        initial_addition(game, game_obj)
    else:
        pass
        ##grabe()
        grabe_array()
        ##suppr_some()
        ##add_some()
        ##color_change(game, game_obj)
        display_fps()

def display_fps():
    print(gl.getLogicTicRate())

def initial_addition(scene, game_obj):
    """Affichage initial des plans."""

    empty = game_obj["Empty"]
    scene = gl.getCurrentScene()
    t0 = time()

    gl.display_init = 1

    for w in range(gl.L):
        for h in range(gl.H):
            # empty définit la position où sera ajouté l'objet
            empty.worldPosition = ( gl.origin[0] + w * gl.size + 2,
                                    0,
                                    gl.origin[1] + h * gl.size)

            # Les plans sont ajoutés
            # Les plans sont dans gl.gris_table, 0 = blanc, 10 = noir
            # random entre 0 et 10
            pixel = "gris" + str(randint(0, 10))

            # Ajout dans la scène
            obj_added = scene.addObject(pixel, empty, 0)
            obj_added.worldScale = (gl.size, 0, gl.size)

            # Ajout dans le tableau
            #gl.pixel_table.append(obj_added)

            # Set du array
            gl.pixel_array[w, h] = obj_added

    gl.display_init = 1
    t1 = time()
    t = t1 - t0
    print("Nombre d'images", gl.L*gl.H)
    print("Temps d'ajout", t)

def grabe_array():
    for w in range(gl.L):
        for h in range(gl.H):
            try:
                gl.pixel_array[w, h].worldPosition[0] += 0.0005
            except:
                print("Array ajout raté")

def grabe():
    for pix in gl.pixel_table:
        try:
            pix.worldPosition[0] += 0.0005
        except:
            print("grabe raté")

def suppr_some():
    """Suppression d'un pixel."""

    try:
        # suppr de l'objet blender
        gl.pixel_table[0].endObject()

        # suppr de l'item dans la liste
        gl.pixel_table.pop(0)
    except:
        print("Suppression raté")

def add_some():
    pass

def color_change(game, game_obj):
    """Changement de couleur au hazard, pour une couleur au hazard."""

    try:
        lequel = randint(0, len(gl.pixel_table))
        position = gl.pixel_table[lequel].worldPosition
        suppr_num(lequel)
        add_num(position, game_obj, game)
    except:
        print("Changement de couleur raté")

def add_num(position, game_obj, game):
    """Ajout d'un pixel dans la table et dans la scène."""

    # empty définit la position où sera ajouté l'objet
    empty = game_obj["Empty"]
    empty.worldPosition = position
    pixel = "gris" + str(randint(0, 10))

    # Ajout
    obj_added = game.addObject(pixel, empty, 0)
    gl.pixel_table.append(obj_added)

def suppr_num(num):
    try:
        # suppr de l'objet blender
        gl.pixel_table[num].endObject()

        # suppr de l'item dans la liste
        gl.pixel_table.pop(num)
    except:
        print("raté")
