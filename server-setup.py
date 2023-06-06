#!/bin/python3

import os 
from cryptography.fernet import Fernet

def check_dir(dirPath):
    if os.path.exists(str(dirPath)):
        #self.print_log(f'Directory {dirPath} exists.')
        pass
    else:
        print(f'Directory {dirPath} does not exist --> creating...')
        os.makedirs(dirPath)

key = Fernet.generate_key()
with open("/etc/join/key-chatroom.txt", "wb") as f:
    f.write(key)
f.close()
check_dir("/etc/join/")
print("private key written to key.txt")
os.system('cp server.py /usr/bin/mrrobot-server')
os.system('chmod +x /usr/bin/mrrobot-server')
print("setting up triggers")
os.system('echo ",<elliot>," > /etc/join/validUsers.txt')
print("creating valid users")
os.system('echo ",<elliot>," > /etc/join/user.txt')
print("creating user")
os.system('echo ",<white-rose>," > /etc/join/bannedUsers.txt')
print("creating banned users")
os.system('echo ",fsociety," > /etc/join/rooms.txt')
print("creating chatrooms")
