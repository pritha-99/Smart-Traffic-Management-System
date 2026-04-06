# 🚦 Smart Traffic Management System using ESP32, MQTT & Cloud

## 📌 Overview

This project implements an IoT-based intelligent traffic management system that dynamically controls traffic signals based on real-time vehicle density. It uses ESP32, IR sensors, and MQTT communication via HiveMQ Cloud, with a Python-based decision engine to optimize traffic flow.

---

## 🎯 Objective

To design a smart traffic control system that:
- Monitors vehicle density using sensors
- Sends real-time data to the cloud
- Processes data using a decision algorithm
- Dynamically controls traffic signals

---

## 🧠 System Architecture

ESP32 (Sensors + LEDs)
        ↓
   MQTT Publish
        ↓
   HiveMQ Cloud Broker
        ↓
   Python Application (Decision Logic)
        ↓
   MQTT Publish
        ↓
   ESP32 (Traffic Signal Control)

---

## 🧰 Hardware Requirements

- ESP32 Development Board
- IR Sensors (3 or 4 units)
- Red, Yellow, Green LEDs (for each lane) or Traffic Module (for each lane)
- Resistors (220Ω / 330Ω) (if using LEDs)
- Breadboard
- Jumper wires
- USB cable / Power supply

---

## 💻 Software Requirements

- Arduino IDE
- Python
- HiveMQ Cloud (MQTT broker)
- Replit (For hosting Python code)

### Arduino Libraries
- WiFi.h
- WiFiClientSecure.h
- PubSubClient.h

### Python Libraries
- paho-mqtt

---

## 🌐 Communication Protocol

- MQTT (Message Queuing Telemetry Transport)

---

## ⚙️ Working Principle

1. IR sensors detect vehicle presence in each lane
2. ESP32 reads sensor data and publishes it to MQTT topic:
   traffic/data
3. Python application subscribes to this topic and processes data
4. Based on traffic density, Python decides which lane gets priority
5. Python publishes control commands:
   traffic/command
6. ESP32 receives commands and controls LEDs accordingly

---

## 📡 MQTT Topics

- traffic/data → Sensor data from ESP32
- traffic/command → Signal control commands

---

## 🧪 Example Data Format

ESP32 → Cloud:
lane1:HIGH,lane2:LOW,lane3:HIGH

Cloud → ESP32:
lane1:GREEN,lane2:RED,lane3:RED

---

## 🚀 Features

- Real-time traffic monitoring
- Cloud-based decision making
- Dynamic signal control
- Scalable for multiple lanes
- Lightweight MQTT communication

---

## 📈 Learning Outcomes

- Understanding of IoT system architecture
- Hands-on experience with ESP32
- MQTT communication (publish/subscribe model)
- Cloud integration (HiveMQ)
- Python-based automation and decision logic

---

## 🔮 Future Scope

- Integration with AI/ML for predictive traffic control
- Mobile app dashboard
- Emergency vehicle priority system
- Integration with smart city infrastructure

---


## 📜 License

This project is for educational purposes.

---

## 💬 Notes

- Ensure all components use the same MQTT broker
- Use TLS (port 8883) for secure communication
- Maintain consistent topic naming across all modules
