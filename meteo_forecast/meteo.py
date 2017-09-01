#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## meteo.py

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
Permet de tester ou de lancer tout.
"""

from beautiful_meteo import BeautifulMeteo
from beautiful_meteo_new import BeautifulMeteoNew
from get_config import GetConfig
from meteo_files_batch import MeteoFilesBatch


class Meteo(GetConfig):

    def __init__(self):
        super().__init__()

    def test_beautiful_meteo(self):
        # Chemin relatif
        file_path_name = "meteo_files/2017_07/meteo_2017_07_29_01_05_09.html"

        forecast = BeautifulMeteo(self.conf, file_path_name)
        forecast.get_forecast()

        print("Prévisions\n",forecast.forecast)

    def test_beautiful_meteo_new(self):
        # Chemin relatif
        file_path_name =  "meteo_files/2017_08/meteo_2017_08_05_18_18_14.html"

        forecast = BeautifulMeteoNew(self.conf, file_path_name)
        forecast.get_forecast()

        print("Prévisions\n", forecast.forecast, "\n")

    def test_meteo_files_batch(self):

        mfb = MeteoFilesBatch(self.conf)
        pas_vu = mfb.get_unanalysed()

        mfb.analyse(pas_vu)


if __name__ == "__main__":

    meteo = Meteo()

    meteo.test_beautiful_meteo()

    meteo.test_beautiful_meteo_new()

    meteo.test_meteo_files_batch()
