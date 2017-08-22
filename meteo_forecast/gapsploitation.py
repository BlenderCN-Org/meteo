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

# Le json de l'exploitation
GAPSPLOITATION = "output/gapsploitation_3.txt"


class GapSploitation(MeteoTools):
    '''Jeu avec les écarts.'''

    def __init__(self):
        super().__init__()

        # Récup des datas dans le fichier GAPS
        self.gaps = self.get_json_file(GAPS)
        self.sort_gaps()

    def sort_gaps(self):
        '''Tri du dict puis du dict dans le dict.'''

        # 1 er tri
        self.gaps_sorted = self.sort_dict(self.gaps)

        # 2 ème tri
        for k, v in self.gaps_sorted.items():
            new_v = self.sort_dict(v)
            self.gaps_sorted[k] = new_v

    def print_some(self):
        for cle, value in self.gaps_sorted.items():
            print("\nJour, heure", cle)
            for k1, v1 in value.items():
                print(k1, v1)

    def get_days(self):
        self.days = []
        for k, v in self.gaps.items():
            for k1, v1 in v.items():
                if k1 not in self.days:
                    self.days.append(k1)
        self.days.sort()
        print("Nombre de jours en stock:", len(self.days))

    def get_gaps_by_day(self):
        self.gaps_by_day = {}

        for day in self.days:
            self.temp_dict = {}
            for k, v in self.gaps_sorted.items():
                for k1, v1 in v.items():
                    if k1 == day:
                        self.temp_dict[k] = v1

            self.gaps_by_day[day] = self.sort_dict(self.temp_dict)

        self.new_gaps = self.sort_dict(self.gaps_by_day)

    def changes(self):
        '''Je supprime les répétitions.'''

        old_dict = self.new_gaps.copy()

        new_dict = OrderedDict()
        last = []
        for k, v in old_dict.items():
            new_dict[k] = OrderedDict()
            for i, j in v.items():
                if j != last:
                    print(last)
                    last = j
                    new_dict[k][i] = j

        self.new_gaps = new_dict

    def print_gaps(self):
        for k, v in self.new_gaps.items():
            print("Prévisions", k)
            for k1, v1 in v.items():
                print(k1, v1)

    def save_gapsploitation(self):
         self.write_json_file(self.new_gaps, GAPSPLOITATION)


def main():
    gs = GapSploitation()
    #gs.print_some()
    gs.get_days()
    gs.get_gaps_by_day()
    gs.changes()
    gs.save_gapsploitation()
    #gs.print_gaps()


if __name__ == "__main__":
    main()
