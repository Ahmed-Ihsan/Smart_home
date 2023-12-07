from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding as sym_padding
import os
import time
import pandas as pd
# import pip
# pip.main(['install','seaborn'])
import seaborn as sns
import matplotlib.pyplot as plt

# Function to generate a random message of given length in bytes
def generate_random_message(length):
    return os.urandom(length)

# Function to measure encryption and decryption time for AES
def measure_aes_time(key_length, message_length):
    key = os.urandom(key_length // 8)
    message = generate_random_message(message_length)

    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()

    padder = sym_padding.PKCS7(128).padder()
    padded_message = padder.update(message) + padder.finalize()

    start_time = time.time()
    encrypted_message = encryptor.update(padded_message) + encryptor.finalize()
    encryption_time = time.time() - start_time

    decryptor = cipher.decryptor()
    unpadder = sym_padding.PKCS7(128).unpadder()

    start_time = time.time()
    decrypted_message = decryptor.update(encrypted_message) + decryptor.finalize()
    decryption_time = time.time() - start_time

    # Remove padding after decryption
    unpadded_message = unpadder.update(decrypted_message) + unpadder.finalize()

    return encryption_time, decryption_time

if __name__ == "__main__":
    key_lengths = [128, 192, 256]  # Key lengths in bits
    message_lengths = [50 * 1000_000, 100 * 1000_000, 150 * 1000_000]  # Message lengths in bytes (50MB, 100MB, 150MB)
    num_rounds = 10  # Number of measurement rounds

    results = []

    for key_length in key_lengths:
        for message_length in message_lengths:
            aes_encryption_times = []
            aes_decryption_times = []

            for _ in range(num_rounds):
                # Measure AES encryption and decryption times
                aes_encryption_time, aes_decryption_time = measure_aes_time(key_length, message_length)
                aes_encryption_times.append(aes_encryption_time)
                aes_decryption_times.append(aes_decryption_time)
            
            # Calculate the average times for this combination
            avg_aes_encryption_time = sum(aes_encryption_times) / num_rounds
            avg_aes_decryption_time = sum(aes_decryption_times) / num_rounds

            # Print the average times
            print(f"Key Length: {key_length} bits, Message Length: {message_length / (1024 * 1024):.1f} MB")
            print(f"Avg AES Encryption Time: {avg_aes_encryption_time:.6f} seconds")
            print(f"Avg AES Decryption Time: {avg_aes_decryption_time:.6f} seconds")
            print("-" * 40)
            
            # Append results
            results.append({
                "Key Length (bits)": key_length,
                "Message Length (MB)": message_length / 1000_000 ,
                "Avg AES Encryption Time (s)": avg_aes_encryption_time,
                "Avg AES Decryption Time (s)": avg_aes_decryption_time,
            })
                    
    df = pd.DataFrame(results)

    # Set seaborn style
    sns.set(style="whitegrid")

    # Create subplots for average AES Encryption and Decryption times
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    sns.barplot(x="Message Length (MB)", y="Avg AES Encryption Time (s)", hue="Key Length (bits)", data=df)
    plt.title("Average AES Encryption Time (10 Rounds)")
    plt.xlabel("Message Length (MB)")
    plt.ylabel("Time (s)")

    plt.subplot(1, 2, 2)
    sns.barplot(x="Message Length (MB)", y="Avg AES Decryption Time (s)", hue="Key Length (bits)", data=df)
    plt.title("Average AES Decryption Time (10 Rounds)")
    plt.xlabel("Message Length (MB)")
    plt.ylabel("Time (s)")

    plt.tight_layout()

    # Show the plot
    plt.show()
    
    