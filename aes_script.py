import os
import time
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

# ---  KEY GENERATION PROCESS ---
print("--- [ Key Generation Process] ---")
# AES-256 requires a 32-byte (256-bit) key
secret_key = get_random_bytes(32)
print(f"Generated 256-bit AES Key (Hex): {secret_key.hex()}")

# ---  FILE ENCRYPTION DEMONSTRATION ---
print("\n--- [ File Encryption Demonstration] ---")
filename = "sensitive_data.txt"
plaintext = b"BIT4138 Logbook: Confidentially securing student records using AES-CBC mode."

# Write original text to file
with open(filename, "wb") as f:
    f.write(plaintext)
print(f"Original file '{filename}' created with content: '{plaintext.decode()}'")

# AES CBC mode requires a 16-byte Initialization Vector (IV)
iv = get_random_bytes(16)
cipher_encrypt = AES.new(secret_key, AES.MODE_CBC, iv)

# Pad plaintext to be a multiple of the 16-byte block size
padded_data = pad(plaintext, AES.block_size)
ciphertext = cipher_encrypt.encrypt(padded_data)

# Save encrypted data to file
encrypted_filename = "sensitive_data.enc"
with open(encrypted_filename, "wb") as f:
    f.write(iv + ciphertext) # Prepend IV for use during decryption
print(f"File encrypted successfully. Saved as '{encrypted_filename}'")
print(f"Ciphertext (Hex): {ciphertext.hex()[:50]}...")

# ---  DECRYPTION RESULTS ---
print("\n--- [ Decryption Results] ---")
# Read encrypted file
with open(encrypted_filename, "rb") as f:
    file_content = f.read()

# Extract IV (first 16 bytes) and ciphertext
extracted_iv = file_content[:16]
extracted_ciphertext = file_content[16:]

cipher_decrypt = AES.new(secret_key, AES.MODE_CBC, extracted_iv)
decrypted_padded = cipher_decrypt.decrypt(extracted_ciphertext)
decrypted_text = unpad(decrypted_padded, AES.block_size)

print(f"Decryption successful!")
print(f"Decrypted Content matches original: {decrypted_text == plaintext}")
print(f"Decrypted Text: '{decrypted_text.decode()}'")

# ---  AES PERFORMANCE TESTING ---
print("\n--- [ AES Performance Testing] ---")
# Benchmark encrypting 10MB of dummy data
large_data = get_random_bytes(10 * 1024 * 1024) 
padded_large_data = pad(large_data, AES.block_size)

start_time = time.time()
test_cipher = AES.new(secret_key, AES.MODE_CBC, iv)
_ = test_cipher.encrypt(padded_large_data)
end_time = time.time()

execution_time = end_time - start_time
print(f"Processed Size: 10 MB")
print(f"AES Encryption Time: {execution_time:.4f} seconds")
print(f"Throughput: {(10 / execution_time):.2f} MB/s")