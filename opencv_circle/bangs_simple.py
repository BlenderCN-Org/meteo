class BangsSimple:
    '''Affichage de plusieurs bangs dans une image avec OpenCV.'''

    comptage = -1

    def __init__(self):
        # La boucle d'affichage
        self.loop = 1
        # Calcul du fps
        self.t_zero = time()
        self.freq = 0
        self.img = get_black_image()

        # Lancement d'une bang
        self.bang_one_start()
        # Lancement d'une autre bang
        self.bang_two_start()

        # Lancement de la fenêtre OpenCV
        self.display()

    def update_freq(self):
        '''Calcul et affichage du fps.'''

        self.freq += 1

        if time() - self.t_zero > 1:
            self.t_zero = time()
            print("Fréquence =", self.freq)
            self.freq = 0

    def bang_one(self, numero):
        global LINES

        n = 8
        # list et non tuple
        O = [200, 400]
        start = 20
        gap = 30
        ampli = 50
        pixel = 2

        # Déplacement linéaire de O sur x,y pendant 1s
        slide = 10, -20
        # Diminution de l'amplitude par seconde
        decrease = 200

        # Création d'une bang
        LINES[numero] = DynamicBang(O, n, start, gap, ampli, pixel, slide, decrease)
        LINES[numero].bang(numero)

    def bang_one_start(self):
        Bangs.comptage += 1
        numero = Bangs.comptage
        t1 = threading.Thread(target=self.bang_one, args=(numero,))
        t1.start()

    def bang_two(self, numero):
        global LINES
        n = 5
        O = [1000, 300]
        start = 20
        gap = 30
        ampli = 100
        pixel = 1

        # Déplacement linéaire de O sur x,y pendant 1s
        slide = -200, 80
        # Diminution de l'amplitude par seconde
        decrease = 300

        # Création d'une bang
        LINES[numero] = DynamicBang(   O, n, start, gap, ampli, pixel,
                                            slide, decrease)
        LINES[numero].bang(numero)

    def bang_two_start(self):
        Bangs.comptage += 1
        numero = Bangs.comptage
        t2 = threading.Thread(target=self.bang_two, args=(numero,))
        t2.start()

    def lines_to_circles(self, img, numero):

        global LINES
        img = LINES[numero].bang(img)
        return img

    def display(self):

        while self.loop:
            self.update_freq()

            # Recalcul de l'image avec toutes les lines
            img = get_black_image()
            key_list_to_remove = []
            for k, v in LINES.items():

                # Le coeur du calcul
                img = self.lines_to_circles(img, k)

                if v.ampli == 0:
                    print("LINES[{}] à supprimer".format(k))
                    key_list_to_remove.append(k)

            # Interdiction de supprimer une clé en cours de parcours
            for i in key_list_to_remove:
                del LINES[i]

            # StaticDisplay an image
            cv2.imshow("Ceci n'est pas une image", img)

            # wait for esc key to exit
            key = np.int16(cv2.waitKey(33))
            if key == 27:  # Echap
                break

        cv2.destroyAllWindows()
