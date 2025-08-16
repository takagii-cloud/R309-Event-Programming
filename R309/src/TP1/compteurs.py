import threading
import time

class Compteur(threading.Thread):
    """Classe permettant de créer un compteur qui s'incrémente ou se décrémente en fonction des paramètres"""
    def __init__(self, nom, value, pas, sens, nb_comptages, periode):
        """Initialisation de la classe Compteur"""
        threading.Thread.__init__(self)
        self.nom = nom
        self.value = value
        self.pas = pas
        self.sens = sens
        self.nb_comptages = nb_comptages
        self.periode = periode

    def run(self):
        """Méthode permettant de lancer le compteur"""
        for i in range(self.nb_comptages):
            if self.sens == 'montant':
                self.value += self.pas
            else:
                self.value -= self.pas
            print(f"value du {self.nom} : {self.value}")
            time.sleep(self.periode)

compteur1 = Compteur(nom="Compteur1", value=0, pas=1, sens='montant', nb_comptages=10, periode=2)
compteur2 = Compteur(nom="Compteur2", value=50, pas=1, sens='descendant', nb_comptages=5, periode=1)

compteur1.start()
compteur2.start()

compteur1.join()
compteur2.join()

print("Les deux compteurs ont terminé.")
