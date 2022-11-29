import keyring
from getpass4 import getpass

pw = getpass('pass: ')
keyring.set_password('ssh', 'username', pw)
print("the key has been activated")
