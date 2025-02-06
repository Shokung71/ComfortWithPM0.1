// Include necessary libraries
#include <WiFi.h>
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include <ArduinoJson.h>
#include "EmotiBit.h"

// WiFi credentials
const char* ssid = "IICE-WiFI";
const char* password = "admin@123";

// Create a server and websocket object
AsyncWebServer server(80);
AsyncWebSocket ws("/ws");

// EmotiBit object
EmotiBit emotibit;

// Sensor data variables
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
}

void readSensorData() {
  // Simulate reading sensor data for now
  averagePPG = random(50, 100);   // Example data
  averageEDA = random(10, 50);   // Example data
  averageTemp = random(20, 30);  // Example data

  Serial.print("PPG: "); Serial.println(averagePPG);
  Serial.print("EDA: "); Serial.println(averageEDA);
  Serial.print("Temp: "); Serial.println(averageTemp);
}

// Function to send data to WebSocket clients
void sendToWebSocket() {
  StaticJsonDocument<256> jsonDoc;
  // JsonDocument jsonDoc(256);

  jsonDoc["PPG"] = averagePPG;
  jsonDoc["EDA"] = averageEDA;
  jsonDoc["Temp"] = averageTemp;

  String jsonString;
  serializeJson(jsonDoc, jsonString);

  // Send JSON data to all connected WebSocket clients
  ws.textAll(jsonString);
  Serial.println(jsonString);  // Debugging output
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
  connectToWiFi();

  setupWebSocket();

  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request) {
    request->send(200, "text/html",
      "<!DOCTYPE html>"
      "<html>"
      "<head><title>ESP32 Data Monitor</title></head>"
      "<body>"
      "<h1>ESP32 Data Monitor</h1>"
      "<div>"
      "<p><strong>PPG:</strong> <span id='ppg'>0</span></p>"
      "<p><strong>EDA:</strong> <span id='eda'>0</span></p>"
      "<p><strong>Temp:</strong> <span id='temp'>0</span></p>"
      "</div>"
      "<script>"
      "const ws = new WebSocket('ws://' + location.host + '/ws');"
      "ws.onmessage = function(event) {"
      "  const data = JSON.parse(event.data);"
      "  document.getElementById('ppg').textContent = data.PPG || 0;"
      "  document.getElementById('eda').textContent = data.EDA || 0;"
      "  document.getElementById('temp').textContent = data.Temp || 0;"
      "};"
      "</script>"
      "</body>"
      "</html>");
  });

  server.begin();
  Serial.println("Server started");

  // Try setting up EmotiBit and bypass SD-Card dependency
    if (!emotibit.setup("testEmo02")) {
    Serial.println("Warning: EmotiBit setup failed. Bypassing SD-Card requirements.");
  } else {
    Serial.println("EmotiBit setup successful");
  }
  // emotibit.setup("testEmo02");
}


void loop() {
  unsigned long currentTime = millis();

  // Update sensor data
  readSensorData();

  // Send data to WebSocket every second
  if (currentTime - lastTime_1s >= interval_1s) {
    lastTime_1s = currentTime;
    sendToWebSocket();
  }

  // Clean up WebSocket clients
  ws.cleanupClients();
}

