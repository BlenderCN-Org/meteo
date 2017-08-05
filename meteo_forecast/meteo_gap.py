#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## meteo_gaps_batch.py

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


from time import sleep
import json
from datetime import datetime
from collections import OrderedDict
from meteo_tools import MeteoTools

## Variable globale à définir
# Fichier avec data issues de meteo_file_parser.py
file_name = 'first_new_1.txt'


class MeteoGap:
    """Excécute le gap d'un fichier meteo."""

    def __init__(self):

        self.tools = MeteoTools()
        self.weather_types = self.tools.get_weather_types


    def get_days(self, data):
        """Retourne la liste    """

        days = []
        for date_heure, prev in data.items():
            if date_heure not in days:
                days.append(date_heure)
        print("Nombre de day enregistrés =", len(days))
        days = sort_days(days)
        return days

    def get_date_jour(self, num):
        """Retourne date 2017-06-11 16:00:00 avec num = 2017_06_11_16 """

        return datetime.strptime(num, '%Y_%m_%d')

    def get_str_from_datetime(self, day):
        """Retourne le str 2017_06_11_16
        avec 2017-06-11 16:05:30 de type datetime
        """

        #print(day, type(day))
        return '{:%Y_%m_%d_%H}'.format(day)

    def get_date(self, num):
        """Retourne date 2017-06-11 16:00:00 avec num = 2017_06_11_16 """

        return datetime.strptime(num, '%Y_%m_%d_%H')

    def sort_days(self, days):
        """Liste de 2017_06_23_05, '2017_06_27_17' """

        sorted_days = []
        # Je traduits
        for day in days:
            real_day = get_date(day)
            sorted_days.append(real_day)
        # je trie
        sorted_days = sorted(sorted_days)
        # je retraduits inverse
        days = []
        for day in sorted_days:
            str_day = get_str_from_datetime(day)
            days.append(str_day)

        #print(days)
        return days

    def get_some_test(self, data, days):
        # Création des dicts pour tous les jours
        forecasts = OrderedDict()

        # Récup du dict des types de temps
        weather_types = get_weather_types()

        for day in days:
            forecasts[day[:-3]] = OrderedDict()

        for day in days:
            for date_heure, prevs in data.items():
                for date, prev in prevs.items():
                    if day == date:
                        # prev = ['vendredi 30', 14, 29, 'Averses orageuses']
                        prev[3] = weather_types[prev[3]]
                        forecasts[day[:-3]][date_heure] = prev

        print("Longueur de forecast pour le 2017_06_22", len(forecasts["2017_06_22"]))
        #print("Prévisions pour le 2017_06_22\n", forecasts["2017_06_22"])

        return forecasts

    def get_real_weather(self, forecasts, days):
        '''Retourne le temps réél du jour day
        day = 2017_06_22
        forecasts =
        "2017_06_23_05": {"2017_06_29_05_05": ["jeudi 29", 14, 22, "Rares averses"],
                          etc ...},
        Le temps réél est celui de 8 heures du jour day in days
        '''

        real_weathers = OrderedDict()
        for day in days:
            for key, val in forecasts.items():
                for cle, valeur in val.items():
                    #print(k, day)  # k=2017_07_02    day=2017_07_09_13
                    if key == day[:-3]:
                        # la valeur à 8 heures ! 2017_07_09_09
                        if day[11:] == "08":
                            # '2017_06_20_22': ['vendredi 23', 20, 36, 2]
                            #print(val)
                            real_weathers[day[:-3]] = valeur

        #{'2017_06_24_08': ['samedi 24', 17, 28, 0],
        # '2017_06_13_08': ['mardi 13', 13, 25, 0],
        # '2017_06_25_08': ['dimanche 25', 15, 26, 0],
        print("Temps rééls sur", len(real_weathers), "jours")
        return real_weathers

    def get_gaps(self, jours, forecasts, real_weathers):
        gaps = OrderedDict()

        # Parcours de forecasts
        for jour, all_prev in forecasts.items():
            # certain jour n'ont pas les datas
            try:
                # le temps réél du jour
                real_w = real_weathers[jour]
                # la liste du jour pour tout y mettre
                gaps[jour] = []

                # Parcours de v = dict des prév du jour
                for j_h, prev in all_prev.items():

                    # L'écart du jour/heure
                    gaps[jour].append([j_h,
                                       prev[1] - real_w[1],
                                       prev[2] - real_w[2],
                                       prev[3] - real_w[3]])
            except:
                print("Il manque des datas pour le", jour)

        return gaps

    def get_sorted_gaps(self, gaps):
        '''TODO: tri sur quoi ?'''

        sorted_gaps = gaps   #OrderedDict()

        for jour, gaps_list in sorted_gaps.items():
            pass


        #print(sorted_gaps)
        return sorted_gaps

    def sort_gaps(self, days):
        """Liste de 2017_06_23_05, '2017_06_27_17' """

        sorted_days = []
        # Je traduits
        for day in days:
            real_day = get_date(day)
            sorted_days.append(real_day)
        # je trie
        sorted_days = sorted(sorted_days)
        # je retraduits inverse
        days = []
        for day in sorted_days:
            str_day = get_str_from_datetime(day)
            days.append(str_day)

        #print(days)
        return days

    def print_sorted_gaps(self, sorted_gaps):
        """
        {'2017_06_28': [['2017_06_24_01', 3, 4, 29],
                    ['2017_06_16_10', -1, -1, 24],
                    ['2017_06_26_00', 2, 0, 25],
                    ['2017_06_27_08', 5, 0, 25],
        """

        for jour, gap_list in sorted_gaps.items():
            print("Variation des prévisions pour le", jour)
            for gap in gap_list:
                total = abs(gap[1]) + abs(gap[2]) + abs(gap[3])
                print("    {:^12}: mini {:^6} maxi {:^6} type de temps {:^6} total{:^6}".
                        format(gap[0], gap[1], gap[2], gap[3], total))
                sleep(0.001)


def main(file_name):
    # Récup des datas dans le fichier first.txt
    data = get_data(file_name)

    # Récup des jours/heurs avec prévisions
    days = get_days(data)
    print("Nombre de jours/heures", len(days))

    # Récup des jours seuls
    jours = get_jours(data)
    print("Nombre de jours", len(jours))

    # Toutes les prévisions
    forecasts = get_some_test(data, days)

    # Récup des temps rééls
    real_weathers = get_real_weather(forecasts, days)

    # Comparaison
    gaps = get_gaps(jours, forecasts, real_weathers)
    #print(gaps)

    # Tri des comparaisons
    sorted_gaps = get_sorted_gaps(gaps)

    # Impression rytmée
    print_sorted_gaps(sorted_gaps)


if __name__ == "__main__":

    main(file_name)
