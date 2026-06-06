import time
import os

# ==================== LFSR GENERATOR  ====================

def run_lfsr(seed, taps, num_bits):
    """
    Simulates a Linear Feedback Shift Register (LFSR).
    Seed: Initial state list of bits, e.g., [1, 0, 1, 1]
    Taps: Indices used for the XOR feedback logic, e.g., [0, 3] (taps on bit 0 and bit 3)
    """
    state = list(seed)
    length = len(state)
    bitstream = []
    
    for _ in range(num_bits):
        # 1. Output the current rightmost bit
        output_bit = state[-1]
        bitstream.append(output_bit)
        
        # 2. Calculate the feedback bit using XOR logic based on the tap positions
        feedback = state[taps[0]]
        for tap in taps[1:]:
            feedback ^= state[tap]
            
        # 3. Shift the register right and insert the feedback bit at the leftmost position
        state = [feedback] + state[:-1]
        
    return bitstream

def run_frequency_test(bits):
    """Performs a Monobit Frequency Test to check 0-and-1 distribution density."""
    total = len(bits)
    ones = bits.count(1)
    zeros = bits.count(0)
    ones_pct = (ones / total) * 100
    zeros_pct = (zeros / total) * 100
    
    print("\n📊 [STATISTICAL RANDOMNESS TESTING]")
    print(f"   [-] Sequence Length Checked : {total} bits")
    print(f"   [-] Distribution of '1's    : {ones} ({ones_pct:.2f}%)")
    print(f"   [-] Distribution of '0's    : {zeros} ({zeros_pct:.2f}%)")
    
    deviation = abs(ones_pct - 50.0)
    if deviation < 5.0:
        print("   [+] Test Verdict: PASSED (Uniform cryptographic distribution)")
    else:
        print("   [-] Test Verdict: FAILED (High sequence bias detected)")

# ====================  RC4 STREAM CIPHER (Figs 4, 5) ====================

def rc4_ksa(key):
    """Key Scheduling Algorithm (KSA) for RC4."""
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    return S

def rc4_prga(S, data_bytes):
    """Pseudo-Random Generation Algorithm (PRGA) to encrypt/decrypt data."""
    i = 0
    j = 0
    out = []
    for byte in data_bytes:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        keystream_byte = S[(S[i] + S[j]) % 256]
        out.append(byte ^ keystream_byte) # Stream cipher XOR operation
    return bytes(out)

# ==================== EXECUTION & PROFILING ====================

if __name__ == "__main__":
    print("\n" + "="*15 + " WEEK 3: STREAM CIPHERS & RANDOMNESS ANALYSIS " + "="*15)
    
    # --- LFSR Segment ---
    initial_seed = [1, 0, 1, 1, 0, 0, 1, 0] # 8-bit seed state
    tap_positions = [0, 2, 3, 7]           # Feedback tap configurations
    generation_length = 500
    
    print(f"\n[!] Initializing LFSR Engine with Seed: {initial_seed}")
    generated_bits = run_lfsr(initial_seed, tap_positions, generation_length)
    
    # Print raw pseudorandom sequence segment
    raw_seq_str = "".join(str(b) for b in generated_bits[:64])
    print(f"[+] Pseudorandom Sequence Stream (First 64 bits): {raw_seq_str}...")
    
    # Execute the statistical testing engine
    run_frequency_test(generated_bits)
    
    # --- RC4 Segment ---
    print("\n" + "-"*30 + " RC4 STREAM ENCRYPTION LAB " + "-"*30)
    secret_key = b"ParrotSecureCryptoKey"
    plaintext_payload = b"Advanced Cryptography BIT4138 Secure Payload Verification String"
    
    print(f"[!] Target Payload: {plaintext_payload.decode()}")
    
    # Simulate standard runtime encryption execution
    state_arr = rc4_ksa(secret_key)
    encrypted_bytes = rc4_prga(state_arr, plaintext_payload)
    print(f"[+] RC4 Ciphertext Output (Hex): {encrypted_bytes.hex().upper()[:60]}...")
    
    # Simulate reverse verification decryption
    state_arr_reset = rc4_ksa(secret_key)
    decrypted_bytes = rc4_prga(state_arr_reset, encrypted_bytes)
    print(f"[+] RC4 Decrypted Output Plain: {decrypted_bytes.decode()}")
    
    # --- Performance Benchmarking ---
    print("\n [ENCRYPTION PERFORMANCE METRICS]")
    stress_payload = os.urandom(5_000_000) # Create 5 Megabytes of mock stream data
    
    t_start = time.perf_counter()
    rc4_state = rc4_ksa(secret_key)
    _ = rc4_prga(rc4_state, stress_payload)
    t_end = time.perf_counter()
    
    duration = t_end - t_start
    throughput = (5000000 / (1024 * 1024)) / duration
    print(f"   [-] Processing Time for 5MB Stream Data : {duration:.4f} seconds")
    print(f"   [-] Calculated Cipher Engine Throughput : {throughput[0]:.2f} MB/s" if isinstance(throughput, tuple) else f"   [-] Calculated Cipher Engine Throughput : {throughput:.2f} MB/s")
    print("="*70 + "\n")