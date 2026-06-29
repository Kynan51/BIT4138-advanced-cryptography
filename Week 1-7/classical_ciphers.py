import sys

def validate_text(prompt_text):
    """Ensures input contains only alphabetic characters (no numbers/symbols)."""
    while True:
        user_input = input(prompt_text).strip()
        if not user_input:
            print("[-] Error: Input cannot be empty. Try again.")
            continue
        if not user_input.replace(" ", "").isalpha():
            print("[-] Error: Input must only contain alphabetic letters (A-Z). No numbers or symbols allowed.")
            continue
        return user_input

def validate_caesar_key():
    """Ensures the Caesar key is a valid integer."""
    while True:
        try:
            key = int(input("[?] Enter Caesar shift key (Integer, e.g., 3): "))
            return key
        except ValueError:
            print("[-] Error: Caesar key must be a valid whole number. Try again.")

def validate_vigenere_key():
    """Ensures the Vigenère key is purely alphabetic."""
    while True:
        key = input("[?] Enter Vigenère keyword (Letters only): ").strip().upper()
        if not key or not key.isalpha():
            print("[-] Error: Vigenère key must contain letters only. Try again.")
            continue
        return key

# ==================== CIPHER ENGINES ====================

def caesar_cipher(text, shift, mode='encrypt'):
    """Encrypts or decrypts text using the Caesar Cipher algorithm."""
    if mode == 'decrypt':
        shift = -shift
    
    result = []
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            # The foundational shift loop formula
            shifted_char = chr((ord(char) - start + shift) % 26 + start)
            result.append(shifted_char)
        else:
            result.append(char) # Keeps spaces intact safely
    return "".join(result)

def vigenere_cipher(text, key, mode='encrypt'):
    """Encrypts or decrypts text using the Vigenère Cipher algorithm."""
    result = []
    key_index = 0
    key = key.upper()
    
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            shift = ord(key[key_index % len(key)]) - ord('A')
            
            if mode == 'decrypt':
                shift = -shift
                
            shifted_char = chr((ord(char) - start + shift) % 26 + start)
            result.append(shifted_char)
            key_index += 1
        else:
            result.append(char)
    return "".join(result)

# ==================== MAIN EXECUTION ====================

if __name__ == "__main__":
    print("\n" + "="*20 + " BIT4138 CRYPTO TESTING INTERFACE " + "="*20)
    
    # 1. Trigger Input Validation (For Figs 3 & 4)
    print("\n[!] Step 1: Testing Input Validation Safeguards...")
    plaintext = validate_text("[?] Enter Plaintext message to process: ")
    
    caesar_key = validate_caesar_key()
    vigenere_key = validate_vigenere_key()
    
    print("\n" + "="*15 + " EXECUTING CLASSICAL CRYPTOGRAPHY ALGORITHMS " + "="*15)
    
    # 2. Caesar Processing
    caesar_encrypted = caesar_cipher(plaintext, caesar_key, 'encrypt')
    caesar_decrypted = caesar_cipher(caesar_encrypted, caesar_key, 'decrypt')
    
    print(f"\n[+] [CAESAR] Shift Key: {caesar_key}")
    print(f"    [-] Ciphertext: {caesar_encrypted}")
    print(f"    [-] Decrypted:  {caesar_decrypted}")
    
    # 3. Vigenère Processing
    vigenere_encrypted = vigenere_cipher(plaintext, vigenere_key, 'encrypt')
    vigenere_decrypted = vigenere_cipher(vigenere_encrypted, vigenere_key, 'decrypt')
    
    print(f"\n[+] [VIGENÈRE] Key Word: {vigenere_key}")
    print(f"    [-] Ciphertext: {vigenere_encrypted}")
    print(f"    [-] Decrypted:  {vigenere_decrypted}")
    print("\n" + "="*60 + "\n")