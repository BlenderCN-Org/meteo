#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## beautiful_meteo.py

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


"""
################  Valable jusqu'au 2017 08 01 à 23h59 ################

Ensuite voir beautiful_meteo_new.py

Lit le fichier meteo_2017_07_29_01_05_09.html

L'attribut forecast de BeautifulMeteo retourne:

{'2017_07_29_01': { '2017_08_10': ['jeudi 10', 13, 26, 'Éclaircies'],
                    '2017_08_06': ['dimanche 06', 14, 26, 'Éclaircies'],
                    '2017_08_11': ['vendredi 11', 13, 26, 'Éclaircies'],
                    '2017_08_08': ['mardi 08', 14, 26, 'Éclaircies'],
                    ..... }}

"""


#from collections import OrderedDict
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from meteo_tools import MeteoTools
from get_config import GetConfig


class BeautifulMeteo(GetConfig):
    '''Fouille dans la page pour trouver les
    températures mini, maxi, type de temps
    des 13 jours suivant le jour/heure courant.

    Retourne un dict de meteo_2017_07_29_01_05_09.html
    Utilise BeautifulSoup.
    '''

    def __init__(self, file_path_name):
        '''Chemin absolu avec nom du fichier.'''

        super().__init__()

        self.debug = self.conf["test"]["debug"]
        self.file_path_name = file_path_name
        self.tools = MeteoTools()

        # Le fichier à analyser
        self.fichier = self.tools.read_file(self.file_path_name)

        self.forecast = {}  #OrderedDict()

        # La clé du dict en 2017_07_29_01
        self.today_key = self.get_today_key()

        # Aujourd'hui en 2017-07-29 01:00:00
        self.today = self.tools.get_real_date_time(self.today_key)

        # Le dict pour le jour/heure
        self.forecast[self.today_key] = {}  #OrderedDict()

        # Une variable pour enregistrer les prévisions simplement
        self.frcst_dict = self.forecast[self.today_key]
        if self.debug:
            print("Clé du dict ordonné:", self.today_key, "\n")

        # La liste des 13 jours suivant le jour courant
        self.thirteen_days = self.tools.get_thirteen_days(self.today)
        if self.debug:
            print("Liste des 13 jours suivant le {}: \n{} \n".
                    format(self.today_key[:-3], self.thirteen_days))

    def get_today_key(self):
        """Retourne la clé du dict qui contiendra toutes les prévisions
        issues du fichier, construit avec le chemin/nom du fichier:

        file/2017_06/meteo_2017_06_11_16_05_30.html

        donne

        clé = 2017_06_11_16
        """

        # str to list
        file_list = list(self.file_path_name)

        # Recherche du dernier / dans file_name
        slash_list = [i for i,x in enumerate(file_list) if x == "/"]  # 4 12

        # Coupe de tout avant le dernier / et la fin: _05_09.html
        return self.file_path_name[slash_list[-1]+7:-11]

    def get_forecast(self):
        """Dans la page html, trouve les températures mini maxi type de temps
            pour les 13 jours suivant.
        """

        soup = BeautifulSoup(self.fichier)

        group_days_summary = soup.find_all("div", class_="group-days-summary")
        bloc_day_summary_0 = group_days_summary[0].find_all("article",
                                                    class_="bloc-day-summary")
        bloc_day_summary_1 = group_days_summary[1].find_all("article",
                                                    class_="bloc-day-summary")


        # 6 jours
        for i in range(0, 6):
            # Le jour traité
            my_day = self.thirteen_days[i]

            jour = group_days_summary[0].find_all("a",
                                                href="#detail-day-0" + str(i+2))
            jour = jour[0].text

            # <span class="min-temp">6°C Minimale</span>
            tmin = bloc_day_summary_0[i-1].find("span", class_="min-temp")
            #'12°C Minimale',
            tmin = int(tmin.string[:-11])

            # <span class="max-temp">17°C Maximale</span>
            tmax = bloc_day_summary_0[i-1].find("span", class_="max-temp")
            # '29°C Maximale'
            tmax = int(tmax.text[:-11])

            day_summary_image = bloc_day_summary_0[i-1].find("li",
                                                    class_="day-summary-image")
            picTemps = day_summary_image.find("span")
            temps = picTemps.text

            self.frcst_dict[my_day] = [jour, tmin, tmax, temps]

        # 7 jours suivant
        bloc_day_summary = group_days_summary[1].find_all("article",
                                                    class_="bloc-day-summary")

        for i in range(0, 6):
            my_day = self.thirteen_days[i + 7]
            jour = bloc_day_summary[i+1].find_all("header")
            jour = jour[0].find_all("h4")
            jour = jour[0].text

            # <span class="min-temp">6°C Minimale</span>
            tmin = bloc_day_summary_1[i-1].find("span", class_="min-temp")
            tmin = int(tmin.text[:-11])

            # <span class="max-temp">17°C Maximale</span>
            tmax = bloc_day_summary_1[i-1].find("span", class_="max-temp")
            tmax = int(tmax.text[:-11])

            day_summary_image = bloc_day_summary_1[i-1].find("li",
                                                    class_="day-summary-image")
            picTemps = day_summary_image.find("span")
            picTemps.text

            self.frcst_dict[my_day] = [jour, tmin, tmax, temps]


def test():
    file_path_name = "meteo_files/2017_07/meteo_2017_07_29_01_05_09.html"

    forecast = BeautifulMeteo(file_path_name)
    forecast.get_forecast()

    print(forecast.forecast)

    tools = MeteoTools()
    tools.print_all_key_value(forecast.forecast['2017_07_29_01'])


if __name__ == "__main__":

    test()
