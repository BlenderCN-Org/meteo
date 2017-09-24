#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## meteo_gaps.py

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
2ème fichier à faire tourner
Calcul les écarts
Le fichier gaps.txt doit exister et contenir au moins: {}
'''

import os
from time import sleep
import json
from datetime import datetime
from collections import OrderedDict
from meteo_tools import MeteoTools
from weather_types import weather_types, weather


# Le json des analyses
FORECAST = "output/forecast.txt"

# Le json des écarts
# Recommence le calcul complet à toute relance
GAPS = "output/gaps.txt"


class MeteoGaps(MeteoTools):
    '''Trouve les gaps pour chaque jour/heure.'''

    def __init__(self):
        super().__init__()

        self.debug = 0

        # Récup des datas dans le fichier FORECAST
        self.forecasts = self.get_json_file(FORECAST)

    def get_all_days_in_forecasts(self):
        '''Uniquement les jours, sans doublon et sans heures.'''

        self.days = []
        for d, p in self.forecasts.items():
            for k, v in p.items():
                day = k
                if day not in self.days:
                    self.days.append(day)

        # Tri
        self.days.sort()

        if self.debug == 1:
            print("Nombre de jours avec prévisions =", len(self.days))
            print("Liste des jours avec prévisions:\n", self.days)

    def get_weather_types(self, wt_str):
        '''Retourne un entier correspondant au type de temps.'''

        try:
            wt = weather[weather_types[wt_str]]
        except:
            print("Vous devez ajouter {} à weather_types".format(wt_str))
            print("et faire correspondre avec weather")
            os._exit(0)
        return wt

    def write_gaps(self):
        '''Ecrit en écrasant le fichier GAPS.'''

        self.write_json_file(self.gaps, GAPS)

    def get_real_weathers(self):
        '''Retourne le temps réél du jour day

        pour le mini
        "2017_06_12_08":
        {"2017_06_19": ["lundi 19", 14, 25, "Ensoleill\u00e9"],
        "2017_06_24": ["samedi 24", 14, 28, "Ensoleill\u00e9"],
        "2017_06_25": ["dimanche 25", 15, 27, "Ensoleill\u00e9"],
        "2017_06_23": ["vendredi 23", 16, 28, "Ensoleill\u00e9"],
        "2017_06_18": ["dimanche 18", 13, 28, "Ensoleill\u00e9"],
        "2017_06_13": ["mardi 13", 13, 25, "Ensoleill\u00e9"],
        "2017_06_21": ["mercredi 21", 16, 31, "Ensoleill\u00e9"],
        "2017_06_17": ["samedi 17", 12, 24, "Ensoleill\u00e9"],
        ici !!!! "2017_06_12": ["lundi 12", 14, 30, "Ensoleill\u00e9"],
        "2017_06_20": ["mardi 20", 16, 31, "Ensoleill\u00e9"],
        "2017_06_14": ["mercredi 14", 10, 25, "Ciel voil\u00e9 "],
        "2017_06_15": ["jeudi 15", 14, 32, "\u00c9claircies"],
        "2017_06_16": ["vendredi 16", 17, 28, "\u00c9claircies"],
        "2017_06_22": ["jeudi 22", 16, 31, "Ensoleill\u00e9"]},

        je cherche d'abord la clé du jour à 8h: 2017_06_12_08
        puis le jour: 2017_06_12

        pour le maxi
        "2017_06_12_16":
        {"2017_06_19": ["lundi 19", 14, 28, "\u00c9claircies"],
        "2017_06_24": ["samedi 24", 16, 26, "\u00c9claircies"],
        "2017_06_25": ["dimanche 25", 14, 25, "\u00c9claircies"],
        "2017_06_23": ["vendredi 23", 16, 29, "\u00c9claircies"],
        "2017_06_18": ["dimanche 18", 13, 27, "\u00c9claircies"],
        "2017_06_13": ["mardi 13", 12, 24, "Ensoleill\u00e9"],
        "2017_06_21": ["mercredi 21", 16, 30, "\u00c9claircies"],
        "2017_06_17": ["samedi 17", 11, 24, "Ensoleill\u00e9"],
        "2017_06_12": ["lundi 12", 14, 29, "Ensoleill\u00e9"],
        "2017_06_20": ["mardi 20", 15, 31, "\u00c9claircies"],
        "2017_06_14": ["mercredi 14", 10, 26, "Ensoleill\u00e9"],
        "2017_06_15": ["jeudi 15", 14, 30, "\u00c9claircies"],
        ici !!!! "2017_06_16": ["vendredi 16", 17, 29, "\u00c9claircies"],
        "2017_06_22": ["jeudi 22", 15, 31, "\u00c9claircies"]},
        '''

        self.real_weathers = OrderedDict()

        for day in self.days:
            # le mini est à 8h ce jour là = day
            key_mini = day + "_08"
            if key_mini in self.forecasts:
                if day in self.forecasts[key_mini]:
                    t_min = self.forecasts[key_mini][day][1]
            else:
                t_min = None

            # le maxi est à 16h ce jour là = day
            key_maxi = day + "_16"
            if key_maxi in self.forecasts:
                if day in self.forecasts[key_maxi]:
                    t_max = self.forecasts[key_maxi][day][2]
            else:
                t_max = None

            # le temps est à 14h ce jour là = day
            key_temps = day + "_14"
            if key_temps in self.forecasts:
                if day in self.forecasts[key_temps]:
                    wt = self.get_weather_types(self.forecasts[key_temps][day][3])
            else:
                wt = None

            self.real_weathers[day] = [ t_min,
                                        t_max,
                                        wt    ]

            if t_min == None or t_max == None or wt == None:
                self.real_weathers[day] = None

            if self.debug:
                print("Temps réel du {}: {}".format(day, self.real_weathers[day]))
        if self.debug:
            print("Dict des temps rééls\n{}".format(self.real_weathers))

        print("Nombre de jours avec temps réel", len(self.real_weathers))

    def inversion_du_dict_forecast(self):
        '''
        forecast =
        { j_h = "2017_08_01_01":
            prev_dict = {"2017_08_11": ["vendredi 11", 12, 26, "\u00c9claircies"],
                        "2017_08_12": ["samedi 12", 13, 26, "\u00c9claircies"],
                        "2017_08_07": ["lundi 07", 13, 25, "\u00c9claircies"],
                        "2017_08_14": ["lundi 14", 14, 27, "\u00c9claircies"],
                        "2017_08_04": ["vendredi 04", 15, 25, "\u00c9claircies"],
                        "2017_08_09": ["mercredi 09", 12, 24, "\u00c9claircies"],
                        "2017_08_06": ["dimanche 06", 13, 24, "\u00c9claircies"],
                        "2017_08_01": ["mardi 01", 15, 26, "\u00c9claircies"],
                        "2017_08_13": ["dimanche 13", 14, 26, "\u00c9claircies"],
                        "2017_08_02": ["mercredi 02", 14, 28, "\u00c9claircies"],
                        "2017_08_03": ["jeudi 03", 17, 29, "\u00c9claircies"],
                        "2017_08_08": ["mardi 08", 13, 24, "\u00c9claircies"],
                        "2017_08_05": ["samedi 05", 14, 25, "\u00c9claircies"],
                        "2017_08_10": ["jeudi 10", 12, 24, "\u00c9claircies"]},
                        ...........}
        devient
        { "2017_08_02":
            "2017_08_01_01": ["mercredi 02", 14, 28, "\u00c9claircies"],
            "2017_08_02_10": ["mer 02", 14, 29, "\u00c9claircies"],
            ...........}

        '''

        self.forecasts_inv = OrderedDict()

        for day in self.days:
            self.forecasts_inv[day] = OrderedDict()

        for j_h, prev_dict in self.forecasts.items():
            for j, prev in prev_dict.items():

                self.forecasts_inv[j][j_h] = prev

        if self.debug == 1:
            print("\nDict ordonné des prévisions =")
            print(self.forecasts_inv)

    def set_gaps(self):
        '''
        { "2017_08_02":
            "2017_08_01_01": ["mercredi 02", 14, 28, "\u00c9claircies"],
            "2017_08_02_10": ["mer 02", 14, 29, "\u00c9claircies"],
            ...........}
        gaps
        {"2017_08_02": { "2017_08_01_01": [0, 0, 0],
                         "2017_06_02_10": [1, 1, 1],
                            etc .... } }
        '''

        # Le dict des écarts
        self.gaps = OrderedDict()

        # Parcours de forecasts
        for j, prev in self.forecasts_inv.items():

            # le temps réél du jour
            real_w = self.real_weathers[j]
            if self.debug == 1:
                print("{} --> valeurs réelles: {}".format(j, real_w))

            # la liste du jour/heure
            self.gaps[j] = OrderedDict()

            # Parcours de prev = dict des prév du jour
            for k, p in prev.items():
                # Conversion du type de temps en entier
                # p[3] = 'Averses orageuses'
                wt = self.get_weather_types(p[3])

                try:
                    ecart = [ (p[1] - real_w[0]),
                              (p[2] - real_w[1]),
                              (wt   - real_w[2])]
                    if self.debug == 2:
                        a = "Le {} pour le jour {} maxi: prévu {} écart {}"
                        print(a.format(j_h, k, p[2], ecart[1]))
                except:
                    # Pas de real_weathers, ecart impossible
                    ecart = None

                # L'écart du jour/heure
                if ecart:
                    self.gaps[j][k] = ecart
                else:
                    self.gaps[j] = None

        print("Nombre de jours avec écarts y compris les écarts None", len(self.gaps))
        if self.debug == 1:
            print("Dict des écarts\n", self.gaps)


def main():
    sleep(1)
    print("Pour une sortie bavarde, changer pour mg.debug = 1")
    print("Aggrandisser la fenêtre du terminal")
    print("2ème scripts à excécuter\n")

    mg = MeteoGaps()

    # Attribut modifiable
    mg.debug = 0

    # Liste de tous les jours dans forecasts, indépendemment de l'heure
    mg.get_all_days_in_forecasts()

    # Temps pseudo réél de chaque jour
    mg.get_real_weathers()

    # Clé en jours au lieu de jour_heure
    mg.inversion_du_dict_forecast()

    # Ecarts
    mg.set_gaps()
    mg.write_gaps()

    print("\nCalcul des écarts OK")
    print("Vous pouvez lancer le jeu")

if __name__ == "__main__":

    main()

