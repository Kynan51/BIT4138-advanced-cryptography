# User Input for parameters
p = int(input("Public Prime (p): "))
g = int(input("Generator (g): "))

# Private Key Inputs
alice_private = int(input("Alice Secret Key: "))
bob_private = int(input("Bob Secret Key: "))

# Compute Public Keys
alice_public = pow(g, alice_private, p)
bob_public = pow(g, bob_private, p)

# Compute Shared Secrets
alice_secret = pow(bob_public, alice_private, p)
bob_secret = pow(alice_public, bob_private, p)

print(f"\nShared Secret: {alice_secret}")
assert alice_secret == bob_secret, "Secrets do not match!"