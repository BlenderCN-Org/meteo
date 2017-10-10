#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# beautiful_meteo_new.py


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


# ###############  Valable à partir du 2017_08_02 à 00h00 ################

# Les informaticiens de la météo se sont surpassés !!!!!!!!!!!!!!!!!!!!!!!!!!!
# Mon python est plus propre comme le fichier html


from bs4 import BeautifulSoup
from meteo_tools import MeteoTools


class BeautifulMeteoNew:
    """Fouille dans la page pour trouver les
    températures mini, maxi, type de temps
    des 13 jours suivant le jour/heure courant.

    Retourne un dict de meteo_2017_07_29_01_05_09.html
    Utilise BeautifulSoup.
    """

    def __init__(self, file_path_name):
        """Chemin absolu avec nom du fichier."""

        self.debug = 0
        self.file_path_name = file_path_name
        self.tools = MeteoTools()

        # Le fichier à analyser
        self.fichier = self.tools.read_file(self.file_path_name)

        self.forecast = {}

        # La clé du dict en 2017_07_29_01
        self.today_key = self.get_today_key()

        # Aujourd'hui en 2017-07-29 01:00:00
        self.today = self.tools.get_real_date_time(self.today_key + "_00")

        # Le dict pour le jour/heure
        self.forecast[self.today_key] = {}

        # Une variable pour enregistrer les prévisions simplement
        self.frcst_dict = self.forecast[self.today_key]
        if self.debug:
            print("Clé du dict ordonné:", self.today_key, "\n")

        # La liste des 13 jours suivant le jour courant
        self.thirteen_days = self.tools.get_thirteen_days(self.today)
        if self.debug:
            print("Liste des 13 jours suivant le {}: \n{} \n".
                  format(self.today_key[:-3], self.thirteen_days))

        # La liste des 14 jours
        self.days_list = [self.today_key[:-3]]
        for d in self.thirteen_days:
            self.days_list.append(d)

    def get_today_key(self):
        """Retourne la clé du dict qui contiendra toutes les prévisions
        issues du fichier, construit avec le chemin/nom du fichier:
        meteo_files/2017_06/meteo_2017_06_11_16_05_30.html
        donne
        clé = 2017_06_11_16
        """

        # str to list
        file_list = list(self.file_path_name)

        # Recherche du dernier / dans file_name
        slash_list = [i for i, x in enumerate(file_list) if x == "/"]  # 4 12

        # Coupe de tout avant le dernier / et la fin: _05_09.html
        return self.file_path_name[slash_list[-1] + 7:-11]

    def get_forecast(self):
        """Dans la page html, trouve les températures mini maxi type de temps
        pour les 14 jours en cours.
        """

        # Défini self.liste_jours
        self.get_liste_jours()

        # Défini days = ["mar 12", "mer 13", etc ...] 14 jours
        days = self.get_jours()

        # Défini t_min = [12, 13, etc ...]
        tm = self.get_t_min()

        # Défini t_max = [12, 13, etc ...]
        tM = self.get_t_max()

        # Défini type_temps = ["pluie", "soleil", etc ...]
        type_temps = self.get_type_temps()

        # Dans forecast
        self.set_forecast(days, tm, tM, type_temps)

    def set_forecast(self, days, tm, tM, type_temps):
        """Le tout dans le dict forecast."""

        for i in range(14):
            self.frcst_dict[self.days_list[i]] = [days[i],
                                                  tm[i],
                                                  tM[i],
                                                  type_temps[i]]

    def get_liste_jours(self):
        """Retourne la partie de la page html avec toutes les infos."""

        soup = BeautifulSoup(self.fichier)

        # <div class="liste-jours">
        self.liste_jours = soup.find_all("div", class_="liste-jours")

    def get_jours(self):
        """Récupération des jours."""

        try:
            jours = self.liste_jours[0].find_all("a")
        except:
            print("Pas de jours")
            jours = None

        # Récupération dans une liste de 14
        days = []
        if jours:
            for elt in jours:
                days.append(elt.get_text())
        else:
            days = [None] * 14

        return days

    def get_t_min(self):
        """Récupération des temps mini."""

        try:
            min_temp = self.liste_jours[0].find_all("span", class_="min-temp")
        except:
            print("Pas de min_temp")
            min_temp = None

        tm = []
        if min_temp:
            for elt in min_temp:
                try:
                    m = int(elt.get_text()[:-11])
                except:
                    print("Pas de temp mini")
                    m = None
                tm.append(m)
        else:
            tm = [None] * 14
        return tm

    def get_t_max(self):
        """Récupération des temps maxi."""

        try:
            max_temp = self.liste_jours[0].find_all("span", class_="max-temp")
        except:
            print("Pas de max_temp")
            max_temp = None

        tM = []
        if max_temp:
            for elt in max_temp:
                try:
                    m = int(elt.get_text()[:-11])
                except:
                    print("Pas de temp maxi")
                    m = None
                tM.append(m)
        else:
            tM = [None] * 14
        return tM

    def get_type_temps(self):
        """<dd class="pic40 J_W1_0-N_1">Éclaircies</dd>
        TODO : Je ne comprends pas
        toto = Éclaircies
                    14°C Minimale 29°C Maximale
        """

        try:
            type_temps = self.liste_jours[0].find_all("dd")
        except:
            print("Pas de type_temps")
            type_temps = None

        tt = []
        if type_temps:
            for elt in type_temps:
                toto = elt.get_text()
                if not "°C" in toto:
                    try:
                        t = toto.splitlines()[0]
                    except:
                        print("Pas de type de temps")
                        t = None
                    tt.append(t)  # la 1ère ligne
        else:
            tt = [None] * 14
        return tt


def test():
    # Chemin relatif
    files = ["meteo_files/2017_08/meteo_2017_08_02_00_05_25.html"]

    for f in files:
        forecast = BeautifulMeteoNew(f)
        forecast.get_forecast()

        print("Prévisions\n", forecast.forecast, "\n")


if __name__ == "__main__":
    test()
