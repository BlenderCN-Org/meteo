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

Lit tous les fichiers à analyser, analyse
avec BeautifulMeteo
ou BeautifulMeteoNew
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
from beautiful_meteo_new import BeautifulMeteoNew
from get_config import GetConfig
from meteo_tools import MeteoTools
#from collections import OrderedDict


class UnAnalysed(GetConfig):
    """Recherche dans les dossiers les fichiers pas encore analysés.
    all = {     '2017_08': ['meteo_2017_08_03_16_05_39.html'],
                '2017_09': ['meteo_2017_09_03_16_05_39.html']}

    analysed = {'2017_08': ['meteo_2017_08_05_16_05_39.html'],
                '2017_09': []}
    """

    def __init__(self):
        super().__init__()

        self.debug = self.conf["test"]["debug"]
        self.meteo_files = self.conf["directory"]["meteo_files"]
        self.analysed_dir = self.conf["directory"]["analysed_dir"]
        self.tools = MeteoTools()

    def get_unanalysed(self):
        """Retourne les fichiers non analysés dans une liste,
        avec chemin absolu.
        """

        tous = self.tools.get_all_files(self.meteo_files)
        vu  = self.tools.get_all_files(self.analysed_dir)

        tous_list = self.tools.files_dict_to_list(tous)
        vu_list = self.tools.files_dict_to_list(vu)

        # All items from tous_list that are not in vu_list
        pas_vu = [item for item in tous_list if item not in vu_list]

        return pas_vu


class MeteoFilesBatch(UnAnalysed):
    """Recherche dans les dossiers les fichiers pas encore analysés,
    puis les analyse avec BeautifulMeteo.
    """

    def __init__(self):
        super().__init__()

    def get_date(self, fichier):
        """Retourne 0 si avant le 2017_08_02 à 00h00, 1 sinon
        avec chemin relatif:
        fichier = /meteo_files/2017_06/meteo_2017_06_11_16_05_30.html
        """

        # key = 2017_06_11_16
        key = fichier[27:-5]
        real_date = self.tools.get_real_date_time(key)
        print(key, real_date)

        if 1:
            new = 1
        else:
            new = 0
        return new

    def analyse(self, pas_vu):
        """Analyse en fonction de la date du fichier.
        Fichiers dans une liste.
        """

        for f in pas_vu:
            # à partir du 2017_08_02 à 00h00
            if 1:
                result = self.analyse_beautiful_meteo_new(f)
            else:
                result = self.analyse_beautiful_meteo(f)

    def analyse_beautiful_meteo(self, fichier):
        """Fichier: nom avec chemin absolu."""

        bm = BeautifulMeteo(fichier)

    def analyse_beautiful_meteo_new(self, fichier):
        bmn = BeautifulMeteoNew(fichier)

    def forecast_to_global_dict():

        pass



def main():
    mfb = MeteoFilesBatch()
    pas_vu = mfb.get_unanalysed()
    mfb.analyse(pas_vu)


if __name__ == "__main__":

    main()
