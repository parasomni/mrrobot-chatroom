#!/bin/python3

import os 
from cryptography.fernet import Fernet

key = Fernet.generate_key()
with open("key.txt", "wb") as f:
    f.write(key)
f.close()
print("private key written to key.txt")
os.system('cp server.py /usr/bin/mrrobot-server')
os.system('chmod +x /usr/bin/mrrobot-server')
print("setting up triggers")
os.system('echo ",<elliot>," > validUsers.txt')
print("creating valid users")
os.system('echo ",<elliot>," > user.txt')
print("creating user")
os.system('echo ",<white-rose>," > bannedUsers.txt')
print("creating banned users")
os.system('echo ",fsociety," > rooms.txt')
print("creating chatrooms")
