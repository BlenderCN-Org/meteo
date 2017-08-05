#!/usr/bin/python3
# -*- coding: UTF-8 -*-

## labtcpclient.py

#############################################################################
# Copyright (C) Labomedia  March 2017
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


# 2017 07 09 modif send pour retour d'erreur si envoi raté


import socket
from time import sleep


class LabTcpClient:
    '''Envoi et réception sur le même socket en TCP.
    Toutes les méthodes sont sans try.
    '''

    def __init__(self, ip, port):

        self.ip = ip
        self.port = port
        self.server_address = (ip, port)
        self.data = None
        self.sock = None
        self.create_socket()

    def create_socket(self):
        '''Création du socket sans try, et avec connexion.'''

        while not self.sock:

            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect(self.server_address)

            print("    Création du socket client {}".format(self.server_address))

            sleep(0.1)

    def send(self, msg):
        '''Envoi d'un message, avec send, msg doit être encodé avant.'''

        # Création d'un socket si besoin
        if not self.sock:
            self.create_socket()

        # Envoi
        try:
            self.sock.send(msg)
        except:
            print("Envoi raté: {}".format(msg))
            # Nouvelle création d'une socket
            self.sock.close()
            self.sock = None

    def reconnect(self):
        '''Reconnexion.'''

        self.sock = None
        self.create_socket()

    def close(self):
        '''Fermeture de la socket.'''

        self.sock.close()
        self.sock = None

    def listen(self):
        '''Retourne les data brutes reçues.'''

        raw_data = None

        raw_data = self.sock.recv()

        return raw_data


if __name__ == "__main__":

    ip = "127.0.0.1"
    port = 6666

    int_list = [x for x in range(20)]

    clt = LabTcpClient(ip, port)

    for num in int_list:
        num = str(num).encode("utf-8")
        print(num)
        sleep(0.1)
        clt.send(num)

    clt.close()
