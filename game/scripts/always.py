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
"""


from time import time
from random import randint
from bge import logic as gl
from scripts.labtools import labgetobject as get_obj


def main():
    get_obj.get_all_scenes()

    game = get_obj.get_scene_with_name("Game")
    if game:
        game_obj = game.objects

    if not gl.display_init:
        initial_addition(game, game_obj)
        gl.display_init = 1
    else:
        scale_histo()
        print_fps()

def scale_histo():
    """Scale de la barre
    en focntion de ce qui est lu dans gapsploitation_2.txt
    """

    for l in range(14):

        sc = l/10
        gl.histo_added[l].worldScale = (0.2, 0, sc)

def print_fps():
    print(gl.getLogicTicRate())

def initial_addition(scene, game_obj):
    """Affichage initial des plans pour avoir 14 barres verticales roses.
    Le plan rose fait 1x1
    largeur de -3 à 3 = 6
    14 barres + 15 espaces = 29
    6/29 = 0.2
    hauteur de 0 à 3.4
    """

    empty = game_obj["Empty"]
    scene = gl.getCurrentScene()

    for l in range(14):
        # empty définit la position où sera ajouté l'objet
        empty.worldPosition = ( 2.18 + 0.2*(2*l + 1),
                                0,
                                1.7)

        # Les plans roses sont ajoutés
        rose = "rose"

        # Ajout dans la scène
        obj_added = scene.addObject(rose, empty, 0)
        obj_added.worldScale = (0.2, 0, 0.02)

        # Liste des objects ajoutés
        gl.histo_added[l] = obj_added

