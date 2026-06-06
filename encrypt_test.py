from cryptography.fernet import Fernet

# 1. Generate a secure symmetric key
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# 2. Define the plaintext data
plaintext = b"BIT4138: Advanced Cryptography Local Test"

# 3. Encrypt the data
ciphertext = cipher_suite.encrypt(plaintext)

# 4. Decrypt it back
decrypted_text = cipher_suite.decrypt(ciphertext)

# 5. Print results to the terminal window 
print("=" * 60)
print(f"[+] Generated Key: {key.decode()}")
print(f"[+] Original Text: {plaintext.decode()}")
print(f"[+] Ciphertext (Encrypted): {ciphertext.decode()[:50]}...")
print(f"[+] Decrypted Text: {decrypted_text.decode()}")
print("=" * 60)