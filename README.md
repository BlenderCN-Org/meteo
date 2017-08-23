# Bangs de météo
## Plus les prévisions météo sont mauvaises, plus les images vont lancé des bangs.

### License and Copyright

Ce jeu est sous Creative Commons Attribution-ShareAlike 3.0 Unported License.

Les scripts sont sous GNU GENERAL PUBLIC LICENSE Version 2.

Pour plus détails, voir le fichier License.

### ça fait quoi ?
#### Principe
Sauvegarde des prévisions de Meteo France pour la ville de Gotham toutes les heures.
Les mauvaises prévisions vont faire des bangs dans une fenêtre OpenCV .


### Testé sur
* Debian Jessie 8.3 avec OpenCV 3.3.0-rc en python 3.4


Une variante est possible dans Blender 2.72 si j'en ai le courage !

### Installation
#### Blender

~~~text
sudo apt-get install blender
~~~

#### Twisted


#### Beautifulsoup


#### Installation OpenCV
Il existe un tas de tuto qui explique comment compiler opencv, mais ces tutos sont des reprises d'un pov gars qui a trouvé intelligent de le faire dans un virtualenv, même les chinois ont copié !

##### Labomedia ne compile pas dans un virtualenv
Réalisé sur debian jessie 8.3 et python 3.4 avec CmakeGUI Qt

http://remananr.com/Blog/opencv-in-python3/

~~~text
sudo apt-get install libopencv-dev python-opencv
sudo apt-get install build-essential cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
sudo apt install python3-dev libpython3.4-dev python3-numpy
python3.4-config --includes
~~~

Dans CMakeLists.txt, pour éviter une erreur incompréhensible comme quoi il ne faut pas compiler dans le dossier de sources, j'ai commenté les lignes 10 à 15

Dans votre dossier projets:

~~~text
git clone https://github.com/opencv/opencv.git
cd opencv
mkdir build
cd build
~~~

Utiliser CmakeGUI Qt
voir http://implab.ce.unipr.it/?p=21
Définir:

* Répertoire sources
* Répertoire destination

puis clic sur Generate
Ouvrir un terminal dans le dossier des sources

~~~text
make -j8
sudo make install
~~~

Quel film ?
« Bonne chance pour une prochaine fois, tas de nullards ! » Boum ! Envoyé ! Je suis bien l'invincible !

### Merci à:

* Labomedia
