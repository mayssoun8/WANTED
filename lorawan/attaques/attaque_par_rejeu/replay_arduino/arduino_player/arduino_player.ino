#include <SPI.h>
#include <LoRa.h>

// Paquet à rejouer (19 octets pour un join_request)
//uint8_t packet[] = {
//  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  // AppEUI
//  0x57, 0x2A, 0x71, 0x99, 0x49, 0xD5, 0xB3, 0x70,  // DevEUI
//  0xDD, 0x7C                                        // DevNonce
//};

// paquet data up 40 9F 95 92 00 00 04 00 02 E2 88 E4 98 1C A3 8E DE 71 45 E1 27 F3 EC B0 C2 08 DA
uint8_t packet[] = {
  0x40, 0x9F, 0x95, 0x92, 0x00, 0x00, 0x04, 0x00, 0x02,
  0xE2, 0x88, 0xE4, 0x98, 0x1C, 0xA3, 0x8E, 0xDE, 0x71,
  0x45, 0xE1, 0x27, 0xF3, 0xEC, 0xB0, 0xC2, 0x08, 0xDA
};

int packetSize = sizeof(packet);

void setup() {
  Serial.begin(9600);
  while (!Serial);

  Serial.println("LoRa Replayer");

  if (!LoRa.begin(868.3E6)) {  // Fréquence 868,3 MHz
    Serial.println("Erreur lors de l'initialisation de LoRa !");
    while (1);
  }

  // Configurer le spreading factor et la bande passante
  LoRa.setSpreadingFactor(7);  // SF7
  LoRa.setSignalBandwidth(125E3);  // 125 kHz
  LoRa.setCodingRate4(5);  // Coding Rate 4/5

  Serial.println("Prêt à rejouer le paquet en boucle...");
}

void loop() {
  Serial.println("Envoi du paquet...");

  // Incrémenter le compteur de trames (FCnt)
  packet[6]++;  // Incrémente l'octet de poids faible
  if (packet[6] == 0) {
    packet[7]++;  // Incrémente l'octet de poids fort si nécessaire
  }

  // Envoyer le paquet
  LoRa.beginPacket();
  LoRa.write(packet, packetSize);
  LoRa.endPacket();

  delay(4000);  // Attendre 4 secondes avant de renvoyer le paquet
}