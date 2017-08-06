#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## meteo_tools.py

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


import os
from pathlib import Path
from json import dumps
from datetime import datetime, timedelta
#from collections import OrderedDict

"""Des méthodes souvent appelées par les autres scripts."""


class MeteoTools:

    def get_all_files(self, master_dir):
        """Retourne un dict avec
        clé = répertoires
        valeur = liste de tous les fichiers avec chemin relatif
        dict = {    "2017_06": [/abs/meteo_x0.html, /abs/meteo_x1.html .....],
                    "2017_07": [/abs/meteo_y0.html, /abs/meteo_y1.html .....],}

        master_dir = répertoire dans le dossier de ce script.
        """

        all_files = {}

        for directory in os.listdir(master_dir):
            all_files[directory] = []
            for fichier in os.listdir(master_dir + "/" + directory):
                if fichier.endswith(".html"):
                    file_name = os.path.join(fichier)
                    abs_file = master_dir + "/" + directory + "/" + file_name
                    all_files[directory].append(abs_file)

        return all_files

    def files_dict_to_list(self, files_dict):
        """Retourne une liste avec tous les fichiers
        d'un dict retourné par get_all_files()
        """

        tous_list = []
        for month_all_files in files_dict.values():
            for f in month_all_files:
                tous_list.append(f)
        return tous_list

    def read_file(self, file_name):
        '''Retourne les datas lues dans le fichier avec son chemin/nom.'''

        # Open our local file
        with open(file_name) as f:
            read_data = f.read()

        f.close()
        return read_data

    def write_data_in_file(self, data, fichier):
        """Ecrit les data dans le fichier, écrase l'existant."""

        with open(fichier, 'w') as fd:
            fd.write(data)

    def data_to_json(self, data):
        """Retourne le json des datas"""

        return dumps(data)

    def get_real_date_time(self, key):
        """Retourne 2017-06-11 16:00:00 avec 2017_06_11_16 """

        return datetime.strptime(key, '%Y_%m_%d_%H')

    def get_date_hour_key_from_datetime(self, day_time):
        """Retourne le str 2017_06_11_16 avec 2017-06-11 16:05:30 de type datetime."""

        return '{:%Y_%m_%d_%H}'.format(day_time)

    def get_date_key_from_datetime(self, day_time):
        """Retourne le str 2017_06_11 avec 2017-06-11 16:05:30 de type datetime."""

        return '{:%Y_%m_%d}'.format(day_time)

    def get_date_hour_mn_key_from_datetime(self, day_time):
        """Retourne le str 2017_06_11_16_05
        avec 2017-06-11 16:05:30 de type datetime.
        """

        return '{:%Y_%m_%d_%H_%M}'.format(day_time)

    def get_thirteen_days(self, today):
        """Retourne une liste des 13 jours en symbole suivant le
        today = 2017-07-29 01:00:00
        """

        thirteen_days = []

        for i in range(13):
            end_date = today + timedelta(days=i+1)
            x_date = end_date.strftime('%Y_%m_%d')
            thirteen_days.append(x_date)

        #['2017_07_29', '2017_07_30', '2017_07_31' ..
        return thirteen_days

    def get_weather_types(self):
        """Dict des types de temps avec leur poids.
        Si le script """

        weather_types = {   "Nuit claire": 0,
                            "Ensoleillé": 1,
                            "Ciel voilé ": 2,
                            "Éclaircies": 3,
                            "Très nuageux": 4,
                            "Brume ou bancs de brouillard": 5,
                            "Brouillard": 6,
                            "Brouillard givrant": 7,
                            "Pluie faible": 8,
                            "Pluie verglaçante": 9,
                            "Pluies éparses / Rares averses": 10,
                            "Pluie / Averses": 11,
                            "Pluie forte": 12,
                            "Averses orageuses": 13,
                            "Pluies orageuses": 14,
                            "Quelques flocons": 15,
                            "Pluie et neige": 16,
                            "Neige / Averses de neige": 17,
                            "Neige forte": 18,
                            "Risque de grêle": 19,
                            "Risque d’orages": 20,
                            "Orages": 21
                        }
        return weather_types

    def print_all_key_value(self, my_dict):
        '''Imprime un dict contenant un dict, affiche le nombre de clés total.
        '''

        total = 0

        for k, v in my_dict.items():
            print(k)
            for f in v:
                total += 1
                print("    ", f)
        print("Nombre de clés total =", total)
        print("pour un théorique par jour de =", 24*1)

    def get_year(self, key):
        """Retourne l'année soit 2017 dans 2017_06_22_15_05_48."""

        return key[0:-12]

    def get_month(self, key):
        """Retourne mois soit 06 dans 2017_06_22_15_05_48."""

        return key[5:-9]

    def get_day(self, key):
        """Retourne jour soit 22 dans 2017_06_22_15_05_48."""

        return key[8:-6]

    def get_hour(self, key):
        """Retourne heure soit 15 dans 2017_06_22_15_05_48."""

        return key[11:-3]

    def get_year_month(self, key):
        """Retourne année mois jour soit 2017_06_22 dans 2017_06_22_15_05_48"""

        return key[0:-9]

    def get_year_month_day(self, key):
        """Retourne année mois jour soit 2017_06_22 dans 2017_06_22_15_05_48"""

        return key[0:-6]

    def sort_jours(self, jours):
        """Retourne la liste triée de la liste de 2017_06_23_05, 2017_06_27_17.
        """

        sorted_jours = []

        # Je traduits
        for jour in jours:
            real_jour = get_date_jour(jour)
            sorted_jours.append(real_jour)

        # je trie
        sorted_jours = sorted(sorted_jours)

        # je retraduits inverse
        jours = []
        for jour in sorted_jours:
            str_jour = get_str_from_datetime(jour)
            jours.append(str_jour[:-3])

        return jours

    def get_jours(self, data):

        jours = []

        for date_heure, prev in data.items():
            if date_heure[:-3] not in jours:
                jours.append(date_heure[:-3])
        jours = self.sort_jours(jours)

        return jours

    def create_directory(self, directory):
        '''Crée le répertoire avec le chemin absolu.
        ex: /media/data/3D/projets/meteo/meteo_forecast/2017_06
        '''

        try:
            Path(directory).mkdir(mode=0o777, parents=False)
            print("Le répertoire {} a été créé.".format(directory))
        except FileExistsError as e:
            print(e)

    def get_absolute_path(self, a_file_or_a_directory):
        """Retourne le chemin absolu d'un répertoire ou d'un fichier
        n'importe où.
        """

        return os.path.abspath(a_file_or_a_directory)

    def create_dir_year_month_in_meteo_files(self, year_month):
        """Crée le répertoires année_mois.
        year_month = 2017_09
        pas de /
        """

        # Chemin absolu
        meteo_files_path = self.get_absolute_path("meteo_files")

        # Création
        self.create_directory(meteo_files_path + "/" + year_month)

        print("Le répertoire {} a été créé ou existe".format(year_month))


def test0():
    tools = MeteoTools()
    print(os.listdir("meteo_files"))

    # fichier
    files_path = tools.get_absolute_path("beautiful_meteo.py")
    print(files_path)

    # fichier
    files_path = tools.get_absolute_path("Copyright")
    print(files_path)

    # répertoire
    meteo_files_path = tools.get_absolute_path("meteo_files")

    # /media/data/3D/projets/meteo/meteo_forecast/meteo_files
    print(meteo_files_path)


    tools.create_directory(meteo_files_path + "/2017_09")

    # en 1 ligne
    tools.create_dir_year_month_in_meteo_files("2018_01")

def test1():
    tools = MeteoTools()

    # test
    key = '2015_03_22_05'

    # real date time: 2015-03-22 05:00:00
    real_date_time = tools.get_real_date_time(key)

    # 13 jours suivant
    thirteen_days = tools.get_thirteen_days(real_date_time)

    # 2015_03_22_05_45
    date_hour_mn_key = tools.get_date_hour_mn_key_from_datetime(real_date_time)

    # 2015_03_22
    date_key = tools.get_date_key_from_datetime(real_date_time)

    # 2015_03_22_05
    date_hour_key = tools.get_date_hour_key_from_datetime(real_date_time)


    print(  "key", key, "\n",
            "real_date_time", real_date_time, "\n",
            "thirteen_days", thirteen_days, "\n",
            "date_hour_mn_key", date_hour_mn_key, "\n",
            "date_key", date_key, "\n",
            "date_hour_key", date_hour_key, "\n"
            )

    # Tous les fichiers dans /file
    file_dir = "meteo_files"
    file_dict = tools.get_all_files(file_dir)
    tools.print_all_key_value(file_dict)

    # Test écriture, lecture
    data = {1: "gshjh", 2:"ghghgh"}
    json_data = tools.data_to_json(data)
    tools.write_data_in_file(json_data, "toto1.txt")

    print("Get some", key)
    key = "2015_03_22_05_00"
    print(  "year", tools.get_year(key),
            "month", tools.get_month(key),
            "day", tools.get_day(key),
            "hour", tools.get_hour(key),
            "year_month_day", tools.get_year_month_day(key))

def test2():
    tools = MeteoTools()
    files_dict = tools.get_all_files("meteo_files")
    files_list = tools.files_dict_to_list(files_dict)
    print(files_list, len(files_list))




if __name__ == "__main__":

    test2()
