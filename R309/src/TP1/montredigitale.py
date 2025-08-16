from threading import Thread
import time

class Montre(Thread):
    """Classe permettant de créer une montre digitale"""
    def __init__(self, h, m, s, mode24=True):
        """Initialisation de la classe Montre"""
        assert isinstance(h, int) and 0 <= h < 24
        assert isinstance(m, int) and 0 <= m < 60
        assert isinstance(s, int) and 0 <= s < 60
        Thread.__init__(self)
        self.h = h
        self.m = m
        self.s = s
        self.mode24 = mode24

    def __str__(self):
        """Méthode permettant d'afficher l'heure"""
        if self.mode24:
            return "%02d:%02d:%02d" % (self.h, self.m, self.s)
        else:
            suffix = "PM" if self.h >= 12 else "AM"
            heure = self.h % 12 or 12
            return "%02d:%02d:%02d %s" % (heure, self.m, self.s, suffix)

    def run(self):
        """Méthode permettant de lancer la montre"""
        while True:
            print(self)
            time.sleep(1)
            self.s += 1
            if self.s == 60:
                self.s = 0
                self.m += 1
                if self.m == 60:
                    self.m = 0
                    self.h += 1
                    if self.h == 24:
                        self.h = 0

if __name__ == "__main__":
    while True:
        print("\nChoisissez le mode d'affichage :")
        print("1 - Mode 24 heures")
        print("2 - Mode 12 heures")
        choix = input("Entrez votre choix (1 ou 2) : ").strip()
        if choix == "1":
            mode24 = True
            break
        elif choix == "2":
            mode24 = False
            break
        else:
            print("Choix invalide. Essayez encore.")

    h, m, s = 15, 10, 30
    montre = Montre(h, m, s, mode24)
    montre.start()
