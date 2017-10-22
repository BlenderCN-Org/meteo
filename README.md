## Bangs de météo
#### Les prévisions de chaque jour sont matérialisées dans blender

### License and Copyright

Ce jeu est sous Creative Commons Attribution-ShareAlike 3.0 Unported License.

Les scripts sont sous GNU GENERAL PUBLIC LICENSE Version 2.

Pour plus détails, voir le fichier License.

#### Principe
Sauvegarde des prévisions de Meteo France pour la ville de Gotham toutes les heures.

#### Visualisation dans Blender
Les prévisions pendant 14 jours de chaque jour créent un histogramme des températures mini et maxi, avec une icône du type de temps par jour, les jours défilent automatiquement, ou manuellement.

Raccoucis:
* Espace: bascule auto/manu
* Up:    avance de 1 jour
* Down:  recul de 1 jour
* Left:  recul de 10 jours
* Right: avance de 10 jours

### Testé sur
* Debian Jessie 8.3
Avec:
* python 3.4
* OpenCV 3.3.0-rc
* Blender 2.72

### Installation
#### Blender

~~~text
sudo apt-get install blender
~~~

#### Beautifulsoup

~~~text
sudo apt-get install python3-bs4
~~~

### Serveur
Le script meteo_download.py enregistre les prévisions toutes les heures.
Il doit tourner en permanence.

#### Dossiers et fichiers à copier sur le serveur

* Coller meteo_download et autorestart.sh dans /home/utilisateur_courant

#### Crontab

Permet de lancer des tâches répétitives

Edition

~~~text
 crontab -e
~~~

ajouter

~~~text
 1 */1 * * * sh ./autorestart.sh > /tmp/autorestart.log
~~~

Lance l'action toutes les heures à 1 mn

### Merci à:

* Labomedia
