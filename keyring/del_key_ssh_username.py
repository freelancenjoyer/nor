import keyring
keyring.delete_password('ssh', 'username')

print("the key has been deleted")
