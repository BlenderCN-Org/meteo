#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## beautiful_meteo.py


#############################################################################
# Copyright (C) Labomedia June 2017
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


################  Valable jusqu'au 2017 08 01 à 23h59 ################

# Ce script python est comme le html, de très mauvaise qualité !!!!!!!

from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from meteo_tools import MeteoTools


class BeautifulMeteo(MeteoTools):
    """Fouille dans la page pour trouver les
    températures mini, maxi, type de temps du jour courant et
    des 13 jours suivant.

    Retourne un dict.
    Utilise BeautifulSoup.
    """

    def __init__(self, file_path_name):
        """Chemin absolu avec nom du fichier."""

        super().__init__()

        self.debug = 0
        self.file_path_name = file_path_name

        # Le fichier à analyser
        self.fichier = self.read_file(self.file_path_name)

        self.forecast = {}

        # La clé du dict en 2017_07_29_01
        self.today_key = self.get_today_key()

        # Aujourd'hui en 2017-07-29 01:00:00
        self.today = self.get_real_date_time(self.today_key + "_00")

        # Le dict pour le jour/heure
        self.forecast[self.today_key] = {}

        # Une variable pour enregistrer les prévisions simplement
        self.frcst_dict = self.forecast[self.today_key]
        if self.debug:
            print("Clé du dict ordonné:", self.today_key, "\n")

        # La liste des 13 jours suivant le jour courant
        self.thirteen_days = self.get_thirteen_days(self.today)

        self.thirteen_days.insert(0, self.today_key[:-3])
        self.fourteen_days = self.thirteen_days

        if self.debug:
            print("14 jours\n{}".format(self.fourteen_days))
            print("qui font bien {} jours\n".format(len(self.fourteen_days)))

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

        soup = BeautifulSoup(self.fichier, "lxml")

        group_days_summary = soup.find_all("div", class_="group-days-summary")
        bloc_day_summary_0 = group_days_summary[0].find_all("article", class_="bloc-day-summary")
        bloc_day_summary_1 = group_days_summary[1].find_all("article", class_="bloc-day-summary")

        # 7 jours
        for i in range(0, 7):
            # jour de la prévision
            my_day = self.fourteen_days[i]

            # vérif avec fichier
            jour = group_days_summary[0].find_all("a",href="#detail-day-0" + str(i+1))
            jour = jour[0].text

            # <span class="min-temp">6°C Minimale</span>
            tmin = bloc_day_summary_0[i].find("span", class_="min-temp")
            #'12°C Minimale',
            tmin = int(tmin.string[:-11])

            # <span class="max-temp">17°C Maximale</span>
            tmax = bloc_day_summary_0[i].find("span", class_="max-temp")
            # '29°C Maximale'
            tmax = int(tmax.text[:-11])

            day_summary_image = bloc_day_summary_0[i-1].find("li",
                                                    class_="day-summary-image")
            picTemps = day_summary_image.find("span")
            temps = picTemps.text

            self.frcst_dict[my_day] = [jour, tmin, tmax, temps]

            if self.debug:
                print("i {} my_day {} jour {} Prévisions {}".format(i,
                      my_day, jour, self.frcst_dict[my_day]))

        # 7 jours suivant
        bloc_day_summary = group_days_summary[1].find_all("article", class_="bloc-day-summary")

        for i in range(0, 7):
            # jour de la prévision
            my_day = self.fourteen_days[i + 7]

            # vérif avec fichier
            jour = bloc_day_summary[i].find_all("header")
            jour = jour[0].find_all("h4")
            jour = jour[0].text

            # <span class="min-temp">6°C Minimale</span>
            tmin = bloc_day_summary_1[i].find("span", class_="min-temp")
            tmin = int(tmin.text[:-11])

            # <span class="max-temp">17°C Maximale</span>
            tmax = bloc_day_summary_1[i].find("span", class_="max-temp")
            tmax = int(tmax.text[:-11])

            day_summary_image = bloc_day_summary_1[i].find("li",
                                                    class_="day-summary-image")
            picTemps = day_summary_image.find("span")
            picTemps.text

            self.frcst_dict[my_day] = [jour, tmin, tmax, temps]

            if self.debug:
                print("i {} my_day {} jour {} Prévisions {}".format(i,
                      my_day, jour, self.frcst_dict[my_day]))

def test():
    """Bonne réponse
    lun 12 12 24
    mar 13 10 25
    mer 14 14 32
    jeu 15 17 28
    ven 16 12 24
    sam 17 13 28
    dim 18 14 30
    lun 19 16 31
    mar 20 16 31
    mer 21 16 31
    jeu 22 16 28
    ven 23 14 28
    sam 24 15 27
    dim 25 14 25
    """

    # Chemin relatif
    file_path_name = "meteo_files/2017_06/meteo_2017_06_12_10_05_19.html"

    forecast = BeautifulMeteo(file_path_name)
    forecast.debug = 1
    forecast.get_forecast()
    days = []
    for k, v in forecast.forecast['2017_06_12_10'].items():
        days.append(k)
    days.sort()

if __name__ == "__main__":

    test()
