from flask import Flask, render_template, redirect, url_for
import paho.mqtt.client as mqtt
from cryptography.fernet import Fernet

app = Flask(__name__)

data_by_raspberry = {}

# Decrypts the encrypted data using the provided key
def decrypt(key, encrypted_data):
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
    return decrypted_data

def on_message(client, userdata, message):
    payload = message.payload
    topic_parts = message.topic.split("/")
    raspberry_name = topic_parts[1]
    sensor_name = topic_parts[2]
    
    # Replace "your_secret_key" with the actual key
    key = 'W1ZbJI5IrBg5pPcUUOIcQAGBWa5Ozye8kM-syAUP3gM='
    decrypted_data = decrypt(key, payload)
    
    if raspberry_name not in data_by_raspberry:
        data_by_raspberry[raspberry_name] = {}
    
    # if sensor_name not in data_by_raspberry[raspberry_name]:
    data_by_raspberry[raspberry_name][sensor_name] = decrypted_data
        
client = mqtt.Client()

# Connect to the MQTT broker
broker_address = "127.0.0.1"
broker_port = 1883
client.connect(broker_address, broker_port)

# Set up the on_message callback after defining the function
client.on_message = on_message

# Subscribe to the desired topic
topic = "sensor_data/#"
client.subscribe(topic)

@app.route('/')
def index():
    return render_template('index.html', data_by_raspberry=data_by_raspberry)

@app.route('/del')
def clear_data():
    data_by_raspberry.clear()
    return redirect(url_for('index'))

# Start the MQTT loop in a separate thread
client.loop_start()

if __name__ == '__main__':
    app.run()
