## Bangs de météo
#### Plus les prévisions météo sont mauvaises, plus il y aura de bangs.

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
Les prévisions pendant 14 jours de chaque jour créent un histogramme, les jours défilent automatiquement, ou manuellement.

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

#### Installation OpenCV
Il existe un tas de tutos qui expliquent comment compiler opencv, mais ces tutos sont des reprises d'un pov'gars qui a trouvé intelligent de le faire dans un virtualenv, bien sûr les chinois ont copié !

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

« Bonne chance pour une prochaine fois, tas de nullards ! Boum ! Envoyé ! Je suis bien l'invincible ! »

### OpenCV
cv2.imshow() n'affiche pas le canal alpha d'une image, matplotlib le fait mais avec un faible fps.

OpenCV charge les images avec le canal alpha, certaines fonctions utilise le canal alpha,
mais par exemple cv2.add() ne fait pas la somme avec les canaux alpha, il les ignore,
d'où le cv2.threshold() de la doc, qui crée un masque, mais l'image collée dans le masque se fera sans prendre en compte le canal alpha.

Un post du forum opencv propose:
"Faîtes-vous même votre méthode !"

Je vais faire simple, un seul bang à la fois, ou + si je suis courageux.

### Merci à:

* Labomedia

