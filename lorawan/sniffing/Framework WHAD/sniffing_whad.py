from whad.device import WhadDevice
from whad.lorawan.connector import LoRaWAN
from whad.lorawan.channel import ChannelPlan, Uplink, Downlink, DataRate

# Create our freq plan
class MyChannelPlan(ChannelPlan):
    def __init__(self):
        super().__init__(
            channels = [
                Uplink(1, 868100000, 0),
                Downlink(1, 868100000, 0)
            ],
            datarates = [
                DataRate(sf=7, bw=125000),
                DataRate(sf=12, bw=125000)
            ],

            rx2=Downlink(1, 868100000, 1)
        )


try:
    print("Connexion à l'Arduino sur /dev/ttyACM0...")
    device = WhadDevice.create('/dev/ttyACM0')  # port série de l'Arduino
    lwan = LoRaWAN(device, channel_plan=MyChannelPlan())  # Configurer LoRaWAN avec le plan de canaux

    # Démarrer l'écoute
    print("Démarrage de l'écoute des paquets LoRaWAN...")
    lwan.start()

    # Boucle pour écouter les paquets reçus
    while True:
        print("En attente de paquets...")
        packet = lwan.wait_packet()  # Attendre un paquet
        print("Paquet reçu :")
        packet.show()  # Afficher les détails du paquet reçu

except Exception as e:
    print(f"Erreur : {e}")
