#  JAMMING

## Utilisation du LoFrasea et jamming_trigger

### jamming_trigger

### Problème rencontré :
- Nous avons observé via **Minicom** que des signaux de jamming sont envoyés correctement, donc les messages détectés. Cependant, en consultant **Chirpstack**, nous remarquons que les messages légitimes ne sont pas toujours émis sur la même fréquence. Parfois, ils sont émis sur des fréquences telles que **867.9 MHz** ou **868.5 MHz**, de manière aléatoire. Ce phénomène est généralement conçu pour améliorer la robustesse au bruit dans les communications LoRaWAN.

### Fréquences observées :
Les fréquences d'émission détectées sont les suivantes :

- 867.1 MHz
- 867.3 MHz
- 867.7 MHz
- 867.9 MHz
- 867.5 MHz
- 868.1 MHz
- 868.3 MHz
- 868.5 MHz

Remarque : 

Après recherche, il se trouve que les canaux par défaut imposés par LoRaWAN sont uniquement ceux en 868.x MHz, les  autres, sont eux ajoutés par le réseau via CFList.

### Impact sur le jamming :
Cette variation des fréquences complique le processus de jamming, car il est nécessaire de couvrir un large éventail de fréquences pour maximiser l'efficacité de l'attaque. Actuellement, nous ne parvenons pas à faire en sorte d'altérer les communications légitimes.


### jamming_deny

Nous observons que le jamming_deny, qui lui brouille en permanence, et non pas uniquement lorsqu'un message légitime est détecté fonctionne un peu mieux, même si ce dernier ne parvient toujours pas à brouiller totalement le signal, nous observons tout de même des retards dans la réception des messages.