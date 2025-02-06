#include <AdcCorrection.h>
#include <BufferFloat.h>
#include <DoubleBufferFloat.h>
#include <EmotiBit.h>
#include <EmotiBitConfigManager.h>
#include <EmotiBitEda.h>
#include <EmotiBitLedController.h>
#include <EmotiBitNvmController.h>
#include <EmotiBitVersionController.h>
#include <EmotiBitWiFi.h>
#include <FileTransferManager.h>

#include <WiFi.h>
#include <NTPClient.h>
#include <WiFiUdp.h>
#include "EmotiBit.h"
#include <FirebaseESP32.h>
#include <TimeLib.h>

#define SerialUSB SERIAL_PORT_USBVIRTUAL // Required to work in Visual Micro / Visual Studio IDE
const uint32_t SERIAL_BAUD = 9600;     //115200

// Arduino Low Power: Version=1.2.2
// Arduino_Json by Arduino: Version=0.2.0
// NTPClient: Version=3.2.1
// Adafruit BusIO: Version=1.16.2
// Adafruit GFX Library: Version=1.11.11
// Adafruit IS31FL3731 Library: Version=2.0.2
// AdafruitSSD1306: Version=2.5.13
// Adafruit Unified Sensor: Version=1.1.14
// ArduinoJson by Benoit Blanchon: Version=7.2.1
// AsynceTCP: Version=1.1.4
// EmotiBit ADS1X15: Version=2.2.0+EmotiBit0.0.1
// EmotiBit ArdionoFilters: Version=1.0.0
// EmotiBit BMI160: Version=0.3.3
// EmotiBit Emojib: Version= 0.0.1
// EmotiBit External EEPROM: Version=1.0.5+EmotiBit.0.0.1
// EmotiBit FeatherWing: Version=1.12.1
// EmotiBit MAX30101: Version=2.0.3
// EmotiBit NCP5623: Version=0.1.0
// EmotiBit SI7013: Version=0.0.7
// EmotiBit SimpleFTPServer: Version=2.17+EmotiBit.0.0.1
// EmotiBit XPlat Utils: Version=1.6.0
// Firebase ESP32 Client: Version=4.4.14
// SdFat by Bill Greiman: Version=2.2.0
// Time by Michael Margolis: Version=1.6.1

EmotiBit emotibit;

const size_t numSamplesPPG = 100;
const size_t numSamplesEDA = 15;
const size_t numSamplesTemp = 8;

float dataPPG[numSamplesPPG];
float dataEDA[numSamplesEDA];
float dataTemp[numSamplesTemp];

size_t countPPG = 0;
size_t countEDA = 0;
size_t countTemp = 0;

float averagePPG = 0;
float averageEDA = 0;
float averageTemp = 0;

unsigned long lastTime_1s = 0;
const unsigned long interval_1s = 1000; // 1 second
unsigned long lastTime_1min = 0; // ตัวแปรเก็บเวลา 1 นาที
const unsigned long interval_1min = 60000; // 1 นาที (60,000 ms)
unsigned long lastTime_5min = 0; // ตัวแปรเก็บเวลา 5 นาที
const unsigned long interval_5min = 300000; // 5 นาที (300,000 ms)

const char* ssid = "3BB_4207_2.4GHz";
const char* password = "410093283";

WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org", 0, 60000);

FirebaseData firebaseData;
FirebaseConfig config;
FirebaseAuth auth;

const char* FIREBASE_HOST = "https://inewgenweb-default-rtdb.asia-southeast1.firebasedatabase.app/";
const char* FIREBASE_AUTH = "euw2n2EBYABgGk9S0K7oT95nKrswcpN6Txs3Ghor";

// Function prototypes
void connectToWiFi();
void connectToFirebase();
void readSensorData();
void sendToFirebase();

void setup() {
  Serial.begin(SERIAL_BAUD);
  Serial.println("Starting setup...");

  connectToWiFi();

  config.database_url = FIREBASE_HOST;
  config.signer.tokens.legacy_token = FIREBASE_AUTH;
  Firebase.begin(&config, &auth);
  connectToFirebase();

  String inoFilename = __FILE__;
  inoFilename.replace("/", "\\");
  if (inoFilename.lastIndexOf("\\") != -1) {
    inoFilename = inoFilename.substring((inoFilename.lastIndexOf("\\")) + 1, (inoFilename.indexOf(".")));
  }
  emotibit.setup(inoFilename);
}

void loop() {
  timeClient.update();
  setTime(timeClient.getEpochTime());
  emotibit.update();

  readSensorData();

  unsigned long currentTime = millis();

  // ส่งข้อมูลทุก 1 วินาที
  if (currentTime - lastTime_1s >= interval_1s) {
    lastTime_1s = currentTime;
    sendToFirebase("1s");
  }

  // ส่งข้อมูลทุก 1 นาที
  if (currentTime - lastTime_1min >= interval_1min) {
    lastTime_1min = currentTime;
    sendToFirebase("1min");
  }

  // ส่งข้อมูลทุก 5 นาที
  if (currentTime - lastTime_5min >= interval_5min) {
    lastTime_5min = currentTime;
    sendToFirebase("5min");
  }
}

void readSensorData() {
  size_t dataAvailablePPG = emotibit.readData(EmotiBit::DataType::PPG_GREEN, &dataPPG[countPPG], numSamplesPPG - countPPG);
  countPPG += dataAvailablePPG;
  if (countPPG >= numSamplesPPG) {
    float sumPPG = 0;
    for (size_t i = 0; i < numSamplesPPG; i++) {
      sumPPG += dataPPG[i];
    }
    averagePPG = sumPPG / numSamplesPPG;
    countPPG = 0;
  }

  size_t dataAvailableEDA = emotibit.readData(EmotiBit::DataType::EDA, &dataEDA[countEDA], numSamplesEDA - countEDA);
  countEDA += dataAvailableEDA;
  if (countEDA >= numSamplesEDA) {
    float sumEDA = 0;
    for (size_t i = 0; i < numSamplesEDA; i++) {
      sumEDA += dataEDA[i];
    }
    averageEDA = sumEDA / numSamplesEDA;
    countEDA = 0;
  }

  size_t dataAvailableTemp = emotibit.readData(EmotiBit::DataType::THERMOPILE, &dataTemp[countTemp], numSamplesTemp - countTemp);
  countTemp += dataAvailableTemp;
  if (countTemp >= numSamplesTemp) {
    float sumTemp = 0;
    for (size_t i = 0; i < numSamplesTemp; i++) {
      sumTemp += dataTemp[i];
    }
    averageTemp = sumTemp / numSamplesTemp;
    countTemp = 0;
  }
}

void sendToFirebase(const String& intervalType) {
  if (Firebase.ready()) {
    FirebaseJson json;
    json.set("EDA", averageEDA);
    json.set("PPG", averagePPG);
    json.set("ST", averageTemp);

    String path = "Device/Inpatient/MD-V5-0000804/" + intervalType + "/"; // เพิ่มช่วงเวลาใน path
    if (Firebase.setJSON(firebaseData, path, json)) {
      Serial.println("Data sent successfully to: " + path);
    } else {
      Serial.println("Failed to send data: " + firebaseData.errorReason());
    }
  } else {
    Serial.println("Firebase not ready, retrying...");
    Firebase.begin(&config, &auth);
  }
}

void connectToWiFi() {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}

void connectToFirebase() {
  while (!Firebase.ready()) {
    Serial.println("Waiting for Firebase to be ready...");
    delay(1000);
  }
  Serial.println("Firebase is ready!");
}

String getTimestamp() {
  return String(year()) + "_" + String(month()) + "_" + String(day()) + "_" + String(hour()) + "_" + String(minute()) + "_" + String(second());
}
