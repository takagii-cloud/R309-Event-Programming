from abc import ABC, abstractmethod
import socket
import threading

# Classe abstraite ClientServeur
class ClientServeur(ABC):

    @abstractmethod
    def envoyerMsg(self, message, adresse):
        pass

    @abstractmethod
    def recevoirMsg(self):
        pass

# Classe abstraite ClientServeurUDP héritant de ClientServeur
class ClientServeurUDP(ClientServeur):
    def __init__(self, host='', port=9000):  
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))

    def envoyerMsg(self, message, adresse):
        self.sock.sendto(message.encode(), adresse)

    def recevoirMsg(self):
        data, addr = self.sock.recvfrom(1024)
        return data.decode(), addr

# Classe EchoUDPServer héritant de ClientServeurUDP
class EchoUDPServer(ClientServeurUDP):
    def start(self):
        print(f"Serveur Echo UDP démarré sur {self.host}:{self.port}")
        while True:
            message, client_addr = self.recevoirMsg()
            response = f"Echo de {self.host} {self.port}: {message}"
            self.envoyerMsg(response, client_addr)

# Classe EchoUDPClient héritant de ClientServeurUDP
class EchoUDPClient(ClientServeurUDP):
    def envoyerMsg(self, message, adresse):
        super().envoyerMsg(message, adresse)
        response, _ = self.recevoirMsg()
        print(f"Réponse du serveur: {response}")

# Classe abstraite ServeurUDPMT (Multi-Thread)
class ServeurUDPMT(ClientServeurUDP, ABC):
    def __init__(self, host='', port=9001):
        super().__init__(host, port)

    @abstractmethod
    def traiterClient(self, message, client_addr):
        pass

    def start(self):
        print(f"Serveur UDP Multi-Thread démarré sur {self.host}:{self.port}")
        while True:
            message, client_addr = self.recevoirMsg()
            thread = threading.Thread(target=self.traiterClient, args=(message, client_addr))
            thread.start()

# Classe EchoUDPServerMT héritant de ServeurUDPMT
class EchoUDPServerMT(ServeurUDPMT):
    def traiterClient(self, message, client_addr):
        thread_name = threading.current_thread().name
        response = f"[{thread_name}] Echo: {message}"
        self.envoyerMsg(response, client_addr)

# Exemple d'utilisation
if __name__ == "__main__":
    choix = input("Mode Serveur (S), ou Client (C) ? : ").lower()
if choix == 's':
    mode = input("Mode simple (1) ou multi-thread (2) ? : ")
    if mode == '1':
        serveur = EchoUDPServer(host='', port=9000)  # Serveur simple sur le port 9000
        serveur.start()
    elif mode == '2':
        serveur_mt = EchoUDPServerMT(host='', port=9001)  # Serveur multithread sur le port 9001
        serveur_mt.start()
elif choix == 'c':
    client = EchoUDPClient(host='', port=0)  # Port client dynamique
    serveur_host = input("Entrez l'adresse IP du serveur : ")
    serveur_port = int(input("Entrez le port du serveur : "))
    while True:
        message = input("Message à envoyer : ")
        client.envoyerMsg(message, (serveur_host, serveur_port))
