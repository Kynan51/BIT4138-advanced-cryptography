import os
from datetime import datetime
from rsa_engine import RSAEngine

# ANSI Escape sequences to enable rich colored console outputs
CLR_RESET  = "\033[0m"
CLR_RED    = "\033[91m"
CLR_GREEN  = "\033[92m"
CLR_YELLOW = "\033[93m"
CLR_BLUE   = "\033[94m"
CLR_CYAN   = "\033[96m"

LOG_FILE = "rsa_chat_history.txt"

class ChatParticipant:
    def __init__(self, username, bit_strength=512):
        self.username = username
        self.crypto_engine = RSAEngine()
        print(f"[*] Generating cryptographically secure keypairs for {CLR_CYAN}{username}{CLR_RESET}...")
        self.keys = self.crypto_engine.generate_keypair(bits=bit_strength)

def clear_chat_history():
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    print(f"{CLR_RED}[!] Local history clearing execution complete.{CLR_RESET}")

def log_message_to_file(timestamp, sender, recipient, ciphertext, decrypted):
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(f"Timestamp: {timestamp}\n")
        file.write(f"Sender:    {sender}\n")
        file.write(f"Recipient: {recipient}\n")
        file.write(f"Ciphertext Array: {str(ciphertext)}\n")
        file.write(f"Decrypted Payload: {decrypted}\n")
        file.write("-" * 50 + "\n")

def run_chat_system():
    print(f"{CLR_GREEN}=========================================")
    print("      WELCOME TO RSA SECURE CHAT")
    print(f"========================================={CLR_RESET}")
    
    # Initialize global multi-user registry matching requirements
    directory = {
        "Alice": ChatParticipant("Alice", bit_strength=512),
        "Bob": ChatParticipant("Bob", bit_strength=512)
    }
    
    while True:
        print(f"\n{CLR_YELLOW}--- CHAT NETWORKING OPERATIONS PANEL ---{CLR_RESET}")
        print("1. Transmit Encrypted Message")
        print("2. Print Registered Users & Public Keys")
        print("3. Register New Participant Profile")
        print("4. Inspect Disk Storage Log Archive")
        print("5. Purge History File Logs")
        print("6. Exit Chat Console")
        
        choice = input("Enter selection index (1-6): ").strip()
        
        if choice == '1':
            sender = input(f"Specify SENDER Identity {list(directory.keys())}: ").strip()
            recipient = input(f"Specify RECIPIENT Identity {list(directory.keys())}: ").strip()
            
            if sender not in directory or recipient not in directory:
                print(f"{CLR_RED}[-] Participant mismatch error. Validate identities and try again.{CLR_RESET}")
                continue
                
            raw_text = input(f"Enter plain payload text string for {CLR_CYAN}{recipient}{CLR_RESET}: ")
            if not raw_text:
                print(f"{CLR_RED}[-] Transmission aborted. Content empty.{CLR_RESET}")
                continue
                
            # Intercept variables from specific targeted address entries
            recipient_engine = directory[recipient].crypto_engine
            recipient_pub_e = directory[recipient].keys['e']
            recipient_mod_n = directory[recipient].keys['n']
            
            sender_engine = directory[sender].crypto_engine
            
            # Cross-encrypt plaintext using the target recipient's public key
            cipher_ints, _ = recipient_engine.encrypt(raw_text, recipient_pub_e, recipient_mod_n)
            
            # Sign plaintext payload to assure authenticity profile matching
            _, signature = sender_engine.sign(raw_text)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"\n{CLR_GREEN}[+] NETWORK ENVELOPE TRANSMITTED SUCCESSFULLY:{CLR_RESET}")
            print(f"    {CLR_BLUE}Cipher blocks sent:{CLR_RESET} {cipher_ints}")
            
            # Recipient decrypts payload via personal internal private key
            recovered_text, _ = recipient_engine.decrypt(cipher_ints)
            
            # Recipient validates authenticity via the sender's public key
            sig_valid, _, _ = recipient_engine.verify(recovered_text, signature, directory[sender].keys['e'], directory[sender].keys['n'])
            
            print(f"\n{CLR_GREEN}[+] RECIPIENT ({recipient}) INCOMING DECRYPTED INBOX:{CLR_RESET}")
            print(f"    [Time Record]: {timestamp}")
            print(f"    [Plain Payload]: {CLR_YELLOW}{recovered_text}{CLR_RESET}")
            
            if sig_valid:
                print(f"    [Authentication]: {CLR_GREEN}Signature Verified! Authenticated from {sender}.{CLR_RESET}")
            else:
                print(f"    [Authentication]: {CLR_RED}CRITICAL WARNING: Integrity Compromised!{CLR_RESET}")
                
            log_message_to_file(timestamp, sender, recipient, cipher_ints, recovered_text)

        elif choice == '2':
            print(f"\n{CLR_BLUE}--- GLOBAL PUBLIC KEY DIRECTORY REGISTER ---{CLR_RESET}")
            for name, profile in directory.items():
                print(f"User: {CLR_CYAN}{name}{CLR_RESET}")
                print(f"  Public key exponent (e): {profile.keys['e']}")
                # Limit size string on printing space allocation optimization
                print(f"  Modulus parameter (n):   {str(profile.keys['n'])[:40]}...")

        elif choice == '3':
            new_user = input("Input new account unique handle: ").strip()
            if not new_user or new_user in directory:
                print(f"{CLR_RED}[-] Error: Handle name blank or profile key collision.{CLR_RESET}")
                continue
            directory[new_user] = ChatParticipant(new_user, bit_strength=512)
            print(f"{CLR_GREEN}[+] Account active. Profile logged to registry cluster.{CLR_RESET}")

        elif choice == '4':
            print(f"\n{CLR_CYAN}--- READING DISK LOG ARCHIVE ({LOG_FILE}) ---{CLR_RESET}")
            if not os.path.exists(LOG_FILE):
                print("[-] Storage archive empty or log file uninitialized.")
                continue
            with open(LOG_FILE, "r", encoding="utf-8") as file:
                print(file.read())

        elif choice == '5':
            clear_chat_history()
            
        elif choice == '6':
            print(f"\n{CLR_GREEN}[+] Secure Chat terminal sequence ended. Terminating routing loops.{CLR_RESET}")
            break
        else:
            print(f"{CLR_RED}[-] Input out of range. Check numeric mapping.{CLR_RESET}")

if __name__ == "__main__":
    run_chat_system()
    