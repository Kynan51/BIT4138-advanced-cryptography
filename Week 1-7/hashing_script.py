import hashlib
import time
import bcrypt

print("==================================================")
print("   BIT4138 WEEK 6: HASHING & PASSWORD SECURITY   ")
print("==================================================")

# ---  SHA-256 HASH GENERATION ---
print("\n--- [ SHA-256 Hash Generation] ---")
data_payload = b"BIT4138_Integrity_Verification_Payload_2026"

# Generate standard SHA-256 Hash
sha256_hash = hashlib.sha256(data_payload).hexdigest()
print(f"Input Data: '{data_payload.decode()}'")
print(f"SHA-256 (Hex): {sha256_hash}")

# Demonstrate Avalanche Effect (Changing 1 character changes the whole hash)
altered_payload = b"BIT4138_Integrity_Verification_Payload_2025"
altered_hash = hashlib.sha256(altered_payload).hexdigest()
print(f"Altered Data: '{altered_payload.decode()}'")
print(f"Altered Hash: {altered_hash} (Avalanche Effect)")


# ---  PASSWORD HASHING SYSTEM ---
print("\n--- [ Password Hashing System] ---")
user_password = "SecureStudentPassword99!"

# Generate a unique cryptographic salt and hash using bcrypt (Work factor = 12)
print("Generating unique salt and executing work-factor stretching...")
generated_salt = bcrypt.gensalt(rounds=12)
hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), generated_salt)

print(f"Plaintext Password: {user_password}")
print(f"Generated Salt:     {generated_salt.decode('utf-8')}")
print(f"Stored Bcrypt Hash: {hashed_password.decode('utf-8')}")


# ---  LOGIN AUTHENTICATION WORKFLOW ---
print("\n--- [ Login Authentication Workflow] ---")
# Simulating a user typing their password at a login prompt
input_attempt_1 = "SecureStudentPassword99!"
input_attempt_2 = "WrongPassword123!"

print(f"Simulating User Login Attempt 1 with: '{input_attempt_1}'")
print(f"Simulating User Login Attempt 2 with: '{input_attempt_2}'")


# ---  HASH VERIFICATION RESULTS ---
print("\n--- [ Hash Verification Results] ---")
# Verifying Attempt 1
is_valid_1 = bcrypt.checkpw(input_attempt_1.encode('utf-8'), hashed_password)
print(f"Verification 1 Result (Correct Password): {is_valid_1} -> ACCESS GRANTED")

# Verifying Attempt 2
is_valid_2 = bcrypt.checkpw(input_attempt_2.encode('utf-8'), hashed_password)
print(f"Verification 2 Result (Incorrect Password): {is_valid_2} -> ACCESS DENIED")


# ---  PASSWORD SECURITY TESTING ---
print("\n--- [ Password Security Testing] ---")
print("Benchmarking Bcrypt computational delay (Work Factor / Rounds tuning):")

for rounds in [10, 11, 12]:
    start_time = time.time()
    _ = bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt(rounds=rounds))
    elapsed = time.time() - start_time
    print(f" -> Bcrypt Rounds {rounds} execution time: {elapsed:.4f} seconds")

print("\nConclusion: The execution delay protects against offline Brute-Force/Rainbow Table attacks.")