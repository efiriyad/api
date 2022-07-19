from cryptography.fernet import Fernet

print("Fernet encryption algorithm, please enter passwords to encrypt (Press Enter to Stop)")
print("------------------------------------------------------------------------------------")

# Ask user to enter passwords until they enter an empty string.
# Store the passwords in a list.
passwords = []
i = 1
while True:
    password = input(f"User {i}: ")
    if password == "":
        break

    passwords.append(password)
    i += 1

print("------------------------------------------------------------------------------------")

cipher = Fernet.generate_key()

print(f"Private key: {cipher.decode()}")

for i, password in enumerate(passwords, 1):
    print(f"User {i}: {Fernet(cipher).encrypt(password.encode()).decode()}")
