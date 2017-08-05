#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## meteo_files_batch.py

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
Les fichiers des prévisions meteo à 45000 sont enregistrés dans:
    meteo_files/2017_06/
    meteo_files/2017_07/
    meteo_files/2018_01/

    Tous les fichiers sont du type meteo_2017_06_11_16_05_30.html

Résultat de l'analyse d'un mois:
    analysed/result_2017_08.txt

Suivi des fichiers analysés:
    analysed_files.txt dans meteo_forecast

Résultat de calcul des écarts
    gaps/gaps_2017_08.txt

Suivi des calculs des écarts:
    gaps_files.txt dans meteo_forecast

Lit tous les fichiers à analyser, analyse avec
    BeautifulMeteo.forecast =
    {'2017_07_29_01': { '2017_08_10': ['jeudi 10', 13, 26, 'Éclaircies'],
                        '2017_08_06': ['dimanche 06', 14, 26, 'Éclaircies'],
                        '2017_08_11': ['vendredi 11', 13, 26, 'Éclaircies'],
                        '2017_08_08': ['mardi 08', 14, 26, 'Éclaircies'],
                        ..... }}

"""

import os, sys
from json import dumps
from beautiful_meteo import BeautifulMeteo
from get_config import GetConfig
#from collections import OrderedDict


## Variable globale à définir
# Le dossier avec les fichiers à lire
file_dir = "meteo_files"

# Les fichiers de destination des json des résultats des analyses du mois
result_file = "result_2017_08.txt"

# La liste des fichiers analysés
analysed_files = "analysed_files.txt"

# Le json des écarts du mois dans un json
gaps_file = "gaps_2017_08.txt"


class UnAnalysed(GetConfig):
    """Recherche dans les dossiers les fichiers pas encore analysés."""

    def __init__(self, file_path_name):
        """."""

        super().__init__()

        self.meteo_conf = self.conf
        self.debug = meteo_conf["test"]["debug"]
        self.meteo_files = meteo_conf["directory"]["meteo_files"]

    def get_unanalysed(self):
        pass


class MeteoFilesBatch(UnAnalysed, GetConfig):
    """Recherche dans les dossiers les fichiers pas encore analysés,
    puis les analyse avec BeautifulMeteo.
    """

    def __init__(self, file_path_name):
        '''Chemin absolu avec nom du fichier.'''

        super().__init__()

        meteo_conf = self.conf
        self.debug = meteo_conf["test"]["debug"]

    def forecast_to_global_dict(file_list_sorted):
        global_dict = {}

        for fichier in file_list_sorted:
            #forecast = get_forecast("file/" + fichier)
            forecast  = BeautifulMeteo(fichier)
            forecast.get_forecast()
            for k, v in forecast.forecast.items():
                global_dict[k] = v

        return global_dict



def main(file_dir, fichier):
    # Liste des fichiers dans le dossier file
    file_list = get_file_list(file_dir)
    print("Nombre de fichier =", len(file_list))

    # Analyse des fichiers triés
    global_dict = forecast_to_global_dict(file_list_sorted)

    # Ecriture dans un fichier du json
    fichier = "first_new_1.txt"
    write_json(global_dict, fichier)

if __name__ == "__main__":

    main(file_dir, fichier)
