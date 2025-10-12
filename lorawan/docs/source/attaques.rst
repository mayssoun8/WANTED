Attaques
========

Attaque sur clés basiques
*************************

Contexte
---------

Dans un réseau LoRaWAN agricole utilisant une version obsolète de LoRaMAC (comme la 1.0.x), plusieurs failles de sécurité sont présentes :

- **Ancienne version du protocole** : LoRaMAC 1.0.x utilise moins de clés de sécurité, ce qui le rend vulnérable par rapport à la version 1.1.x.
- **Identifiants faibles et prévisibles** : Certains DevEUI et AppKey comme `000...`, `111...`, ou `123...` sont faciles à deviner, facilitant les attaques par force brute.

Ces vulnérabilités rendent le réseau facile à attaquer. L'objectif est d'exploiter cette faiblesse liée au choix des identifiants.

Méthodologie de l'attaque
-------------------------

L'attaque repose sur la force brute du **DevEUI** et de l'**AppKey**, ce qui permet d'établir une connexion avec la passerelle et d'envoyer ensuite des données falsifiées.

Rappel des clés de sécurité dans LoRaMAC 1.0.x en utilisant OTAA
----------------------------------------------------------------

- **AppKey** : Sécurise l'activation OTAA et génère les clés de session.
- **AppSKey** : Chiffre/déchiffre les données utilisateur.
- **NwkSKey** : Assure l'intégrité des messages MAC.

Contre-mesures et recommandations
---------------------------------

- Mettre à jour vers **LoRaMAC 1.1.x** pour bénéficier des améliorations de sécurité.
- Utiliser des clés cryptographiques **complexes et aléatoires**, difficiles à deviner.
- **Renouveler régulièrement** les clés du réseau pour limiter l'exposition en cas de fuite.

Améliorations possibles
------------------------

- **Étendre la bibliothèque de clés** pour tester un plus grand nombre de combinaisons courantes dans les déploiements vulnérables.
- **Optimiser les délais d'attente** pour réduire le temps total d'exécution sans compromettre la fiabilité des tests.

Limites de l'attaque
--------------------

- **Temps d'exécution croissant** : Plus le nombre de clés testées est élevé, plus le temps de brute-force augmente de manière exponentielle.
- **Délais à respecter** : Chaque test doit respecter un délai (~10-15s) pour laisser la connexion s'établir.
- **Absence de ciblage précis** : L'attaque ne permet pas de choisir un réseau spécifique.

Lors des tests, nous avons pu rejoindre un réseau en utilisant des identifiants faibles comme :

- **DevEUI** : `1111111111111111`
- **AppKey** : `11111111111111111111111111111111`

Ou encore :

- **DevEUI** : `AAAAAAAAAAAAAAAA`
- **AppKey** : `AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA`

Ces valeurs n'étaient pas incluses dans notre banc de test initial, ce qui montre qu'un réseau avec de telles configurations était accessible.

**Conclusion** : Bien que l'attaque soit efficace contre des identifiants faibles, son efficacité dépend fortement du contexte et du nombre de clés testées.

Déploiement
-----------

Le code source de cette attaque est disponible dans le répertoire :  
``attaques/attaque_cles_basiques``

Deux plateformes matérielles peuvent être utilisées :

1. **Arduino Dragino**  
2. **LoPy4** (déjà utilisé comme nœud légitime, donc moins privilégié ici)

Utilisation avec LoPy4
~~~~~~~~~~~~~~~~~~~~~~
Si on veut quand même utiliser un **LoPy4** pour cette attaque, il suffit de flasher le code contenu dans :

``attaques/attaque_cles_basiques/pycom``  

via **Pymakr** sur un autre LoPy4, comme nous l'avons fait pour le nœud légitime.

Utilisation avec Arduino Dragino
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Avant de commencer, il faut installer la bibliothèque **MCCI LoRaWAN LMIC** disponible ici :  
`https://github.com/mcci-catena/arduino-lorawan.git`

Cette bibliothèque est disponible directement dans **Arduino IDE** et permet de créer un nœud LoRaWAN avec du matériel Arduino Dragino, ce qui est indispensable pour réaliser cette attaque.

Une fois la bibliothèque installée, il suffit de :

1. Ouvrir le fichier :  
   ``attaques/attaque_cles_basiques/arduino/attaquesArduino.ino``
2. Téléverser le code sur la carte :

   - Via **Arduino IDE**, puis observer le moniteur série.
   - Ou en ligne de commande :  
     ```
     arduino --upload attaqueArduino.ino --port /dev/ttyACM1
     ```
   - Pour voir la sortie, utiliser **minicom** :  
     ```
     minicom -D /dev/ttyACM1 -b 9600
     ```

---

Sniffing
********

Contexte
--------

Le sniffing LoRaWAN consiste à intercepter passivement les communications radio entre les dispositifs et la passerelle. Cette technique permet :

- D'analyser le trafic réseau pour identifier des vulnérabilités
- De capturer des paquets pour des attaques ultérieures (comme le rejeu)
- De diagnostiquer des problèmes de configuration

Méthodologie
------------

1. **Configuration matérielle** :
   - Utilisation d'un Arduino Dragino
   - Réglage de la fréquence LoRa (868 MHz en Europe)

2. **Capture des paquets** :
   - Interception des messages Join-Request et Data Up
   - Décodage des en-têtes LoRaWAN (MHDR, DevEUI, etc.)

3. **Analyse des trames** :
   - Conversion little-endian/big-endian
   - Vérification des MIC (Message Integrity Code)

Exemple de paquets capturés
----------------------------

Join-Request typique :

.. code-block:: none

   00 00 00 00 00 00 00 00 00 57 2A 71 99 49 D5 B3 70 DD 7C 93 36 E4 C9

- **MHDR (0x00)** : Join-Request
- **AppEUI** : 00 00 00 00 00 00 00 00 (valeur par défaut)
- **DevEUI** : 70 B3 D5 49 99 71 2A 57 (après conversion big-endian)
- **DevNonce** : DD 7C
- **MIC** : 93 36 E4 C9

Trames Data Up :

.. code-block:: none

   40 E2 F1 54 00 00 00 00 02 6F BD 26 07 55 5E 51 5A BA 78 C1 AE E8 76 D0 23 15 FA
   40 E2 F1 54 00 00 03 00 02 86 4F A9 79 3E C1 42 97 4E 06 F4 F4 1E E2 75 BC 79 BD 

- **MHDR (0x40)** : Unconfirmed Data Up
- **FCnt** : 00 00 puis 03 00 (incrémentation visible)

Outils nécessaires
-------------------

- **Matériel** :
  - Arduino Dragino
  - Antenne LoRa compatible 868MHz

- **Logiciels** :
  - Bibliothèque `arduino-LoRa <https://github.com/sandeepmistry/arduino-LoRa>`_
  - Minicom pour l'analyse des logs

Déploiement
-----------

Installation du sniffer
~~~~~~~~~~~~~~~~~~~~~~~
1. Flasher le code sur l'Arduino :

   .. code-block:: bash

      arduino --upload attaques/attaque_rejeu/replay_arduino/arduino_sniffer/arduino_sniffer.ino --port /dev/ttyACM1

2. Visualisation des paquets avec Minicom :

   .. code-block:: bash

      minicom -D /dev/ttyACM1 -b 9600

Automatisation avec le script sniffer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Le script ``sniffer.sh`` permet d'automatiser la capture :

.. code-block:: bash

   ./attaques/attaque_rejeu/replay_arduino/arduino_sniffer/sniffer.sh \
     -p /dev/ttyACM1 \
     -b 9600 \
     -o captures.txt

Options disponibles :

- ``-p`` : Port série (par défaut /dev/ttyACM1)
- ``-b`` : Baud rate (par défaut 9600)
- ``-o`` : Fichier de sortie

Analyse avancée
---------------

Pour interpréter les captures :

1. **Identifier le type de message** via le MHDR :
   - ``0x00`` : Join-Request
   - ``0x40`` : Unconfirmed Data Up
   - ``0x80`` : Confirmed Data Up

2. **Extraire les identifiants** :
   - DevEUI (octets 9-16 en little-endian)
   - AppEUI (octets 1-8)

3. **Vérifier l'intégrité** :
   - Les 4 derniers octets représentent le MIC
   - Doivent correspondre au calcul AES-CMAC avec la NwkSKey

Contre-mesures
--------------

- **Activer le chiffrement** (AES-128) pour empêcher la lecture des payloads
- **Utiliser des MIC robustes** et vérifier systématiquement leur validité

Limites
-------

- **Portée limitée** : Nécessité d'être à proximité physique du réseau
- **Dépendance matérielle** : Sensibilité du récepteur
- **Interprétation partielle** : Sans accès aux clés, certains champs restent illisibles (écoute possible mais incompréhensible si réseau bien configuré)

---

Attaque par rejeu
*****************

Contexte
--------

Dans un réseau LoRaWAN vulnérable, l'attaque par rejeu (*replay attack*) exploite la retransmission de paquets légitimes capturés pour :

- Perturber le réseau en saturant la passerelle.
- Falsifier des données (exemple : fausses mesures de capteurs).
- Contourner les mécanismes d'authentification si les compteurs de trames (FCnt) ou les MIC ne sont pas vérifiés.

Cette attaque est particulièrement efficace si :

- Le réseau n'utilise pas de compteurs de trames incrémentiels.
- Les MIC ne sont pas recalculés après capture.

Méthodologie de l'attaque
-------------------------

1. **Capture de paquets** :
   - Utilisation d'un sniffer (exemple : LoRattack avec USRP) ou d'un Arduino Dragino avec l'outil de sniffing défini dans la section Sniffing de cette documentation.
   - Filtrage des paquets *Unconfirmed Data Up* (MHDR = `0x40`).

2. **Analyse des trames** :
   - Extraction du **DevEUI**, **FCnt**, et **MIC**.
   - Conversion des formats (little-endian/big-endian).

3. **Rejeu automatisé** :
   - Réinjection des paquets capturés avec modification du FCnt.
   - Optionnel : Recalcul du MIC si la NwkSKey est connue (rare en pratique).

Exemple de paquet capturé
-------------------------

.. code-block:: none

   40 E2 F1 54 00 00 05 00 02 BF AE FF F4 7D 78 9A A3 0E 61 44 A7 39 90 93 9E 25 E2

- **MHDR (0x40)** : *Unconfirmed Data Up*.
- **FCnt** : `05 00` (valeur incrémentielle).
- **MIC** : `93 9E 25 E2` (vérifié par la passerelle).

Outils nécessaires
------------------

- **Matériel** :
  - Carte Arduino Dragino de préférence ou USRP (pour LoRattack).
- **Logiciels** :
  - `LoRattack <https://github.com/konicst1/lorattack>`_ (sniffing/rejeu).
  - Bibliothèque `arduino-LoRa <https://github.com/sandeepmistry/arduino-LoRa>`_.

Déploiement
-----------

Avec LoRattack (USRP)
~~~~~~~~~~~~~~~~~~~~~
1. Installer les dépendances :

   .. code-block:: bash

      sudo apt install gnuradio bittwist uhd-host
      git clone https://github.com/konicst1/lorattack.git
      cd lorattack && ./run.sh

2. Capturer et rejouer les paquets :

   .. code-block:: bash

      # Capture
      Lancer ./run.sh et sélectionner le sniffing.
      # Rejeu
      Lancer ./run.sh et sélectionner le replay à partir d'un fichier pcap obtenu dans l'étape précédente.

Avec Arduino Dragino (de manière manuelle)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. Flasher le code de rejeu en veillant à modifier le paquet à rejouer dans le code source :

   .. code-block:: bash

      arduino --upload attaques/attaque_rejeu/replay_arduino/arduino_player/arduino_player.ino --port /dev/ttyACM1

2. Analyser les logs via minicom :

   .. code-block:: bash

      minicom -D /dev/ttyACM1 -b 9600

Avec Arduino Dragino (de manière automatisée)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. Flasher le code de rejeu automatisé :

   .. code-block:: bash

      arduino --upload attaques/attaque_rejeu/replay_arduino/arduino_total_replay/arduino_total_replay.ino --port /dev/ttyACM1

2. Analyser les logs via minicom :

   .. code-block:: bash

      minicom -D /dev/ttyACM1 -b 9600

Contre-mesures
--------------

- **Validation stricte du FCnt** : Rejeter les paquets avec un compteur inférieur ou égal à la dernière valeur enregistrée.
- **Rotation des clés de session** : Limiter la durée de vie des NwkSKey/AppSKey, en renouvelant les sessions régulièrement.
- **Chiffrement de bout en bout** : Empêcher la lecture/modification des payloads.

Limites
-------

- **Efficacité réduite** : Si le réseau vérifie les MIC et FCnt, les paquets rejoués sont ignorés.
- **Portée limitée** : Nécessite une proximité physique avec le réseau cible.
- **Complexité** : Recalculer le MIC sans connaître la NwkSKey est impossible.

Exemple pratique
----------------

Un paquet rejoué avec succès (FCnt incrémenté) :

.. code-block:: none

   [ORIGINAL]  40...05 00...93 9E 25 E2
   [REPLAYED]  40...06 00...A1 B2 C3 D4  # MIC invalide, mais FCnt mis à jour

Ce paquet sera visible dans les logs du sniffer, mais rejeté par ChirpStack sans MIC valide.

---

Attaque de brouillage
*********************

Contexte
--------

Le brouillage radio (jamming) est une forme d’attaque par déni de service (DoS) qui vise à perturber les communications sans intercepter les données. Elle consiste à inonder un canal radio avec des signaux parasites pour empêcher les nœuds LoRaWAN de transmettre ou de recevoir correctement.

Il existe plusieurs types de brouillage :

- **Brouillage continu (constant jamming)** : envoi constant de signaux pour occuper le canal.

- **Brouillage réactif (reactive jamming)** : envoi d’un signal dès qu’un paquet est détecté.

- **Brouillage aléatoire (random jamming)** : émission de signaux à intervalles irréguliers.

- **Brouillage ciblé (trigger ou selective jamming)** : attaque déclenchée à la détection d’un certain type de trame ou contenu.

Dans cette documentation, nous allons nous concentrer sur le brouillage de type “deny”, c’est-à-dire une attaque simple et continue qui vise à saturer le canal radio LoRaWAN pour empêcher toute autre communication légitime.

Méthodologie de l'attaque
-------------------------

L'attaque consiste à utiliser un nœud LoRa pour transmettre en boucle un message répétitif, sans respecter les intervalles habituels entre deux transmissions. Le message contient simplement une chaîne de caractères (par exemple "JammingJamming...") répétée, qui n’a aucune signification fonctionnelle, mais occupe le temps d’antenne radio.

Le nœud utilise la même configuration que les dispositifs du réseau cible :

- **Fréquence** : 868,3 MHz

- **Spreading Factor** : SF7

- **Bande passante** : 125 kHz

- **Coding rate** : 4/5

Grâce à cette configuration, l’attaque peut interférer efficacement avec la passerelle et bloquer les communications entrantes des vrais capteurs.

Déploiement
-----------

Matériel utilisé :
~~~~~~~~~~~~~~~~~~


- **LoPy4** (nœud légitime)

- **Arduino Dragino** (nœud de brouillage)

- **Passerelle LoRaWAN** configurée sur la fréquence 868,3 MHz

Étapes :
~~~~~~~~


1.  Mise en place du nœud légitime (LoPy4) :

- Ouvrir Pymakr ou VSCode avec le plugin Pycom.

- Charger le script de transmission qui se trouve dans : ``reproduction-attaques-lorawan/noeud_pycom/message_pycom.py``   vers la passerelle.

- Lancer le code et observer la réception dans l'interface ChirpStack

Une fois le fonctionnement normal confirmé (messages visibles sur ChirpStack), on initialise l’attaque.

2. Mise en place du nœud brouilleur (Arduino Dragino) :
- Ouvrir le fichier suivant dans l’IDE Arduino : ``reproduction-attaques-lorawan/attaques/brouillage/jamming_deny/jamming_deny.ino``

- S’assurer que les paramètres LoRa sont identiques à ceux du LoPy4 :

 .. code-block:: bash

      LoRa.begin(868.3E6);
      LoRa.setSpreadingFactor(7);
      LoRa.setSignalBandwidth(125E3);

- Connecter l’Arduino et téléverser le code

Le code de brouillage est flashé sur l’Arduino Dragino. Ce dernier transmet en boucle un message répétitif (par exemple "JammingJamming...") sur la même fréquence et avec les mêmes paramètres LoRa (SF7, BW 125 kHz).

3.  Observation des effets de l’attaque :

Dès l’activation du brouillage, on observe une interruption de la réception des messages du LoPy4 par la passerelle.
Cette coupure confirme que le canal est saturé par le nœud attaquant et que l’attaque de type deny est efficace.

L’envoi peut être vérifié via le moniteur série de l’IDE Arduino, où un message de confirmation s’affiche après chaque transmission.

 .. code-block:: bash

      JAM_SUCCES;
   
   

Contre-mesures et recommandations
---------------------------------

- Activer la détection d’interférences au niveau de la passerelle, si disponible.

- Surveiller le taux de perte de paquets pour détecter une activité anormale.

- Utiliser le frequency hopping (saut de fréquence) pour réduire l’impact du brouillage.

- Mettre en place des mécanismes de priorité ou de répétition adaptative dans les capteurs.

Limites
-------
- Portée physique réduite : L’attaquant doit être proche de la passerelle ou des nœuds pour être efficace.

- Consommation énergétique élevée : L’attaque nécessite une émission continue, ce qui peut vider rapidement la batterie du dispositif malveillant.

- Détection possible : Une activité radio anormale peut être repérée avec des outils de monitoring RF.