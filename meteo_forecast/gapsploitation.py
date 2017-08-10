#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## gapsploitation.py

'''
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
'''

import os
from time import sleep
import json
from datetime import datetime
from collections import OrderedDict
from meteo_tools import MeteoTools


# Le json des écarts
GAPS = "output/gaps.txt"


class GapSploitation(MeteoTools):
    '''Jeu avec les écarts.'''

    def __init__(self):
        super().__init__()

        # Récup des datas dans le fichier GAPS
        self.gaps = self.get_json_file(GAPS)
        self.sort_gaps()

        self.print_some()

    def sort_gaps(self):
        '''Tri du dict puis du dict dans le dict.'''

        # 1 er tri
        self.gaps_sorted = self.sort_dict(self.gaps)

        # 2 ème tri
        for k, v in self.gaps_sorted.items():
            new_v = self.sort_dict(v)
            self.gaps_sorted[k] = new_v

    def sort_dict(self, old_dict):
        '''Tri d'un dict par clé en date.'''

        new_dict = OrderedDict()
        old_dict_keys = list(old_dict)
        old_dict_keys.sort()
        for k in old_dict_keys:
            new_dict[k] = old_dict[k]

        return new_dict

    def print_some(self):
        '''
        Jour, heure 2017_08_07_11
            2017_08_07 [0, 0, 0]
            2017_08_08 [15, 21, 25]
            2017_08_09 [24, 40, 52]
            2017_08_10 [33, 60, 39]
            2017_08_11 [44, 92, 12]
            2017_08_12 [60, 125, 15]
            2017_08_13 [84, 162, 144]
            2017_08_14 [98, 196, 7]
            2017_08_15 [120, 208, 200]
            2017_08_16 [135, 234, 225]
            2017_08_17 [140, 250, 30]
            2017_08_18 [154, 264, 11]
            2017_08_19 [168, 300, 12]
            2017_08_20 [182, 338, 13]
        '''

        for cle, value in self.gaps_sorted.items():
            print("\nJour, heure", cle)
            for k1, v1 in value.items():
                print(k1, v1)

def main():
    gs = GapSploitation()


if __name__ == "__main__":
    main()
