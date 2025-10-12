
# 07/02 :

- L'outil LoRattack semble bien installé et configuré.
- Nous pouvons capturer et analyser des paquets de notre réseau légitime grâce à l'outil (sniffing).
- Cependant le replay attack ne marche pas encore.


---

 # Semaine 10/02 :

Nous parvenons correctement à sniffer les paquets (join_request, join_accept et data_up), en effet nous les voyons apparaitre en direct dans le terminal. Cependant ils ne sont pas toujours enrigistrés en pcap, ce qui est nécessaire pour le replay.

Cela vient probablement de la maniere de stopper le sniffing (actuellement avec Ctrl +C), ou alors du filtrage des paquets à enregistrer qui peut etre trop strict. Nous allons alors modifier le code analyzer.py pour tenter de corriger cela.


➡️Finalement c'est bon, il faut seulement capturer un peu moins de paquets (pour réduire la durée d'attente) et attendre lorsque nous stoppons le sniffing pour laisser le temps de sauvegarder les trames dans un fichier.

On a ainsi un fichier pcap contenant un join_request, un join_accept, et un data_up, que nous pourrons modifier en fonction du type de replay que nous souhaitons mettre en place.

## Problème : Sélection de la séquence à rejouer

Lorsque nous souhaitons lancer l'attaque par rejeu depuis ce fichier, voici le message affiché :

    No sequence file found in the session directory: session/data/REPLAY/sequence

➡️ Solution : Dans LoRattack, dans la partie Attack > Replay, sélectionner Edit replay sequence afin de choisir la séquence à rejouer.

Dans notre cas, nous allons tenter de rejouer le join_request (que pour l'exemple), qui est le premier paquet. Il suffit donc d'inscrire un "1" dans le fichier sequence.


## Problème : Underflow lors du replay

Lorsque nous mettons en marche le replay, nous rencontrons l'erreur suivante :

Uusrp_sink :error: In the last 2472 ms, 1 underflows occurred.

UUUUUUUusrp_sink :error: In the last 799 ms, 7 underflows occurred.

UUUUUUUUusrp_sink :error: In the last 803 ms, 8 underflows occurred.

➡️ Interprétation :
Cela signifie que l'émetteur ne reçoit pas assez de données en temps réel pour transmettre correctement le signal. Concrètement, l’USRP attend des données, mais elles arrivent en retard ou en quantité insuffisante, ce qui provoque des interruptions dans l’émission du signal.

🔍 Tentatives de correction

🔹 Modification du buffer

Ajout d'une ligne dans LoRa_transmitter :

    self.uhd_usrp_sink_0.set_min_output_buffer(2**20)

✅ Testé, mais toujours pas de résultat.

Tentative d'exportation d'une variable pour augmenter la taille du buffer :

    export UHD_OUTPUT_BUFFER_SIZE=100000000

❌ Toujours pas de résultat.

Tentative avec une autre variable UHD :

    UHD_TRANSPORT_TX_SO_SNDBUF=10000000 ./run.sh

❌ Toujours pas de résultat.

🔹 Réduction du gain en transmission

 Diminution du gain du signal émis, de 70 à 10.
 
❌ Pas d'amélioration.

🔹 Réduction du sample rate

Test avec une baisse du sample rate du transmetteur jusqu’à 0.25 MHz.

❌ Toujours le même problème.

🔹 Charge processeur / limitations matérielles

Vérification si le problème vient d’une surcharge du processeur.

Fermeture de tous les processus non nécessaires et exécution du test uniquement avec le terminal ouvert.

❌ Le problème persiste.

    sudo -E chrt -f 99 ./run.sh

❌ Pas d'amélioration.


Configuration de la clock master : la source de la clock de l'USRP est bien en interne, mais ça ne fonctionne quand même pas.

Le port USB est bien en 3.0 à une vitesse normalement suffisante.


# On abandonne ainsi cet outil pour l'instant pour tenter le replay avec un arduino.