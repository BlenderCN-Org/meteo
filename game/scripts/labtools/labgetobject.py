#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

## labgetobject.py

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


from bge import logic as gl

def get_all_scenes():

    # Liste des objets scènes
    activeScenes = gl.getSceneList()

    # Liste des noms de scènes
    scene_name = []
    for scn in activeScenes:
        scene_name.append(scn.name)

    return activeScenes, scene_name

def get_scene_with_name(scn):

    activeScenes, scene_name = get_all_scenes()
    if scn in scene_name:
        return activeScenes[scene_name.index(scn)]
    else:
        print(scn, "pas dans la liste")
        return None
