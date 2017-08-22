#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## meteo_gaps.py

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
from weather_types import weather_types


# Le json des analyses
FORECAST = "output/forecast.txt"

# Le json des écarts
# Recommence le calcul complet à toute relance
GAPS = "output/gaps.txt"


class MeteoGaps(MeteoTools):
    """Trouve les gaps pour chaque jour/heure."""

    def __init__(self):
        super().__init__()

        # Récup des datas dans le fichier FORECAST
        self.forecasts = self.get_json_file(FORECAST)

        # Liste de tous les jours dans forecasts, indépendemment de l'heure
        self.get_all_days_in_forecasts()

        # Temps pseudo réél de chaque jour
        self.get_real_weathers()

    def get_all_days_in_forecasts(self):
        """Uniquement les jours, sans doublon et sans heures."""

        self.days = []
        for d, p in self.forecasts.items():
            day = d[:-3]
            if not day in self.days:
                self.days.append(day)
        print("Nombre de jours en stock =", len(self.days))

    def get_real_weathers(self):
        '''Retourne le temps réél du jour day
        day = 2017_06_22
        forecasts =
        "2017_06_23_05": {"2017_06_29_05_05": ["jeudi 29", 14, 22, "Rares averses"],
                          etc ...},
        Le temps réél est celui de 8 heures.
        real_weathers = {   2017_06_22: ["jeudi 06", 14, 22, "Soleil"],
                            ...}
        '''

        self.real_weathers = {}
        for day in self.days:  # 2017_06_22
            for j_h, prev in self.forecasts.items():  # jour_heur, prev
                if j_h[:-3] == day:
                    # la valeur à 8 heures ! 2017_07_08_05
                    if j_h[11:] == "08":
                        jour = prev[day][0]
                        t_min = prev[day][1]

                    elif j_h[11:] == "16":
                        t_max = prev[day][2]

                    elif j_h[11:] == "14":
                        wt = self.get_weather_types(prev[day][3])

            self.real_weathers[day] = [ jour,
                                        t_min,
                                        t_max,
                                        wt    ]

            if day not in self.real_weathers:
                self.real_weathers[day] = None

        print("Nombre de jours avec temps réel", len(self.real_weathers))

    def get_day_gap(self, j1, j2):
        '''Retourne le nombre de jours entre 2 date.'''

        a = self.get_real_date_time(j1)
        b = self.get_real_date_time(j2)

        return (b - a).days

    def get_weather_types(self, wt_str):
        '''Retourne un entier correspondant au type de temps.'''

        try:
            wt = weather_types[wt_str]
        except:
            print("Vous devez ajouter {} à weather_types".format(p[3]))
            print("avec un coefficient logique")
            os._exit(0)
        return wt

    def write_gaps(self):
        '''Ecrit en écrasant le fichier GAPS.'''

        self.write_json_file(self.gaps, GAPS)

    def get_gaps(self):
        """gaps du jour/heure
        {"2017_06_11_20": { "2017_06_11": [0,   0, 0],
                            "2017_06_12": [13, 31, 1],
                            etc ....
                            }
        }
        """

        self.gaps = {}

        # Parcours de forecasts
        for j_h, prev in self.forecasts.items():
            # le temps réél du jour
            real_w = self.real_weathers[j_h[:-3]]

            if real_w:
                # la liste du jour/heure
                self.gaps[j_h] = {}
                a = 0
                # Parcours de prev = dict des prév du jour
                for k, p in prev.items():
                    # Conversion du type de temps en entier
                    wt = self.get_weather_types(p[3])

                    # Plus le jour est proche, plus les écarts sont pénalisés
                    e = 1 #14 - self.get_day_gap(j_h + "_59", k + "_23_59")

                    ecart = [ (p[1] - real_w[1]) * e,
                              (p[2] - real_w[2]) * e,
                              (wt   - real_w[3]) * e ]

                    # L'écart du jour/heure
                    self.gaps[j_h][k] = ecart

        print("Nombre de jours avec écarts", len(self.gaps))


def main():
    mg = MeteoGaps()
    mg.get_gaps()
    mg.write_gaps()



if __name__ == "__main__":

    main()
