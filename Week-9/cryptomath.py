import random

def gcd(a, b):
    """Compute the Greatest Common Divisor using Euclidean Algorithm."""
    while b:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    """Extended Euclidean Algorithm to calculate coefficients for Bezout's identity."""
    if a == 0:
        return b, 0, 1
    gcd_val, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd_val, x, y

def mod_inverse(e, phi):
    """Compute the modular multiplicative inverse of e modulo phi."""
    gcd_val, x, _ = extended_gcd(e, phi)
    if gcd_val != 1:
        raise ValueError("Modular inverse does not exist because values are not coprime.")
    return x % phi

def miller_rabin(n, k=40):
    """
    Miller-Rabin Primality Test.
    Returns True if n is probably prime, False if composite.
    """
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False

    # Factor out powers of 2 from n - 1 such that n - 1 = 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Witness loop
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_large_prime(bits=512):
    """Generates a secure large prime number verified via Miller-Rabin."""
    while True:
        n = random.getrandbits(bits)
        n |= (1 << (bits - 1)) | 1  # Ensure appropriate bit size and odd state
        if miller_rabin(n):
            return n

def pollard_rho(n):
    """
    Pollard's Rho Factorization Algorithm.
    Used to rapidly find non-trivial factors of a composite integer.
    """
    if n % 2 == 0:
        return 2
    if miller_rabin(n):
        return n
        
    x = random.randint(2, n - 1)
    y = x
    c = random.randint(1, n - 1)
    g = 1
    
    cycle_function = lambda val: (pow(val, 2, n) + c) % n
    
    while g == 1:
        x = cycle_function(x)
        y = cycle_function(cycle_function(y))
        g = gcd(abs(x - y), n)
        
    if g == n:
        return pollard_rho(n)  # Retry with a different constant if failure occurs
    return g