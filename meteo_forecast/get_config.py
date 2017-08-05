#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## get_config.py

#############################################################################
# Copyright (C) Labomedia Juin 2017
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

"""Retourne la config dans un dict,
utilisé dans tous les scripts.

Utilise le fichier meteo.ini spécifique
"""

from labconfig import MyConfig

ini_file = "meteo.ini"

class GetConfig(MyConfig):

    def __init__(self):
        super().__init__(ini_file)


if __name__ == '__main__':

    meteo_cfg = GetConfig()
    print(dir(meteo_cfg))
    print(meteo_cfg.conf)
