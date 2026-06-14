from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import os

def run_software_guard_demo():
    print("==================================================")
    print("🛡️ SECURE SOFTWARE UPDATE SIGNING LAB")
    print("==================================================\n")

    # STEP 1: Developer Environmental setup (Key Generation)
    print("[STAGE 1: GENERATING DEVELOPER CRYPTOGRAPHIC IDENTITIES]")
    developer_private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    developer_public_key = developer_private_key.public_key()
    print("✅ Keypair generated successfully (RSA 2048-bit).\n")

    # STEP 2: Package creation and signing
    print("[STAGE 2: PACKAGING AND SIGNING SOFTWARE UPDATE]")
    software_payload = b"print('System updating... Installing Security Patches v4.1.2')"
    
    # Generate the digital signature using the private key
    software_signature = developer_private_key.sign(
        software_payload,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )
    print(f" - Software Update File Contents: {software_payload}")
    print(f" - Generated Vendor Digital Signature: {software_signature.hex()[:50]}...")
    print("📦 Update Package ready for deployment.\n")

    # STEP 3: Client Validation (Successful Deployment)
    print("[STAGE 3: CLIENT SIMULATION - VALIDATING AUTHENTIC UPDATE]")
    try:
        developer_public_key.verify(
            software_signature,
            software_payload,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        print("✅ VERIFICATION SUCCESSFUL: Signature matches developer certificate.")
        print("🚀 ACTION: Executing verified code payload safely...")
    except Exception:
        print("❌ CRITICAL ERROR: Package identification failed.")

    print("\n" + "="*50 + "\n")

    # STEP 4: Threat Emulation (Man-in-the-Middle Payload Interception)
    print("[STAGE 4: THREAT EMULATION - INJECTING MALICIOUS PAYLOAD]")
    # Attacker modifies the update payload but leaves the old signature or tries to forge it
    tampered_payload = b"print('System hacked! Executing malware payload...')"
    print(f"⚠️ Attacker swapped payload to: {tampered_payload}")
    
    try:
        print("🔍 Client Endpoint scanning update metadata...")
        developer_public_key.verify(
            software_signature,  # Sending original signature with modified payload
            tampered_payload,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        print("🚀 ACTION: Executing update...")
    except Exception:
        print("🚨 SECURITY ALERT: DIGITAL SIGNATURE MISMATCH OR CERTIFICATE UNTRUSTED!")
        print("🛑 ACTION: Operation aborted. Dropping corrupt software package to protect kernel.")

if __name__ == "__main__":
    run_software_guard_demo()