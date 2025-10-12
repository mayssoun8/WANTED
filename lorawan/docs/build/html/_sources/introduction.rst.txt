Introduction
============

Objectif du projet
******************

Ce projet a pour but d’expérimenter différentes attaques sur un réseau LoRaWAN, notamment :

- **Sniffing** : interception des paquets LoRaWAN transmis sur le réseau.
- **Brouillage** : perturbation du signal pour empêcher la communication.
- **Rejeu de paquets** : retransmission de paquets interceptés pour tromper le réseau.
- **Usurpation d’identité** : imitation d’un nœud légitime pour envoyer des données falsifiées.

Ce document décrit la mise en place de ces attaques ainsi que leur reproduction dans le cadre du projet.

Infrastructure LoRaWAN
======================

Matériel utilisé
****************

- **Passerelle LoRaWAN** fournie par l’encadrant, incluant :
  
  - Raspberry Pi 3 Model B
  - Module concentrateur LoRa IC880A

- **Serveur réseau ChirpStack** préconfiguré sur la passerelle.

Logiciel utilisé
****************

ChirpStack
----------

ChirpStack est utilisé comme serveur réseau LoRaWAN. Pour accéder à son interface web et configurer l’application :

1. Se connecter au réseau WiFi de la passerelle.
2. Ouvrir un navigateur et entrer l’URL : `http://192.168.0.1:8080/`.

Noeud légitime
==============

Matériel utilisé
****************

- **LoPy4 Pycom**

Logiciel utilisé
****************

Pymakr via VS Code
------------------

Mise en place :

1. Installer l’extension **Pymakr** sur **VS Code**.
2. Brancher le **LoPy4 Pycom** au PC via USB.
3. Synchroniser le LoPy4 avec le projet.
4. Flasher le code souhaité :

   - Sélectionner **"Upload on device"**.
   - Exécuter le script avec **"Run on device"** dans l’onglet Pymakr.

Code utilisé
------------

Les scripts sont disponibles dans le répertoire **`noeud_pycom`** du dépôt Git.

- **Fichier principal** : `simulation_capteur_humidité.py`
  
  - Ce fichier simule un capteur d’humidité.
  - Les clés cryptographiques peuvent être modifiées directement dans le code.

Noeud attaquant
===============

Matériel utilisé
****************

- **Arduino Dragino**

Logiciel utilisé
****************

Arduino IDE
-----------

Ou directement via un terminal Linux.

Bibliothèques utilisées
-----------------------

Pour ce projet, nous utilisons plusieurs bibliothèques Arduino compatibles avec LoRaWAN :

- **LoRa** de **Sandeep Mistry** (v0.8.0)
- **MCCI LoRaWAN LMIC** de **Terry Moore** (v5.0.1)
- **RadioLib** de **Jan Gromes** (v7.1.2)
