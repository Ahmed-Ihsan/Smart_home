import random
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Generate random sensor data
def generate_random_temperature():
    return round(random.uniform(-20, 40), 2)

def generate_random_humidity():
    return round(random.uniform(20, 80), 2)

def generate_random_light_intensity():
    return round(random.uniform(0, 1000), 2)

# Create data
num_data_points = 50
data = {
    'Time': list(range(1, num_data_points + 1)),
    'Temperature (°C)': [generate_random_temperature() for _ in range(num_data_points)],
    'Humidity (%)': [generate_random_humidity() for _ in range(num_data_points)],
    'Light Intensity (lux)': [generate_random_light_intensity() for _ in range(num_data_points)]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Set seaborn style
sns.set(style="whitegrid")

# Create line plots for temperature, humidity, and light intensity
plt.figure(figsize=(10, 6))
sns.lineplot(x='Time', y='Temperature (°C)', data=df, label='Temperature (°C)')
sns.lineplot(x='Time', y='Humidity (%)', data=df, label='Humidity (%)')
sns.lineplot(x='Time', y='Light Intensity (lux)', data=df, label='Light Intensity (lux)')
plt.title('Sensor Data Over Time')
plt.xlabel('Time')
plt.ylabel('Value')
plt.legend()
plt.show()

import numpy as np
import matplotlib.pyplot as plt

# Generate time values
fs = 1000  # Sampling frequency (samples per second)
t = np.arange(0, 10, 1/fs)  # 10 seconds of ECG data

# Generate a simple ECG-like waveform
ecg_signal = (
    0.5 * np.sin(2 * np.pi * 0.5 * t) +   # P wave
    1.0 * np.sin(2 * np.pi * 1.0 * t) -   # QRS complex
    0.5 * np.sin(2 * np.pi * 2.0 * t)     # T wave
)

# Add noise to the signal
noise = 0.1 * np.random.randn(len(t))
ecg_signal_with_noise = ecg_signal + noise

# Plot the ECG-like waveform
plt.figure(figsize=(12, 6))
plt.plot(t, ecg_signal_with_noise)
plt.title('Synthetic ECG-like Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.show()
