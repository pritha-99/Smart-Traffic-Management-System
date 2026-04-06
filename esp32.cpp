\documentclass{article}
\usepackage{listings}
\usepackage{xcolor}

\lstset{
  language=C++,
  basicstyle=\ttfamily\small,
  keywordstyle=\color{blue},
  stringstyle=\color{red},
  commentstyle=\color{green!50!black},
  numbers=left,
  numberstyle=\tiny,
  stepnumber=1,
  numbersep=5pt,
  breaklines=true,
  frame=single,
  tabsize=2
}

\begin{document}

\section*{ESP32 MQTT Traffic Control Code}

\begin{lstlisting}
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <PubSubClient.h>

const char* ssid = WIFI_SSID;
const char* password = WIFI_PASSWORD;

const char* mqtt_server = MQTT_SERVER;
const int mqtt_port = 8883;
const char* mqtt_user = MQTT_USERNAME;
const char* mqtt_pass = MQTT_PASSWORD;

WiFiClientSecure espClient;
PubSubClient client(espClient);

int lane1_sensor_pin = 14;
int lane2_sensor_pin = 22;
int lane3_sensor_pin = 23;

int L1_R = 27, L1_Y = 25, L1_G = 26;
int L2_R = 18, L2_Y = 19, L2_G = 21;
int L3_R = 32, L3_Y = 33, L3_G = 15;

void callback(char* topic, byte* payload, unsigned int length) {
  String msg = "";

  for (int i = 0; i < length; i++) {
    msg += (char)payload[i];
  }

  Serial.println("Received: " + msg);

  digitalWrite(L1_R, LOW); digitalWrite(L1_Y, LOW); digitalWrite(L1_G, LOW);
  digitalWrite(L2_R, LOW); digitalWrite(L2_Y, LOW); digitalWrite(L2_G, LOW);
  digitalWrite(L3_R, LOW); digitalWrite(L3_Y, LOW); digitalWrite(L3_G, LOW);

  if (msg.indexOf("lane1:GREEN") >= 0) digitalWrite(L1_G, HIGH);
  if (msg.indexOf("lane1:YELLOW") >= 0) digitalWrite(L1_Y, HIGH);
  if (msg.indexOf("lane1:RED") >= 0) digitalWrite(L1_R, HIGH);

  if (msg.indexOf("lane2:GREEN") >= 0) digitalWrite(L2_G, HIGH);
  if (msg.indexOf("lane2:YELLOW") >= 0) digitalWrite(L2_Y, HIGH);
  if (msg.indexOf("lane2:RED") >= 0) digitalWrite(L2_R, HIGH);

  if (msg.indexOf("lane3:GREEN") >= 0) digitalWrite(L3_G, HIGH);
  if (msg.indexOf("lane3:YELLOW") >= 0) digitalWrite(L3_Y, HIGH);
  if (msg.indexOf("lane3:RED") >= 0) digitalWrite(L3_R, HIGH);
}

void reconnect() {
  while (!client.connected()) {
    if (client.connect("ESP32_Client", mqtt_user, mqtt_pass)) {
      client.subscribe("traffic/command");
    } else {
      delay(2000);
    }
  }
}

void setup() {
  Serial.begin(115200);

  pinMode(lane1_sensor_pin, INPUT);
  pinMode(lane2_sensor_pin, INPUT);
  pinMode(lane3_sensor_pin, INPUT);

  pinMode(L1_R, OUTPUT); pinMode(L1_Y, OUTPUT); pinMode(L1_G, OUTPUT);
  pinMode(L2_R, OUTPUT); pinMode(L2_Y, OUTPUT); pinMode(L2_G, OUTPUT);
  pinMode(L3_R, OUTPUT); pinMode(L3_Y, OUTPUT); pinMode(L3_G, OUTPUT);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) delay(500);

  espClient.setInsecure();
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) reconnect();
  client.loop();

  int l1 = digitalRead(lane1_sensor_pin);
  int l2 = digitalRead(lane2_sensor_pin);
  int l3 = digitalRead(lane3_sensor_pin);

  String data = "lane1:" + String(l1 == LOW ? "HIGH" : "LOW") +
                ",lane2:" + String(l2 == LOW ? "HIGH" : "LOW") +
                ",lane3:" + String(l3 == LOW ? "HIGH" : "LOW");

  Serial.println("Sending: " + data);
  client.publish("traffic/data", data.c_str());

  delay(1000);
}
\end{lstlisting}

\end{document}
