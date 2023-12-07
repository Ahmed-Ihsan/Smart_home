import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from scipy.io import loadmat
import matplotlib.pyplot as plt

# Load the dataset from .mat file
data = loadmat('rpy_9axis.mat')
sensor_data = data['sensorData']
Fs = data['Fs']

accelerometer_readings = sensor_data['Acceleration']
gyroscope_readings = sensor_data['AngularVelocity']
mag_readings = sensor_data['MagneticField']

# Combine sensor data into a single array
all_data = np.zeros((accelerometer_readings.shape[0], 3, 3))

for i in range(accelerometer_readings.shape[0]):
    all_data[i, 0, :] = accelerometer_readings[i, :]
    all_data[i, 1, :] = gyroscope_readings[i, :]
    all_data[i, 2, :] = mag_readings[i, :]

# Prepare dataset for CNN
for i in range(all_data.shape[0]):
    folder_name = str(round(all_data[i, 0, 0] * 1000))
    os.makedirs(os.path.join('Dataset', folder_name), exist_ok=True)
    plt.imsave(f'Dataset/{folder_name}/{i}.jpg', all_data[i, :, :])

# Prepare ImageDataGenerator for CNN
image_generator = ImageDataGenerator(validation_split=0.3)

train_generator = image_generator.flow_from_directory(
    'Dataset',
    target_size=(3, 3),
    batch_size=15,
    class_mode='categorical',
    subset='training'
)

validation_generator = image_generator.flow_from_directory(
    'Dataset',
    target_size=(3, 3),
    batch_size=15,
    class_mode='categorical',
    subset='validation'
)

# CNN Model
base_model = ResNet50(include_top=False, weights='imagenet', input_shape=(3, 3, 3))
for layer in base_model.layers:
    layer.trainable = False

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation='relu'),
    layers.Dense(2, activation='softmax')
])

model.compile(optimizer='sgd', loss='categorical_crossentropy', metrics=['accuracy'])

# Training CNN model
history = model.fit(train_generator, validation_data=validation_generator, epochs=20)

# DNN Model
net_dnn = models.Sequential([
    layers.Dense(10, activation='relu', input_shape=(features_train.shape[1],)),
    layers.Dense(4)  # Assuming output size is 4, please modify according to your actual output size
])

net_dnn.compile(optimizer='sgd', loss='mean_squared_error', metrics=['accuracy'])

# Train DNN model
history_dnn = net_dnn.fit(features_train, output, epochs=20)
