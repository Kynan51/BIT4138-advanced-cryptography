import hashlib
import re

# Mock database of leaked password hashes (commonly breached patterns)
LEAKED_HASHES_DB = {
    hashlib.sha256("password123".encode()).hexdigest(): "password123",
    hashlib.sha256("12345678".encode()).hexdigest(): "12345678",
    hashlib.sha256("admin2026".encode()).hexdigest(): "admin2026",
    hashlib.sha256("qwerty".encode()).hexdigest(): "qwerty",
}

def analyze_password(password: str):
    print("=" * 50)
    print(f"🕵️ LAB ANALYSIS FOR INPUT: '{password}'")
    print("=" * 50)
    
    # 1. Structural Security Checklist
    score = 0
    checks = {
        "Length >= 10 chars": len(password) >= 10,
        "Contains Numbers": bool(re.search(r"\d", password)),
        "Contains Uppercase": bool(re.search(r"[A-Z]", password)),
        "Contains Special Char": bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))
    }
    
    print("\n[STEP 1: ENTROPY & STRUCTURE CHECK]")
    for check, passed in checks.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f" - {check}: {status}")
        if passed: score += 1
        
    strength = "WEAK" if score < 3 else "STRONG"
    print(f"👉 Structural Strength Assessment: {strength} ({score}/4 criteria met)")

    # 2. Hash Generation
    print("\n[STEP 2: CRYPTOGRAPHIC HASH GENERATION]")
    user_hash = hashlib.sha256(password.encode()).hexdigest()
    print(f" - Computed SHA-256 Hash: {user_hash}")

    # 3. Simulated Leak/Breach Lookup
    print("\n[STEP 3: SIMULATED BREACH & RAINBOW TABLE LOOKUP]")
    if user_hash in LEAKED_HASHES_DB:
        print("🚨 ALERT! MATCH FOUND IN BREACH DATABASE!")
        print(f"   The hash matches known leaked plaintext: '{LEAKED_HASHES_DB[user_hash]}'")
        print("   Status: COMPROMISED (Even if structurally strong, it is unsafe!)")
    else:
        print("🛡️ No matches found in the leak database. Password is structurally isolated.")

if __name__ == "__main__":
    # Test Case A: Weak, Compromised Password
    analyze_password("password123")
    
    print("\n" + "#"*60 + "\n")
    
    # Test Case B: Strong, Safe Password
    analyze_password("P@ss_W0rd_Extr3m3_2026")