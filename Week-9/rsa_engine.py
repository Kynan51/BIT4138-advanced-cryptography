import hashlib
import cryptomath

class RSAEngine:
    def __init__(self):
        self.p = None
        self.q = None
        self.n = None
        self.phi = None
        self.e = 65537
        self.d = None

    def generate_keypair(self, bits=512):
        """Part A: Key Generation Implementation."""
        self.p = cryptomath.generate_large_prime(bits)
        self.q = cryptomath.generate_large_prime(bits)
        
        while self.p == self.q:
            self.q = cryptomath.generate_large_prime(bits)

        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)

        # Ensure e is coprime to the Euler Totient equation
        while cryptomath.gcd(self.e, self.phi) != 1:
            self.e = cryptomath.random.randint(3, self.phi - 1)
            if self.e % 2 == 0:
                self.e += 1

        self.d = cryptomath.mod_inverse(self.e, self.phi)
        return {
            "p": self.p, "q": self.q, "n": self.n,
            "phi": self.phi, "e": self.e, "d": self.d
        }

    def encrypt(self, plaintext, public_key_e=None, modulus_n=None):
        """Part B: Plaintext character to ASCII conversion and raw encryption."""
        e = public_key_e if public_key_e is not None else self.e
        n = modulus_n if modulus_n is not None else self.n
        
        if not e or not n:
            raise ValueError("Keys must be fully generated before encryption operations.")
            
        execution_trace = []
        cipher_integers = []
        
        for char in plaintext:
            ascii_val = ord(char)
            encrypted_val = pow(ascii_val, e, n)
            cipher_integers.append(encrypted_val)
            execution_trace.append((char, ascii_val, encrypted_val))
            
        return cipher_integers, execution_trace

    def decrypt(self, cipher_integers, private_key_d=None, modulus_n=None):
        """Part C: Ciphertext decryption conversion loop returning original text."""
        d = private_key_d if private_key_d is not None else self.d
        n = modulus_n if modulus_n is not None else self.n
        
        if not d or not n:
            raise ValueError("Keys must be fully configured before decryption operations.")
            
        execution_trace = []
        decrypted_characters = []
        
        for cipher_val in cipher_integers:
            decrypted_ascii = pow(cipher_val, d, n)
            original_char = chr(decrypted_ascii)
            decrypted_characters.append(original_char)
            execution_trace.append((cipher_val, decrypted_ascii, original_char))
            
        return "".join(decrypted_characters), execution_trace

    def compute_sha256(self, message):
        """Helper to hash messages using standard SHA-256 hashes."""
        return hashlib.sha256(message.encode('utf-8')).hexdigest()

    def sign(self, message):
        """Part D: Computes digital signatures by encrypting SHA-256 hashes with private keys."""
        if not self.d or not self.n:
            raise ValueError("Private key configuration missing. Cannot sign document payload.")
        hash_hex = self.compute_sha256(message)
        hash_int = int(hash_hex, 16)
        signature = pow(hash_int, self.d, self.n)
        return hash_hex, signature

    def verify(self, message, signature, public_key_e=None, modulus_n=None):
        """Part E: Validates structural integrity by checking signature values against a public key."""
        e = public_key_e if public_key_e is not None else self.e
        n = modulus_n if modulus_n is not None else self.n
        
        if not e or not n:
            raise ValueError("Public key configuration missing. Verification failed.")
            
        original_hash_hex = self.compute_sha256(message)
        recovered_hash_int = pow(signature, e, n)
        
        # Format matching dynamic hex character configurations
        recovered_hash_hex = hex(recovered_hash_int)[2:].zfill(64)
        return original_hash_hex == recovered_hash_hex, original_hash_hex, recovered_hash_hex