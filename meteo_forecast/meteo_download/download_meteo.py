#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# download_meteo.py

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

    def downloadFile(self, file_name):
        '''Télécharge et enregistre un fichier.
        Cette fonction fait 2 choses, il faudrait 2 fonctions !
        file_name avec chemin absolu
        '''

        # Open the url
        try:
            page = urllib.request.urlopen(self.url)

            # Open our local file for writing
            local_file = open(file_name, "w")

            # Write to our local file
            decoded_page = page.read().decode("utf-8")

            # Ajout d'un EOF
            decoded_page += "\n"

            local_file.write(decoded_page)
            local_file.close()

        # handle errors
        except HTTPError as e:
                print("HTTP Error:", e.code)
        except URLError as e:
                print("URL Error:", e.reason)

    def create_path_file_name(self):
        '''Crée le nom du fichier qui sera enregisté dans un dossier par mois
        exemple: meteo_files/2017_06/meteo_2017_06_11_16_23.html
        '''

        today = datetime.datetime.today()

        # Nom du répertoire
        year_month = '{:%Y_%m}'.format(today)

        # Création du répertoire si besoin
        self.tools.create_dir_year_month_in_meteo_files(year_month)

        # Nom du fichier avec son chemin absolu
        name = '{:meteo_files/%Y_%m/meteo_%Y_%m_%d_%H_%M_%S.html}'.format(today)

        if self.debug:
            print("Nom du chemin et fichier", name)

        return name

    def every_hour_loop(self):
        '''Teste toutes les mn si l'heure est ok'''

        while 1:
            today = datetime.datetime.today()
            if self.debug:
                print("Minutes =", '{: %M}'.format(today))

            # Nom du fichier dans le dossier file
            file_name = self.create_path_file_name()

            if '{: %M}'.format(today) == " 05":
                print("Téléchargement de:", file_name)
                self.downloadFile(file_name)

            if self.debug:
                print("Téléchargement de:", file_name)
                self.downloadFile(file_name)

            sleep(5)


def main():
    # Pour test
    debug = 1

    # Url d'orléans
    meteo_url = "http://www.meteofrance.com/previsions-meteo-france/orleans/45000"

    print("Boucle de téléchargement des prévisions meteo toutes les heures.")

    # Téléchargement toutes les heures
    meteo = DownloadMeteo(meteo_url, debug)
    meteo.every_hour_loop()


if __name__ == '__main__':
    main()
