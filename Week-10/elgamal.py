import random
import time

# --- Mathematical Helper Functions ---
def is_prime(n, k=5):
    if n < 2: return False
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]:
        if n == p: return True
        if n % p == 0: return False
    s, d = 0, n - 1
    while d % 2 == 0:
        if d == 0: break
        d //= 2
        s += 1
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1: continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1: break
        else: return False
    return True

def generate_large_prime(start=1000, end=5000):
    while True:
        p = random.randint(start, end)
        if is_prime(p):
            return p

def mod_inverse(a, m):
    g, x, y = ext_gcd(a, m)
    if g != 1:
        return None
    else:
        return x % m

def ext_gcd(a, b):
    if a == 0: return b, 0, 1
    gcd, x1, y1 = ext_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

# --- Core Cryptosystem Implementations ---
class ElGamal:
    @staticmethod
    def generate_keys():
        # Step 1 & 2: Choose Prime and Generator
        p = generate_large_prime(2000, 5000)
        # Simplified generator finder for academic sizing
        g = 2
        while pow(g, (p-1)//2, p) == 1:
            g += 1
        # Step 3: Private Key
        x = random.randint(2, p - 2)
        # Step 4: Public Key Calculation
        y = pow(g, x, p)
        return {"p": p, "g": g, "public_key": y, "private_key": x}

    @staticmethod
    def encrypt_char(char_ascii, p, g, y, custom_k=None):
        k = custom_k if custom_k is not None else random.randint(2, p - 2)
        c1 = pow(g, k, p)
        c2 = (char_ascii * pow(y, k, p)) % p
        return c1, c2, k

    @staticmethod
    def decrypt_char(c1, c2, p, x):
        s = pow(c1, x, p)
        s_inv = mod_inverse(s, p)
        if s_inv is None: return 0
        return (c2 * s_inv) % p

class RSA_Benchmark:
    @staticmethod
    def generate_keys():
        p = generate_large_prime(100, 500)
        q = generate_large_prime(500, 1000)
        while p == q:
            q = generate_large_prime(500, 1000)
        n = p * q
        phi = (p - 1) * (q - 1)
        e = 65537
        if phi % e == 0: e = 3
        d = mod_inverse(e, phi)
        return (e, n), (d, n)

    @staticmethod
    def encrypt(m, pub_key):
        e, n = pub_key
        return pow(m, e, n)

    @staticmethod
    def decrypt(c, priv_key):
        d, n = priv_key
        return pow(c, d, n)

# --- Elliptic Curve Demo Math (Weierstrass Form) ---
# Curve: y^2 = x^3 + ax + b (mod p)
class MiniECC:
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p

    def point_add(self, P, Q):
        if P is None: return Q
        if Q is None: return P
        x1, y1 = P
        x2, y2 = Q
        if x1 == x2 and y1 != y2: return None
        if x1 == x2 and y1 == y2: return self.point_double(P)
        
        num = (y2 - y1) % self.p
        den = mod_inverse((x2 - x1) % self.p, self.p)
        if den is None: return None
        lam = (num * den) % self.p
        
        x3 = (lam**2 - x1 - x2) % self.p
        y3 = (lam * (x1 - x3) - y1) % self.p
        return (x3, y3)

    def point_double(self, P):
        if P is None: return None
        x1, y1 = P
        if y1 == 0: return None
        
        num = (3 * x1**2 + self.a) % self.p
        den = mod_inverse((2 * y1) % self.p, self.p)
        if den is None: return None
        lam = (num * den) % self.p
        
        x3 = (lam**2 - 2 * x1) % self.p
        y3 = (lam * (x1 - x3) - y1) % self.p
        return (x3, y3)

    def scalar_mult(self, k, P):
        R = None
        Q = P
        while k > 0:
            if k % 2 == 1: R = self.point_add(R, Q)
            Q = self.point_double(Q)
            k //= 2
        return R

# --- System Run State Variables ---
current_keys = None
last_ciphertext = None

# --- Main UI Handler ---
def main_menu():
    global current_keys, last_ciphertext
    while True:
        print("\n===================================")
        print("     ELGAMAL SECURITY SYSTEM       ")
        print("===================================")
        print("1. Generate Keys")
        print("2. Encrypt Message")
        print("3. Decrypt Message")
        print("4. Compare RSA vs ElGamal (Benchmark)")
        print("5. ECC Demo Operations")
        print("6. Exit")
        choice = input("\nSelect an option (1-6): ").strip()

        if choice == '1':
            print("\nGenerating secure parameters...")
            current_keys = ElGamal.generate_keys()
            print("\n[+] Success! Keys Generated:")
            print(f" -> Prime Field (p): {current_keys['p']}")
            print(f" -> Generator (g):   {current_keys['g']}")
            print(f" -> Private Key (x): {current_keys['private_key']} (Keep Secret!)")
            print(f" -> Public Key (y):  {current_keys['public_key']}")

        elif choice == '2':
            if not current_keys:
                print("[-] Error: Generate ElGamal keys first using Option 1.")
                continue
            msg = input("Enter standard plaintext string: ")
            cipher_list = []
            print("\nEncrypting sequence details:")
            print(f"{'Char':<6}{'ASCII':<8}{'Random k':<10}{'C1 Code':<10}{'C2 Code'}")
            print("-" * 50)
            for char in msg:
                ascii_val = ord(char)
                c1, c2, k = ElGamal.encrypt_char(ascii_val, current_keys['p'], current_keys['g'], current_keys['public_key'])
                cipher_list.append((c1, c2))
                print(f"'{char}':<6{ascii_val:<8}{k:<10}{c1:<10}{c2}")
            last_ciphertext = cipher_list
            print("\n[+] Complete Ciphertext Payload Stored.")

        elif choice == '3':
            if not current_keys or not last_ciphertext:
                print("[-] Error: System context requires keys and active ciphertext payload.")
                continue
            decrypted_chars = []
            print("\nDecrypting payload segments...")
            for c1, c2 in last_ciphertext:
                plain_ascii = ElGamal.decrypt_char(c1, c2, current_keys['p'], current_keys['private_key'])
                decrypted_chars.append(chr(plain_ascii))
            recovered_string = "".join(decrypted_chars)
            print(f"\n[+] Recovered Decrypted Message: {recovered_string}")

        elif choice == '4':
            print("\nExecuting Cryptographic Performance Benchmark...")
            msg_char = 84  # Standard ASCII code 'T'
            
            # ElGamal Metric Analysis
            t0 = time.perf_counter()
            eg_keys = ElGamal.generate_keys()
            t1 = time.perf_counter()
            eg_c1, eg_c2, eg_k = ElGamal.encrypt_char(msg_char, eg_keys['p'], eg_keys['g'], eg_keys['public_key'])
            t2 = time.perf_counter()
            ElGamal.decrypt_char(eg_c1, eg_c2, eg_keys['p'], eg_keys['private_key'])
            t3 = time.perf_counter()
            
            eg_keygen = (t1 - t0) * 1000
            eg_enc = (t2 - t1) * 1000
            eg_dec = (t3 - t2) * 1000

            # RSA Metric Analysis
            t0 = time.perf_counter()
            rsa_pub, rsa_priv = RSA_Benchmark.generate_keys()
            t1 = time.perf_counter()
            rsa_c = RSA_Benchmark.encrypt(msg_char, rsa_pub)
            t2 = time.perf_counter()
            RSA_Benchmark.decrypt(rsa_c, rsa_priv)
            t3 = time.perf_counter()
            
            rsa_keygen = (t1 - t0) * 1000
            rsa_enc = (t2 - t1) * 1000
            rsa_dec = (t3 - t2) * 1000

            print("\n+---------------------------------------------------------+")
            print("| Algorithm | Key Gen (ms)  | Encrypt (ms)  | Decrypt (ms)  |")
            print("+---------------------------------------------------------+")
            print(f"| RSA       | {rsa_keygen:<13.4f} | {rsa_enc:<13.4f} | {rsa_dec:<13.4f} |")
            print(f"| ElGamal   | {eg_keygen:<13.4f} | {eg_enc:<13.4f} | {eg_dec:<13.4f} |")
            print("+---------------------------------------------------------+")
            print("\nArchitectural Observation Notes:")
            print(" -> ElGamal encryption requires computing two dynamic exponentiations due to random parameter k.")
            print(" -> RSA encryption with a small public exponent (e.g., 65537) processes drastically faster than asymmetric alternatives.")

        elif choice == '5':
            print("\nInitializing Elliptic Curve Operations Demo...")
            # Using curve parameters: y^2 = x^3 + 1x + 6 over Prime Field 11
            ecc = MiniECC(1, 6, 11)
            # Generator Base Point setup
            G = (2, 7)
            print(f"Using Curve Configuration: y^2 = x^3 + {ecc.a}x + {ecc.b} mod {ecc.p}")
            print(f"Base Generator Point G = {G}")
            
            # Compute point structures
            two_G = ecc.point_double(G)
            three_G = ecc.point_add(G, two_G)
            
            print(f" -> Point Doubling (2G) calculation: {two_G}")
            print(f" -> Point Addition (G + 2G = 3G):    {three_G}")
            
            # Demonstration of the hard problem
            priv_k = 4
            pub_pt = ecc.scalar_mult(priv_k, G)
            print(f" -> Scalar Multiplication ({priv_k} * G) [Public Key Point]: {pub_pt}")
            print("[Hardness Context] Knowing G and Public point, extracting the raw multiplier scalar is computationally infeasible on cryptographically large primes.")

        elif choice == '6':
            print("\nTerminating cryptosystem shell environment. Goodbye.")
            break
        else:
            print("[-] Invalid input configuration selected. Try options 1 to 6.")

if __name__ == "__main__":
    main_menu()