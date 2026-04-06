import paho.mqtt.client as mqtt
import time
import os
import matplotlib.pyplot as plt

# 🔹 HiveMQ
broker = HIVEMQ_HOST
port = 8883
username = MQTT_USERNAME
password = MQTT_PASSWORD

# 🔹 State
mode = "IDLE"
last_switch = time.time()
GREEN_TIME = 5

lane1 = "LOW"
lane2 = "LOW"
lane3 = "LOW"

lane1_state = "YELLOW"
lane2_state = "YELLOW"
lane3_state = "YELLOW"

active_lanes = []
current_index = 0

history = []

# 🔹 Graph
lane1_data, lane2_data, lane3_data, time_data = [], [], [], []
start_time = time.time()
last_graph_save = time.time()

# 🔹 UI
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def light(s):
    return "🟢" if s=="GREEN" else "🟡" if s=="YELLOW" else "🔴"

def display():
    clear()
    print("==== 🚦 3-LANE SMART TRAFFIC SYSTEM ====")
    print("Mode:", mode)
    print("Active Lanes:", active_lanes)

    print("\nLane1   Lane2   Lane3")
    print(light(lane1_state), "     ", light(lane2_state), "     ", light(lane3_state))

    print("\nRecent:")
    for h in history[-5:]:
        print(h)

# 🔹 Publish
def publish(client, l1, l2, l3):
    global lane1_state, lane2_state, lane3_state

    lane1_state = l1
    lane2_state = l2
    lane3_state = l3

    msg = f"lane1:{l1},lane2:{l2},lane3:{l3}"
    client.publish("traffic/command", msg)

    history.append(msg)

# 🔹 MQTT
def on_connect(client, userdata, flags, rc):
    client.subscribe("traffic/data")

def on_message(client, userdata, msg):
    global lane1, lane2, lane3, mode, active_lanes, current_index

    data = msg.payload.decode()

    try:
        parts = data.split(",")
        lane1 = parts[0].split(":")[1]
        lane2 = parts[1].split(":")[1]
        lane3 = parts[2].split(":")[1]
    except:
        return

    # 🔹 Graph data
    lane1_data.append(1 if lane1=="HIGH" else 0)
    lane2_data.append(1 if lane2=="HIGH" else 0)
    lane3_data.append(1 if lane3=="HIGH" else 0)
    time_data.append(int(time.time() - start_time))

    if len(time_data) > 40:
        lane1_data.pop(0)
        lane2_data.pop(0)
        lane3_data.pop(0)
        time_data.pop(0)

    # 🔹 NEW ACTIVE LANE SET
    new_active = []
    if lane1 == "HIGH": new_active.append("lane1")
    if lane2 == "HIGH": new_active.append("lane2")
    if lane3 == "HIGH": new_active.append("lane3")

    # 🔹 RESET ONLY IF CHANGED
    if new_active != active_lanes:
        active_lanes = new_active
        current_index = 0

    # 🔹 Mode logic
    if len(active_lanes) == 0:
        mode = "IDLE"
    elif len(active_lanes) == 1:
        mode = "PRIORITY"
    else:
        mode = "ROUND"

# 🔹 Logic
def logic(client):
    global current_index, last_switch

    now = time.time()

    # IDLE
    if mode == "IDLE":
        publish(client, "YELLOW", "YELLOW", "YELLOW")
        return

    # PRIORITY
    if mode == "PRIORITY":
        publish(client,
            "GREEN" if lane1=="HIGH" else "RED",
            "GREEN" if lane2=="HIGH" else "RED",
            "GREEN" if lane3=="HIGH" else "RED"
        )
        return

    # ROUND ROBIN (FIXED)
    if mode == "ROUND":
        if now - last_switch > GREEN_TIME:
            current_index = (current_index + 1) % len(active_lanes)
            last_switch = now

        current_lane = active_lanes[current_index]

        publish(client,
            "GREEN" if current_lane=="lane1" else "RED",
            "GREEN" if current_lane=="lane2" else "RED",
            "GREEN" if current_lane=="lane3" else "RED"
        )

# 🔹 Graph
def graph():
    global last_graph_save

    if time.time() - last_graph_save < 5:
        return

    plt.clf()
    plt.plot(time_data, lane1_data, label="Lane1")
    plt.plot(time_data, lane2_data, label="Lane2")
    plt.plot(time_data, lane3_data, label="Lane3")

    plt.ylim(-0.2, 1.2)
    plt.legend()
    plt.grid()

    plt.savefig("graph.png")
    last_graph_save = time.time()

# 🔹 Setup
client = mqtt.Client()
client.username_pw_set(username, password)
client.tls_set()

client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port)
client.loop_start()

plt.figure(figsize=(6,4))

# 🔹 Loop
while True:
    logic(client)
    display()
    graph()
    time.sleep(1)


