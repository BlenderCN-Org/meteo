#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## meteo_files_batch.py

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



# 1er fichier à faire tourner
# Analyse les fichiers téléchargés si pas encore analysés
# Le fichier analysed.txt doit exister et contenir au moins: []
# Le fichier forecast.txt doit exister et contenir au moins: {}
# TODO créer les fichiers en auto


from json import dumps, loads
from time import sleep
from datetime import datetime
from beautiful_meteo import BeautifulMeteo
from beautiful_meteo_new import BeautifulMeteoNew
from meteo_tools import MeteoTools


## Variable globale
# Le dossier avec tous les fichiers de Météo France
METEO_FILES_DIR = "meteo_files"

# Fichier non json, 1 ligne par fichier météo
ANALYSED = "output/analysed.txt"

# Le json des analyses, non trié
FORECAST = "output/forecast.txt"


class AnalysedManagement(MeteoTools):
    """Gestion des fichiers analysés, et pas encore analysés.
    analysed = liste des chemins relatifs
    meteo_files/2017_06/meteo_2017_06_11_22_05_42.html
    """

    def __init__(self):
        super().__init__()
        self.analysed = []
        self.unanalysed = []

    def get_analysed(self):
        """analysed.txt = json = liste de tous les analysés."""

        self.analysed = self.get_json_file(ANALYSED)
        if self.analysed == None:
            self.analysed = []

    def get_unanalysed(self):
        """Retourne les fichiers non analysés dans une liste,
        avec chemin absolu.
        """

        tous = self.get_all_files(METEO_FILES_DIR)
        tous_list = self.files_dict_to_list(tous)

        # Maj de self.analysed
        self.get_analysed()

        # All items from tous_list that are not in vu_list
        self.unanalysed = [item for item in tous_list if item not in self.analysed]

    def record_analysed(self):
        """Ajoute les listes analysed et unanalysed,
        puis enregistre le json
        """

        tous = self.analysed + self.unanalysed

        self.write_json_file(tous, ANALYSED)


class MeteoFilesBatch(AnalysedManagement):
    """Analyse avec BeautifulMeteo ou New les fichiers pas encore analysés."""

    def __init__(self):
        super().__init__()
        self.forecast = {}

    def new_or_not(self, fichier):
        """Retourne 0 si avant le 2017_08_02 à 00h00, 1 sinon
        avec chemin relatif:
        fichier = /meteo_files/2017_06/meteo_2017_06_11_16_05_30.html
        """

        # key = 2017_06_11_16

        key = fichier[26:-8]

        # Retourne 2017-06-11 16:00:00 avec 2017_06_11_16
        real_date = self.get_real_date_time(key)

        # à partir du 2017_08_02 à 00h00
        modif = datetime.strptime('2017_08_02_00_00', '%Y_%m_%d_%H_%S')

        # Comparaison
        if real_date > modif:
            new = 1
        else:
            new = 0

        return new

    def analyse(self, pas_vu):
        """Analyse en fonction de la date du fichier.
        Fichiers dans une liste.
        """

        analysed = []
        for f in pas_vu:
            print("Fichier en cours d'analyse: {}".format(f))
            analysed.append(f)

            if self.new_or_not(f):
                result = self.analyse_beautiful_meteo_new(f)
            else:
                # Fichier avant le 2 août ne pose pas de pb
                try:
                    result = self.analyse_beautiful_meteo(f)
                except:
                    # il n'y a jamais d'exception
                    print("Fichier impossible à analyser !")
                    result = None

            if result:
                self.forecast_to_dict(result)

            sleep(0.1)

    def analyse_beautiful_meteo(self, fichier):
        """Fichier: nom avec chemin absolu."""

        bm = BeautifulMeteo(fichier)
        bm.get_forecast()
        result = bm.forecast

        return result

    def analyse_beautiful_meteo_new(self, fichier):
        """Fichier: nom avec chemin absolu."""

        bmn = BeautifulMeteoNew(fichier)
        bmn.get_forecast()
        result = bmn.forecast

        return result

    def forecast_to_dict(self, result):
        """"clé = meteo_files/2017_08/meteo_2017_08_05_08_05_20.html
        il faut 2017_08_07_01
        """

        self.forecast = self.dict_sum(self.forecast, result)

    def record_forecast(self):
        # Récup du précédent json
        data = self.read_file(FORECAST)

        try:
            data_dict = loads(data)
        except:
            data_dict = {}

        # Somme de 2 dictionnaires
        self.forecast = self.dict_sum(data_dict, self.forecast)

        # Write en "w"
        self.write_json_file(self.forecast, FORECAST)
        print("Sauvegarde dans forecast.txt ok")


def main():
    print("\nJe suis le 1er script à excécuter")
    print("Analyse des fichiers:\n")
    mfb = MeteoFilesBatch()
    mfb.get_unanalysed()

    mfb.analyse(mfb.unanalysed)
    mfb.record_analysed()

    mfb.record_forecast()

    print("\nAnalyse des fichiers terminée")
    print("Lancer ensuite le script gaps.py")


if __name__ == "__main__":
    main()
