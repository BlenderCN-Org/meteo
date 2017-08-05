# Poussières de météo
## Plus les prévisions météo sont mauvaises, plus les poussières s'agitent.

### License and Copyright

Ce jeu est sous Creative Commons Attribution-ShareAlike 3.0 Unported License.

Les scripts sont sous GNU GENERAL PUBLIC LICENSE Version 2.

Pour plus détails, voir le fichier License.

### ça fait quoi ?
#### Principe
Sauvegarde des prévisions de Meteo France pour la ville d'Orléans toutes les heures.
Les mauvaises prévisions vont faire s'agiter des poussières dans le Game Engine de Blender 3D.


### Testé sur
* Debian Jessie 8.3 avec Blender 2.72

### Installation
#### Blender

~~~text
sudo apt-get install blender
~~~

#### Twisted


#### Beautifulsoup


#### Installation OpenCV
Sur debian jessie 8.3 et python 3.4

http://remananr.com/Blog/opencv-in-python3/

~~~text
sudo apt-get install libopencv-dev python-opencv
sudo apt-get install build-essential cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
sudo apt install python3-dev libpython3.4-dev python3-numpy
python3.4-config --includes
~~~

Dans CMakeLists.txt, pour éviter une erreur incompréhensible comme quoi il ne faut pas compiler dans le dossier de sources, j'ai commenté les lignes 10 à 15

Dans votre dossier projets

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


« Bonne chance pour une prochaine fois, tas de nullards ! » Boum ! Envoyé ! Je suis bien l'invincible !

### Merci à:

* Labomedia
