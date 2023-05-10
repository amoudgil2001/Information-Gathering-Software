from cryptography.fernet import Fernet

key = Fernet.generate_key()

file = open('encryption.txt', 'wb')
file.write(key)
file.close()
print(key)