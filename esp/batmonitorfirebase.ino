#include <WiFi.h>
#include "FirebaseESP32.h"

#define FIREBASE_HOST       "FIREBASEHOST"
#define FIREBASE_AUTH       "FIREBASEAUTH"
#define WIFI_SSID           "WIFISSID"
#define WIFI_PASSWORD       "WIFIPASSWORD"

#define PATH_SOCKET_1       "pathToControl/pathToControl/pathToControl/socket_1"
#define PIN_ON              HIGH
#define PIN_OFF             LOW
#define PIN_FIREBASE_ON     1
#define PIN_FIREBASE_OFF    0
#define updateFirebase      300
#define PIN_SOCKET_1        16

FirebaseData firebaseData;

void setupPins() {
  pinMode(PIN_SOCKET_1, OUTPUT);
  digitalWrite(PIN_SOCKET_1, PIN_OFF);
}

void setupWifi() {
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.print(".");
    delay(300);
  }
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());
  Serial.println();
}

void setupFirebase() {
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
  Firebase.reconnectWiFi(true);
}

void getInt(String path, int pin, String messageOn, String messageOff) {
  if (Firebase.getInt(firebaseData, path)) {
    if (firebaseData.intData() == PIN_FIREBASE_ON) {
      digitalWrite(pin, PIN_ON);
      Serial.println(messageOn);
    } else if (firebaseData.intData() == PIN_FIREBASE_OFF) {
      digitalWrite(pin, PIN_OFF);
      Serial.println(messageOff);
    }
  } else  {
    Serial.println("FAILED");
    Serial.println("REASON: " + firebaseData.errorReason());
    Serial.println("PATH: " + path);
    Serial.println("------------------------------------");
    Serial.println();
  }

  delay(updateFirebase);
}

void blink() 
{
  digitalWrite(PIN_SOCKET_1, PIN_ON);
  delay(1000);
  digitalWrite(PIN_SOCKET_1, PIN_OFF);
  delay(1000);
}

void setup() {
  Serial.begin(115200);

  setupPins();

  setupWifi();

  setupFirebase();
}

void loop() {
  getInt(PATH_SOCKET_1, PIN_SOCKET_1, "Socket_1 on", "Socket_1 off");
  
  //blink();
}
