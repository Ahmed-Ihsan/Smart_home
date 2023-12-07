import paho.mqtt.client as mqtt
from cryptography.fernet import Fernet

class DataDecryption:
    def __init__(self, key):
        self.key = key

    def decrypt(self, encrypted_data):
        cipher_suite = Fernet(self.key)
        decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
        return decrypted_data

class Computer:
    def __init__(self):
        self.data_decryption = DataDecryption(key='W1ZbJI5IrBg5pPcUUOIcQAGBWa5Ozye8kM-syAUP3gM=')  # استبدل بالمفتاح السري الخاص بك

    def process_sensor_data(self, topic, encrypted_data, room_number, sensor_name):
        decrypted_data = self.data_decryption.decrypt(encrypted_data)
        print(f"Received data from Room {room_number}, Sensor {sensor_name}: {decrypted_data}")

def on_message(client, userdata, message):
    payload = message.payload
    topic_parts = message.topic.split("/")
    try:
        room_number = topic_parts[1]
        sensor_name = topic_parts[2]
    except:
        print("Error")
        room_number = 1
        sensor_name = 10
    computer.process_sensor_data(message.topic, payload, room_number, sensor_name)

# إعداد الحاسوب والاتصال بالوسيط MQTT
computer = Computer()

client = mqtt.Client()
client.on_message = on_message
client.connect("127.0.0.1", 1883)
client.subscribe("sensor_data/#")
client.loop_forever()
