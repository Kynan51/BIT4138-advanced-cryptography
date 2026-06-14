from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import os

# 1. Key Generation
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

# 2. Document Data
document_data = b"Academic Logbook Data: Integrity Verified."

# 3. Digital Signature Generation
signature = private_key.sign(
    document_data,
    padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
    hashes.SHA256()
)

print("---  SIGNATURE GENERATION ---")
print(f"Document Message: {document_data.decode()}")
print(f"Generated PSS Signature (Hex): {signature.hex()[:64]}...")

# 4. Signature Verification Process
print("\n--- SIGNATURE VERIFICATION & VALIDATION ---")
try:
    public_key.verify(
        signature,
        document_data,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )
    print("[SUCCESS] Signature matches document. Integrity & Authenticity confirmed!")
except Exception:
    print("[FAILURE] Signature validation failed.")

# 5. Security Testing (Tamper Test)
print("\n--- TAMPER TESTING ---")
tampered_data = b"Academic Logbook Data: Integrity Altered."
try:
    public_key.verify(
        signature,
        tampered_data,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )
except Exception as e:
    print(f"[REJECTED] Document data was modified! Verification failed: {str(e)}")