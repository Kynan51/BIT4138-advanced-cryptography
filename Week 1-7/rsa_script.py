import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.Signature import pss

print("==================================================")
print("   BIT4138 WEEK 5: RSA KEY MANAGEMENT & CRYPTO   ")
print("==================================================\n")

# ---  RSA KEY PAIR GENERATION ---
print("--- [ RSA Key Pair Generation] ---")
# Generate a secure 2048-bit RSA key pair
private_key = RSA.generate(2048)
public_key = private_key.publickey()

# Export keys to PEM format for display
private_pem = private_key.export_key().decode('utf-8')
public_pem = public_key.export_key().decode('utf-8')

print("Successfully generated 2048-bit RSA Key Pair.")
print(f"Public Key Snippet:\n{public_pem[:150]}...\n--- END PUBLIC KEY ---")
print(f"Private Key Snippet:\n{private_pem[:150]}...\n--- END PRIVATE KEY ---")


# ---  PUBLIC KEY ENCRYPTION PROCESS ---
print("\n--- [ Public Key Encryption Process] ---")
secret_message = b"BIT4138: Confidential RSA Session Key Exchange Data."
print(f"Original Message: {secret_message.decode()}")

# Use PKCS#1 OAEP for secure asymmetric encryption padding
cipher_encrypt = PKCS1_OAEP.new(public_key)
ciphertext = cipher_encrypt.encrypt(secret_message)

print("Encryption complete using Recipient's Public Key.")
print(f"Ciphertext (Hex): {ciphertext.hex()[:60]}...")


# ---  PRIVATE KEY DECRYPTION RESULTS ---
print("\n--- [ Private Key Decryption Results] ---")
# Decrypting using the corresponding Private Key
cipher_decrypt = PKCS1_OAEP.new(private_key)
decrypted_message = cipher_decrypt.decrypt(ciphertext)

print("Decryption complete using Recipient's Private Key.")
print(f"Decrypted Message Match: {decrypted_message == secret_message}")
print(f"Decrypted Result: '{decrypted_message.decode()}'")


# ---  SECURE MESSAGE TRANSMISSION (Digital Signatures) ---
print("\n--- [ Secure Message Transmission] ---")
# To ensure Authenticity & Non-repudiation, the sender signs a hash of the message
message_to_sign = b"Secure payload transmitted across untrusted network."
message_hash = SHA256.new(message_to_sign)

# Sign with Sender's Private Key
signature = pss.new(private_key).sign(message_hash)
print("Message securely signed using Sender's Private Key.")
print(f"Digital Signature (Hex): {signature.hex()[:60]}...")


# ---  RSA TESTING AND VALIDATION ---
print("\n--- [ RSA Testing and Validation] ---")
# The recipient verifies the signature using the Sender's Public Key
verifier_hash = SHA256.new(message_to_sign)
verifier = pss.new(public_key)

try:
    verifier.verify(verifier_hash, signature)
    print("✅ Validation SUCCESS: Digital signature is VALID.")
    print("Integrity: Authenticated. Data has not been modified.")
except (ValueError, TypeError):
    print("❌ Validation FAILURE: Invalid signature detected.")