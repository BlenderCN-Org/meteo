#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## main.py

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


"""
Script à lancer pour actualiser les prévisions,
après avoir récupérer les prévisions sur le serveur
Ensuite vous pouvez lancer le jeu
"""


from time import  sleep
from meteo_files_batch import MeteoFilesBatch
from gaps import MeteoGaps


def main():

    # meteo_flies_batch
    print("\nJe suis le 1er script à excécuter")
    print("Analyse des fichiers:\n")
    mfb = MeteoFilesBatch()
    mfb.get_unanalysed()

    mfb.analyse(mfb.unanalysed)
    mfb.record_analysed()

    mfb.record_forecast()

    print("\nAnalyse des fichiers terminée")
    print("Lancement de gaps.py")

    # gaps
    sleep(1)
    print("Pour une sortie bavarde, changer pour mg.debug = 1")
    print("2ème scripts et dernier à excécuter\n")

    mg = MeteoGaps()

    # Attribut modifiable
    mg.debug = 0

    # Liste de tous les jours dans forecasts, indépendemment de l'heure
    mg.get_all_days_in_forecasts()

    # Temps pseudo réél de chaque jour
    mg.get_real_weathers()

    # Clé en jours au lieu de jour_heure
    mg.inversion_du_dict_forecast()

    # Ecarts
    mg.set_gaps()
    mg.write_gaps()

    print("\nCalcul des écarts OK")
    print("Vous pouvez lancer le jeu")


if __name__ == "__main__":
    main()
