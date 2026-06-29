import time

# ANSI Escape Codes for Terminal Colors
CYAN = "\033[96m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
GREEN = "\033[92m"
MAGENTA = "\033[95m"
RESET = "\033[0m"
BOLD = "\033[1m"

def print_banner(text):
    print(f"\n{BOLD}{MAGENTA}{'='*60}\n{text:^60}\n{'='*60}{RESET}\n")

# 1. Public Parameters (The Base Paint)
p = 23  
g = 5   
print_banner("🛸 STEP 1: PUBLIC PARAMETERS AGREED ONSHORE 🛸")
print(f"{CYAN}[COMMON BASE COATING]{RESET} Public Prime (p): {p}, Generator/Base Color (g): {g}")
time.sleep(1)

# 2. Private Keys (The Secret Colors)
print_banner("🔐 STEP 2: CHOSING SECRET INGREDIENTS (PRIVATE) 🔐")
alice_private = 6
bob_private = 15
print(f"{YELLOW}[ALICE]{RESET} Secret Color Factor (a): {alice_private}  -> (Kept hidden from Eve!)")
print(f"{BLUE}[BOB]{RESET} Secret Color Factor (b): {bob_private} -> (Kept hidden from Eve!)")
time.sleep(1)

# 3. Public Keys (The Mixed Colors sent over the air)
print_banner("🧪 STEP 3: MIXING & EXCHANGING PUBLIC COLORS 🧪")
alice_public = pow(g, alice_private, p)  # 5^6 mod 23 = 8
bob_public = pow(g, bob_private, p)    # 5^15 mod 23 = 19

print(f"{YELLOW}[ALICE]{RESET} mixed Base({g}) with Secret({alice_private}) mod {p}.")
print(f"       👉 Resulting Public Mix (A): {GREEN}████ {alice_public}{RESET}")
print(f"{BLUE}[BOB]{RESET} mixed Base({g}) with Secret({bob_private}) mod {p}.")
print(f"     👉 Resulting Public Mix (B): {GREEN}████ {bob_public}{RESET}")
print("\n...Exchanging mixed colors across the open cosmic channel...")
time.sleep(1.5)

# 4. Shared Secret Computation (The Final Secret Shared Shade)
print_banner("🎨 STEP 4: COMPUTING THE FINAL SHARED SECRET SHADE 🎨")
alice_secret = pow(bob_public, alice_private, p)
bob_secret = pow(alice_public, bob_private, p)

print(f"{YELLOW}[ALICE]{RESET} injects her SecretFactor({alice_private}) into Bob's Mix({bob_public}).")
print(f"       Final Shared Secret Paint Code: {BOLD}{GREEN}████ {alice_secret}{RESET}")

print(f"{BLUE}[BOB]{RESET} injects his SecretFactor({15}) into Alice's Mix({alice_public}).")
print(f"     Final Shared Secret Paint Code: {BOLD}{GREEN}████ {bob_secret}{RESET}")

# Verification
if alice_secret == bob_secret:
    print(f"\n{BOLD}{GREEN}🎉 SUCCESS: Secure Cryptographic Key Connection Verified!{RESET}")
else:
    print(f"\n{BOLD}\033[91m❌ ERROR: Key mismatch.{RESET}")