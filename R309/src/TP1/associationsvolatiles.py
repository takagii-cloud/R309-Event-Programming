import threading
import time

class TableDns:
    """Classe permettant de gérer une table DNS"""
    def __init__(self, ttl):
        """Initialisation de la classe TableDns"""
        self.ttl = ttl
        self.table = {}
        self.verrou = threading.Lock()
        self.thread_nettoyage = threading.Thread(target=self.nettoyer_entrees_expirees)
        self.thread_nettoyage.daemon = True
        self.thread_nettoyage.start()

    def ajouter_entree(self, addr_sym, addr_ip):
        """Méthode permettant d'ajouter une entrée dans la table DNS"""
        with self.verrou:
            tps_expiration = time.time() + self.ttl
            self.table[addr_sym] = (addr_ip, tps_expiration)
            print(f"Ajouté : {addr_sym} -> {addr_ip} (expire dans {self.ttl} secondes)")

    def obtenir_ip(self, addr_sym):
        """Méthode permettant d'obtenir l'adresse IP associée à une adresse symbolique"""
        with self.verrou:
            entree = self.table.get(addr_sym)
            if entree and entree[1] > time.time():
                return entree[0]
            else:
                return None

    def nettoyer_entrees_expirees(self):
        """Méthode permettant de nettoyer les entrées expirées"""
        while True:
            with self.verrou:
                temps_actuel = time.time()
                cles_expires = [cle for cle, (_, temps_exp) in self.table.items() if temps_exp <= temps_actuel]
                for cle in cles_expires:
                    del self.table[cle]
                    print(f"Entrée expirée supprimée : {cle}")
            time.sleep(1)

table_dns = TableDns(ttl=5)
table_dns.ajouter_entree("takagii.jp", "192.168.16.1")

time.sleep(3)
print("IP pour takagii.jp :", table_dns.obtenir_ip("takagii.jp"))

time.sleep(3)
print("IP pour takagii.jp après expiration :", table_dns.obtenir_ip("takagii.jp"))
