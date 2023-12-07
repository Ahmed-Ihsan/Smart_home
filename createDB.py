import numpy as np
from scipy.io import savemat

# Number of data points
num_points = 1000

# Generate random accelerometer, gyroscope, and magnetometer data for 1000 rows
acceleration = np.random.randn(num_points, 3)
gyroscope = np.random.randn(num_points, 3)
magnetometer = np.random.randn(num_points, 3)

# Generate random timestamps
time = np.linspace(0, 10, num_points)

# Create the data dictionary
random_data = {
    'Acceleration': acceleration,
    'AngularVelocity': gyroscope,
    'MagneticField': magnetometer,
    'Time': time
}

# Save the dictionary to a .mat file
savemat('random_data.mat', random_data)
