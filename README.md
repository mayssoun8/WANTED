# Reproduction de Scénarios d'Attaques sur LoRaWAN

## Objectif
Ce projet a pour but de **reproduire et analyser une sélection de scénarios d'attaques** sur le protocole **LoRaWAN**, afin de mieux comprendre ses vulnérabilités et ses mécanismes de sécurité.

## Structure du projet

### 1. Réseau légitime
Avant d'effectuer les attaques, nous devons créer un **réseau légitime**, qui servira de base pour nos expérimentation.  

Les codes nécessaires à la configuration de ce réseau sont disponibles dans le répertoire :  
**[`noeud_pycom`](./noeud_pycom)**  

### 2. Attaques
Enfin, nous effectuerons une variété d'autres attaques comme du replay, du spoofing ou du jamming. 

Ces scénarios d'attaques sont disponibles dans le répertoire :  
**[`attaques`](./attaques)**

### 3. Outil de Craft de paquets
Un outil de craft de paquets est disponible à la racine de ce projet :  
**[`craft.py`](./craft.py)**

### 4. Application

Pour faciliter l'utilisation de ce projet et l'implémentation des diverses attaques, une application a été créée dans le répertoire **[`application`](./application)**, que l'on peut lancer en utilisant le fichier bash présent dans le répertoire.

## Documentation

Une documentation détaillée est disponible. Pour la générer :
1. Accédez au répertoire `docs`
2. Exécutez la commande :
   ```bash
   make html
   ```
Dans cette documentation sont détaillées les clés permettant de reproduire ce projet, mais également une idée de scénario d'attaque pouvant être implémentée dans le futur.

