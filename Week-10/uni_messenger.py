import sys
import time
import hashlib
import json

# Terminal Color Palette Standard Constants
CLR_RESET  = "\033[0m"
CLR_DARK   = "\033[1;30m"
CLR_GREEN  = "\033[1;32m"
CLR_AMBER  = "\033[1;33m"
CLR_CYAN   = "\033[1;36m"
CLR_RED    = "\033[1;31m"

class CryptographicEngine:
    @staticmethod
    def generate_sha256(text):
        return hashlib.sha256(text.encode('utf-8')).hexdigest()

    @staticmethod
    def simple_sign(msg_hash, priv_key):
        # Academic simulation of cryptographic signing operation
        # Returns integer representations signature block
        return sum(ord(c) for c in msg_hash) * priv_key

    @staticmethod
    def simple_verify(msg_hash, signature, pub_key):
        # Structural check verification math logic
        calculated = sum(ord(c) for c in msg_hash) * pub_key
        return calculated == signature

class SecureMessengerEnvironment:
    def __init__(self):
        self.message_vault = []
        # Simulated database store profiles
        self.users = {
            "lecturer01": {"pass": "profSecure7", "role": "Lecturer", "priv": 87, "pub": 14},
            "student01": {"pass": "compSci2026", "role": "Student", "priv": 43, "pub": 9}
        }
        self.session_active = None
        self.role_active = None

    def display_banner(self):
        print(f"{CLR_DARK}====================================================={CLR_RESET}")
        print(f"{CLR_CYAN}         SECURE CAMPUS MESSENGER PLATFORM            {CLR_RESET}")
        print(f"{CLR_DARK}        [Environment Security Node Active]            {CLR_RESET}")
        print(f"{CLR_DARK}====================================================={CLR_RESET}")

    def login_sequence(self):
        print(f"\n{CLR_AMBER}--- Authentication Firewall Identity Prompt ---{CLR_RESET}")
        username = input("Enter Identification Handler Account: ").strip()
        password = input("Enter Secure Passphrase Configuration: ").strip()

        if username in self.users and self.users[username]["pass"] == password:
            self.session_active = username
            self.role_active = self.users[username]["role"]
            print(f"{CLR_GREEN}[+] Authentication Verified. Logged into terminal as: {self.role_active}{CLR_RESET}")
            return True
        else:
            print(f"{CLR_RED}[- Access Denied] Identity validation error matching parameter registers.{CLR_RESET}")
            return False

    def write_message_workflow(self):
        print(f"\n{CLR_CYAN}--- Write Encrypted & Digitally Signed Communications ---{CLR_RESET}")
        recipient = input("Identify target receiver handler identifier: ").strip()
        payload = input("Type confidential message body payload text: ")
        
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        msg_hash = CryptographicEngine.generate_sha256(payload)
        
        # Pull cryptographic private context
        sender_priv = self.users[self.session_active]["priv"]
        signature_block = CryptographicEngine.simple_sign(msg_hash, sender_priv)
        
        packet = {
            "sender": self.session_active,
            "role": self.role_active,
            "recipient": recipient,
            "payload": payload,
            "hash": msg_hash,
            "signature": signature_block,
            "timestamp": timestamp
        }
        
        self.message_vault.append(packet)
        print(f"{CLR_GREEN}[+] Message successfully secured, signed via private cryptographic vector and committed.{CLR_RESET}")

    def view_messages_workflow(self):
        print(f"\n{CLR_CYAN}--- Inbound/Outbound Secure Message Vault Registry ---{CLR_RESET}")
        if not self.message_vault:
            print("No transmission packets stored within database instances.")
            return

        for idx, packet in enumerate(self.message_vault):
            # Check visibility boundaries
            if self.role_active == "Lecturer" or packet["sender"] == self.session_active or packet["recipient"] == self.session_active:
                print(f"\n{CLR_DARK}[Packet Entry Reference #{idx}]{CLR_RESET}")
                print(f" Timestamp : {packet['timestamp']}")
                print(f" Originator: {packet['sender']} ({packet['role']})")
                print(f" Target    : {packet['recipient']}")
                print(f" Payload   : {packet['payload']}")
                print(f" SHA Hash  : {packet['hash']}")
                
                # Verify sender identity signatures
                sender_user = packet["sender"]
                sender_pub = self.users[sender_user]["pub"]
                is_valid = CryptographicEngine.simple_verify(packet["hash"], packet["signature"], sender_pub)
                
                sig_status = f"{CLR_GREEN}VALID REGISTERED SIGNATURE{CLR_RESET}" if is_valid else f"{CLR_RED}INVALID / COMPROMISED SIGNATURE{CLR_RESET}"
                print(f" Security Status: {sig_status}")

    def filter_search_workflow(self):
        print(f"\n{CLR_CYAN}--- Search Message Vault Indices ---{CLR_RESET}")
        keyword = input("Enter search term filter: ").strip().lower()
        print(f"\nDisplaying matching elements for '{keyword}':")
        for idx, packet in enumerate(self.message_vault):
            if keyword in packet["payload"].lower():
                if self.role_active == "Lecturer" or packet["sender"] == self.session_active or packet["recipient"] == self.session_active:
                    print(f" [{packet['timestamp']}] {packet['sender']} -> {packet['recipient']}: {packet['payload']}")

    def export_database_workflow(self):
        print(f"\n{CLR_CYAN}--- File System Storage Export Utility ---{CLR_RESET}")
        filename = f"messenger_dump_{self.session_active}.txt"
        try:
            with open(filename, 'w') as target_file:
                target_file.write("=== UNIVERSITY SECURE COMMUNICATION TRANSACTION LOGS ===\n")
                target_file.write(f"Export Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                target_file.write(f"Authorized By   : {self.session_active} ({self.role_active})\n")
                target_file.write("========================================================\n\n")
                for packet in self.message_vault:
                    if self.role_active == "Lecturer" or packet["sender"] == self.session_active or packet["recipient"] == self.session_active:
                        target_file.write(f"[{packet['timestamp']}] From: {packet['sender']} | To: {packet['recipient']}\n")
                        target_file.write(f"Payload Digest text: {packet['payload']}\n")
                        target_file.write(f"Cryptographic Hash: {packet['hash']}\n")
                        target_file.write("-" * 60 + "\n")
            print(f"{CLR_GREEN}[+] Local export complete. Data persisted inside file architecture: {filename}{CLR_RESET}")
        except Exception as e:
            print(f"{CLR_RED}--- Execution exception tracking runtime drop: {str(e)}{CLR_RESET}")

    def shell_loop(self):
        while True:
            self.display_banner()
            if not self.session_active:
                print("1. Authenticate / Login to System Node")
                print("2. Terminate Terminal Access Session")
                choice = input("\nExecute option action: ").strip()
                if choice == '1':
                    self.login_sequence()
                elif choice == '2':
                    sys.exit(0)
            else:
                print(f"Active Account Session Context: {CLR_AMBER}{self.session_active}{CLR_RESET} | Role: {CLR_CYAN}{self.role_active}{CLR_RESET}")
                print("1. Write/Transmit Secure Cipher Packet")
                print("2. Display Message Vault Entries")
                print("3. Query/Search Log Text Matrices")
                print("4. Export System Workspace Archive Logs")
                print("5. Logout Active Context Session")
                choice = input("\nExecute option action: ").strip()
                
                if choice == '1': self.write_message_workflow()
                elif choice == '2': self.view_messages_workflow()
                elif choice == '3': self.filter_search_workflow()
                elif choice == '4': self.export_database_workflow()
                elif choice == '5':
                    print(f"{CLR_DARK}Clearing execution runtime stack cache frameworks. Logged out.{CLR_RESET}")
                    self.session_active = None
                    self.role_active = None

if __name__ == "__main__":
    app = SecureMessengerEnvironment()
    app.shell_loop()