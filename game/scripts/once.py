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

"""
Ce script est appelé par main_init.main dans blender
Il ne tourne qu'une seule fois pour initier las variables
qui seront toutes des attributs du bge.logic (gl)
Seuls les attributs de logic sont stockés en permanence.

Un thread est crée pour recevoir le multicast, puis après avoir reçu l'adresse
ip du serveur sur ce multicast, lancement d'un socket TCP pour envoyer.

"""


import numpy as np
from bge import logic as gl

from scripts.labtools.labconfig import MyConfig

def get_conf():
    """Récupère la configuration depuis le fichier *.ini."""

    # Le dossier courrant est le dossier dans lequel est le *.blend
    current_dir = gl.expandPath("//")
    print("Dossier courant depuis once.py {}".format(current_dir))
    gl.once = 0

    # TODO: trouver le *.ini en auto
    gl.ma_conf = MyConfig(current_dir + "scripts/bgb.ini")
    gl.conf = gl.ma_conf.conf

    print("\nConfiguration du jeu bgb:")
    print(gl.conf, "\n")

def set_gris_table():
    """Table des objets blender plan en gris."""
    gl.gris_table = ["gris0", "gris1", "gris2", "gris3", "gris4", "gris5",
                     "gris6","gris7", "gris8", "gris9", "gris10"]

def variable_init():

    gl.display_init = 0

    # Tableau dimension 2
    #gl.pixel_array = np.array(np.zeros((gl.L, gl.H), dtype=object))
    gl.pixel_array = np.empty((gl.L, gl.H), dtype=object)
    print(np.shape(gl.pixel_array))

    gl.suppr = 0

def var_from_ini():
    """Les pixels sont carrées.
    TODO mettre dans ini
    """

    gl.wide = 6 # largeur de l'écran
    gl.L = 125  #125  # nombre de pixels en largeur
    gl.H = 70  #70  # nombre de pixels en hauteur
    gl.nb = gl.L * gl.H
    gl.largeur_pixel = gl.wide / gl.L
    gl.size = gl.largeur_pixel
    gl.origin = (gl.size/2, gl.size/2)

    print(  "gl.size", gl.size,
            "gl.nb", gl.nb,
            "gl.origin", gl.origin,
            "gl.largeur_pixel", gl.largeur_pixel)

def main():
    """Lancé une seule fois à la 1ère frame au début du jeu par main_once."""

    print("Initialisation des scripts lancée un seule fois au début du jeu.")

    # Récupération de la configuration
    get_conf()

    var_from_ini()

    variable_init()

    set_gris_table()

    # Pour les mondoshawan
    print("ok once.py")
