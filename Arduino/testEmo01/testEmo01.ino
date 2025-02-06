#include <WiFi.h>
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include <NTPClient.h>
#include <WiFiUdp.h>
#include <TimeLib.h>
#include "EmotiBit.h"

// WiFi credentials
const char* ssid = "IICE-WiFI";
const char* password = "admin@123";

// Wifi หอ
// {"WifiCredentials": [{"ssid": "3BB_4207_2.4GHz", "password" : "410093283"}]}

// {"WifiCredentials": [{"ssid": "{"WifiCredentials": [{"ssid": "IICE-WiFI", "password" : "admin@123"}]}", "password" : "admin@123"}]}

// Create a server and websocket object
AsyncWebServer server(80);
AsyncWebSocket ws("/ws");

WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org", 0, 60000);

EmotiBit emotibit;

// Sensor data buffers and variables
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
const unsigned long interval_1s = 1000;

void connectToWiFi() {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // test
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(200, "text/html",
      "<!DOCTYPE html>"
      "<html lang='en'>"
      "<head>"
      "<meta charset='UTF-8'>"
      "<meta name='viewport' content='width=device-width, initial-scale=1.0'>"
      "<title>ESP32 Data Monitor</title>"
      "<style>"
      "body { font-family: Arial, sans-serif; text-align: center; padding: 20px; }"
      "h1 { color: #333; }"
      ".data-box { margin: 20px auto; padding: 10px; border: 1px solid #ddd; border-radius: 5px; display: inline-block; }"
      ".data-box p { margin: 5px 0; font-size: 18px; }"
      "</style>"
      "</head>"
      "<body>"
      "<h1>ESP32 Data Monitor</h1>"
      "<div class='data-box'>"
      "<p><strong>PPG:</strong> <span id='ppg'>0</span></p>"
      "<p><strong>EDA:</strong> <span id='eda'>0</span></p>"
      "<p><strong>Temp:</strong> <span id='temp'>0</span></p>"
      "</div>"
      "<script>"
      "const eventSource = new EventSource('/data');" // ใช้ Server-Sent Events (SSE) หรือเปลี่ยนเป็น WebSocket
      "eventSource.onmessage = function(event) {"
      "  const data = JSON.parse(event.data);"
      "  document.getElementById('ppg').textContent = data.PPG || 0;"
      "  document.getElementById('eda').textContent = data.EDA || 0;"
      "  document.getElementById('temp').textContent = data.Temp || 0;"
      "};"
      "</script>"
      "</body>"
      "</html>");
  // "<div class='tenor-gif-embed' data-postid='12805916815008299407' data-share-method='host' data-aspect-ratio='1' data-width='100%'><a href='https://tenor.com/view/oia-uia-oia-cat-uia-cat-catcultclassics-gif-12805916815008299407'>Oia Uia Sticker</a>from <a href='https://tenor.com/search/oia-stickers'>Oia Stickers</a></div> <script type='text/javascript' async src='https://tenor.com/embed.js'></script>"
  });
  Serial.println("HTML OK!");
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

// Function to send data to WebSocket clients
void sendToWebSocket() {
  // DynamicJsonDocument json(256);
  // JsonDocument jsonDoc(256);
  // StaticJsonDocument jsonDoc(256);  // ใช้ไดนามิกหากขนาดข้อมูลเปลี่ยนแปลงได้
  // ใช้ StaticJsonDocument แทน DynamicJsonDocument
  StaticJsonDocument<256> jsonDoc;

  // เพิ่มข้อมูลลงใน JSON Document
  // json["PPG"] = averagePPG;
  jsonDoc["PPG"] = averagePPG;  // ใช้ jsonDoc แทน json
  jsonDoc["EDA"] = averageEDA;
  jsonDoc["Temp"] = averageTemp;

  // แปลง JSON Document เป็น String
  String jsonString;
  serializeJson(jsonDoc, jsonString);

  // ส่งข้อมูลผ่าน WebSocket
  ws.textAll(jsonString);
}

void setupWebSocket() {
  ws.onEvent([](AsyncWebSocket *server, AsyncWebSocketClient *client, AwsEventType type, void *arg, uint8_t *data, size_t len) {
    if (type == WS_EVT_CONNECT) {
      Serial.println("WebSocket client connected");
    } else if (type == WS_EVT_DISCONNECT) {
      Serial.println("WebSocket client disconnected");
    }
  });
  server.addHandler(&ws);
}

void setup() {
  Serial.begin(9600);
  Serial.println("Starting setup...");

  connectToWiFi();

  timeClient.begin();
  setupWebSocket();

  server.begin();
  Serial.println("WebSocket server started");

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

  if (currentTime - lastTime_1s >= interval_1s) {
    lastTime_1s = currentTime;
    sendToWebSocket(); // Send data via WebSocket every second
  }

  ws.cleanupClients(); // Clean up disconnected clients
}
