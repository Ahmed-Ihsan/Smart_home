import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import paho.mqtt.client as mqtt
from cryptography.fernet import Fernet
from collections import defaultdict

# Initialize variables
sensor_data = defaultdict(list)

# MQTT broker details
MQTT_BROKER_HOST = "127.0.0.1"
MQTT_BROKER_PORT = 1883
MQTT_TOPIC = "sensor_data/#"

# Create MQTT client
client = mqtt.Client()

# Replace with your actual Fernet key
FERNET_KEY = 'W1ZbJI5IrBg5pPcUUOIcQAGBWa5Ozye8kM-syAUP3gM='

# Callback when message is received
def on_message(client, userdata, message):
    topic_parts = message.topic.split("/")
    raspberry_node = topic_parts[1]
    sensor_name = topic_parts[2]

    encrypted_payload = message.payload
    cipher_suite = Fernet(FERNET_KEY)
    decrypted_payload = cipher_suite.decrypt(encrypted_payload)

    sensor_data[(raspberry_node, sensor_name)].append(float(decrypted_payload.decode()))
    if len(sensor_data[(raspberry_node, sensor_name)]) > 10:
        sensor_data[(raspberry_node, sensor_name)].pop(0)

# Configure MQTT client
client.on_message = on_message
client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT)
client.subscribe(MQTT_TOPIC)
client.loop_start()

# Create figure and axis
fig, ax = plt.subplots()
lines = {}

# Create lines for each sensor
for sensor_name in ["Temperature", "HeartRate", "Humidity", "Gas"]:
    lines[sensor_name], = ax.plot([], [], label=sensor_name)
    sensor_data[("4", sensor_name)] = []

ax.set_xlim(0, 10)
ax.set_ylim(0, 100)
ax.legend()

# Animation update function
def update(frame):
    for sensor_name, line in lines.items():
        x_data = list(range(len(sensor_data[("2", sensor_name)])))
        y_data = sensor_data[("2", sensor_name)]
        line.set_data(x_data, y_data)
        ax.relim()
        ax.autoscale_view()

# Create animation
ani = FuncAnimation(fig, update, frames=None, blit=False)

# Display the plot
plt.show()
