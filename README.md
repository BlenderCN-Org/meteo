# Bangs de météo
## Plus les prévisions météo sont mauvaises, plus il y aura de bangs.

## C'est pas fini !

### License and Copyright

Ce jeu est sous Creative Commons Attribution-ShareAlike 3.0 Unported License.

Les scripts sont sous GNU GENERAL PUBLIC LICENSE Version 2.

Pour plus détails, voir le fichier License.

### ça fait quoi ?
#### Principe
Sauvegarde des prévisions de Meteo France pour la ville de Gotham toutes les heures.
Les mauvaises prévisions vont faire des bangs dans une fenêtre OpenCV.

#### Visualisation dans Blender
Les prévisions pendant 14 jours de chaque jour créent un histogramme, les jours défilent automatiquement.

### Testé sur
* Debian Jessie 8.3 avec OpenCV 3.3.0-rc en python 3.4


### Installation
#### Blender

~~~text
sudo apt-get install blender
~~~

#### Installation de twisted pour python 3

~~~text
sudo pip3 install twisted
~~~

#### Beautifulsoup

~~~text
sudo apt-get install python3-bs4
~~~

#### Installation OpenCV
Il existe un tas de tutos qui expliquent comment compiler opencv, mais ces tutos sont des reprises d'un pov'gars qui a trouvé intelligent de le faire dans un virtualenv, même les chinois ont copié !

##### Labomedia ne compile pas dans un virtualenv
Réalisé sur debian jessie 8.3 et python 3.4 avec CmakeGUI Qt

http://remananr.com/Blog/opencv-in-python3/

~~~text
sudo apt-get install libopencv-dev python-opencv
sudo apt-get install build-essential cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
sudo apt install python3-dev libpython3.4-dev python3-numpy
python3.4-config --includes
~~~

Récupération des sources:

~~~text
git clone https://github.com/opencv/opencv.git
~~~

###### CUDA
Dans Synaptic, installer python3-pycuda, cela va ajouter toutes les dépendances nécessaires !
Il faut toujours être fainéant !


###### Utiliser CmakeGUI Qt

voir http://implab.ce.unipr.it/?p=21

Définir:

* Répertoire sources
* Répertoire destination

puis clic sur Configure puis Generate

Ouvrir un terminal dans le dossier des sources

~~~text
make -j8
sudo make install
~~~

Quel film ?

« Bonne chance pour une prochaine fois, tas de nullards ! » Boum ! Envoyé ! Je suis bien l'invincible !

### Merci à:

* Labomedia

