import keyring

print(keyring.get_password('ssh', 'username'))
