#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# download_meteo.py

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
import datetime
import urllib.request
from urllib.error import HTTPError,URLError
from meteo_tools import MeteoTools


class DownloadMeteo:

    def __init__(self, url, debug):
        self.url = url
        self.debug = debug
        self.tools = MeteoTools()
        self.page = "\n"

    def download_file(self):
        """Télécharge et enregistre un fichier.
        Cette fonction fait 2 choses, il faudrait 2 fonctions !
        file_name avec chemin absolu
        """

        # Open the url
        try:
            page = urllib.request.urlopen(self.url)
            self.page = page.read().decode("utf-8")
            # Ajout d'un EOF
            self.page += "\n"

        # handle errors
        except HTTPError as e:
                print("HTTP Error:", e.code)
        except URLError as e:
                print("URL Error:", e.reason)

    def write_file(self, file_name):
        """Ecrit la page html dans un fichier."""

        with open(file_name, 'w') as my_file:
            my_file.write(self.page)

        my_file.close()

    def create_path_file_name(self):
        """Crée le nom du fichier qui sera enregisté dans un dossier par mois
        exemple: meteo_files/2017_06/meteo_2017_06_11_16_23.html
        """

        today = datetime.datetime.today()

        # Nom du répertoire
        year_month = '{:%Y_%m}'.format(today)

        # Création du répertoire si besoin
        self.tools.create_dir_year_month_in_meteo_files(year_month)

        # Nom du fichier avec son chemin absolu
        name = "{:meteo_files/%Y_%m/meteo_%Y_%m_%d_%H_%M_%S.html}".format(today)

        if self.debug:
            print("Nom du chemin et fichier", name)

        return name

    def download_and_write(self, file_name):
        """download_and_write"""
        
        print("Téléchargement de:", file_name)
        self.download_file()
        self.write_file(file_name)

    def every_hour_loop(self):
        """Teste toutes les mn si l'heure est ok"""

        while 1:
            today = datetime.datetime.today()
            if self.debug:
                print("Minutes =", '{: %M}'.format(today))

            # Nom du fichier dans le dossier file
            file_name = self.create_path_file_name()

            if '{: %M}'.format(today) == " 05":
                self.download_and_write(file_name)

            if self.debug:
                self.download_and_write(file_name)

            sleep(60)


def main():
    """Lancement de ce script"""
    
    # Pour test
    debug = 0

    # Url d'orléans
    meteo_url = "http://www.meteofrance.com/previsions-meteo-france/orleans/45000"

    print("Boucle de téléchargement des prévisions meteo toutes les heures.")

    # Téléchargement toutes les heures
    meteo = DownloadMeteo(meteo_url, debug)
    meteo.every_hour_loop()


if __name__ == '__main__':
    main()
