#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_BME680.h"
#include <Adafruit_SI1145.h>

// Configuration du capteur BME680
#define BME_SCK 13
#define BME_MISO 12
#define BME_MOSI 8
#define BME_CS 7
#define SEALEVELPRESSURE_HPA (1013.25)
Adafruit_BME680 bme(BME_CS, BME_MOSI, BME_MISO, BME_SCK); // Mode SPI

// Configuration du capteur HC-SR04
#define Broche_Echo 10
#define Broche_Trigger 9

// Configuration du capteur MQ135
const int pinMQ135 = A0;
int valeurAirPropre = 0;
int seuilFumee = 0;

// Configuration du capteur SI1145
Adafruit_SI1145 si1145;

// Variables pour le timer non bloquant
unsigned long previousMillis = 0;
const long interval = 2000; // Intervalle de lecture : 2 secondes

void setup() {
  // Initialisation de la communication série avec l'XBee
  Serial.begin(9600);

  // Calibration du MQ135 en air propre
  Serial.println("Calibration du capteur MQ135...");
  for (int i = 0; i < 100; i++) {
    valeurAirPropre += analogRead(pinMQ135);
    delay(50);
  }
  valeurAirPropre /= 100;  // Moyenne des lectures
  seuilFumee = valeurAirPropre + 184; // Définition du seuil
  Serial.println("😡😡Valeur en air propre😡😡 : ");
  Serial.println(valeurAirPropre);
  Serial.println("😡😡Seuil de détection de fumée😡😡 : ");
  Serial.println(seuilFumee);

  // Initialisation du BME680
  if (!bme.begin()) {
    envoyerDonnees("Erreur: BME680 non détecté ! Vérifiez le câblage.");
    while (1);
  }
  bme.setTemperatureOversampling(BME680_OS_8X);
  bme.setHumidityOversampling(BME680_OS_2X);
  bme.setPressureOversampling(BME680_OS_4X);
  bme.setIIRFilterSize(BME680_FILTER_SIZE_3);
  bme.setGasHeater(320, 150);

  // Initialisation du HC-SR04
  pinMode(Broche_Trigger, OUTPUT);
  pinMode(Broche_Echo, INPUT);

  // Initialisation du SI1145
  if (!si1145.begin()) {
    envoyerDonnees("Erreur: SI1145 non détecté !");
    while (1);
  }

  envoyerDonnees("Initialisation terminée. Début des lectures...");
}

void loop() {
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    // Lecture du BME680
    if (!bme.performReading()) {
      envoyerDonnees("Erreur: Lecture BME680 échouée !");
    } else {
      envoyerDonnees("👾");
      envoyerDonnees("BME680 - Temperature: " + String(bme.temperature) + " *C");
      envoyerDonnees("BME680 - Pression: " + String(bme.pressure / 100.0) + " hPa");
      envoyerDonnees("BME680 - Humidité: " + String(bme.humidity) + " %");
    }

    // Lecture du HC-SR04
    long distance = lireDistance();
    envoyerDonnees("👾");
    envoyerDonnees("HC_SR04 - Distance: " + String(distance) + " cm");

    // Lecture du MQ135
    int valeurMQ135 = analogRead(pinMQ135);
    envoyerDonnees("👾");
    envoyerDonnees("MQ135 - Valeur lue: " + String(valeurMQ135));
    
    if (valeurMQ135 > seuilFumee) {
      envoyerDonnees("⚠️ Alerte : Présence de fumée détectée😡😡😡😡 !");
    } else {
      envoyerDonnees("😡😡Air normal");
    }

    // Lecture du SI1145
    float uv_index = si1145.readUV() / 100.0;
    uint16_t ir = si1145.readIR();
    uint16_t visible = si1145.readVisible();
    envoyerDonnees("👾");
    envoyerDonnees("SI1145 - UV: " + String(uv_index));
    envoyerDonnees("SI1145 - IR: " + String(ir));
    envoyerDonnees("SI1145 - Visible: " + String(visible));

    envoyerDonnees("Fin des lectures.");
    envoyerDonnees("Réactualisation dans 10 secondes");
  }
}

long lireDistance() {
  const int nombreLectures = 5;
  long sommeDistance = 0;

  for (int i = 0; i < nombreLectures; i++) {
    digitalWrite(Broche_Trigger, LOW);
    delayMicroseconds(2);
    digitalWrite(Broche_Trigger, HIGH);
    delayMicroseconds(10);
    digitalWrite(Broche_Trigger, LOW);
    long duree = pulseIn(Broche_Echo, HIGH);
    sommeDistance += duree * 0.034 / 2;
    delay(50);
  }
  return sommeDistance / nombreLectures;
}

void envoyerDonnees(String message) {
  Serial.println(message);
  delay(1500);
}
