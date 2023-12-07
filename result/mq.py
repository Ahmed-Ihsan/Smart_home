import paho.mqtt.client as mqtt
import time
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# MQTT broker settings
broker_address = "127.0.0.1"
port = 1883
topic = "test_topic"

# Create an MQTT client
client = mqtt.Client()

# Callback function for when the message is received
def on_message(client, userdata, message):
    global start_time
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Received message: {message.payload.decode()}")
    print(f"Time taken to receive message: {elapsed_time:.6f} seconds")

# Set the callback function
client.on_message = on_message

# Connect to the MQTT broker
client.connect(broker_address, port)

# Start the MQTT client loop
client.loop_start()

# Message lengths in bytes
message_lengths = [1000000, 2000000, 3000000, 4000000]  # Modify as needed
num_rounds = 10  # Number of measurement rounds

results = []

for length in message_lengths:
    total_publish_time = 0

    for round_num in range(num_rounds):
        # Create a message with the desired length
        message = "A" * length
        
        # Publish message and measure time
        start_time = time.time()
        client.publish(topic, message)
        print(f"Published message with length {length} bytes (Round {round_num + 1})")

        # Subscribe to the topic to receive the published message
        client.subscribe(topic)

        # Allow time for the message to be received
        time.sleep(2)  # Adjust as needed

        # Calculate and accumulate publish times
        end_time = time.time()
        publish_time = end_time - start_time -2
        total_publish_time += publish_time

        # Unsubscribe from the topic
        client.unsubscribe(topic)

    # Calculate and print average times for this message length
    avg_publish_time = total_publish_time / num_rounds
    print(f"Average Publish Time (Message Length {length} bytes): {avg_publish_time:.6f} seconds")
    print("-" * 40)

    results.append({
        "Message Length (Bytes)": length,
        "Average Publish Time (Seconds)": avg_publish_time
    })

# Disconnect from the MQTT broker
client.loop_stop()
client.disconnect()

# Create a DataFrame from the results
df = pd.DataFrame(results)

# Set seaborn style
sns.set(style="whitegrid")

# Create a bar plot to visualize average publish times
plt.figure(figsize=(8, 6))
sns.barplot(x="Message Length (Bytes)", y="Average Publish Time (Seconds)", data=df)
plt.title("Average MQTT Publish Time vs. Message Length")
plt.xlabel("Message Length (Bytes)")
plt.ylabel("Average Publish Time (Seconds)")
plt.show()
