#!/bin/python3
import os 

def check_dir(dirPath):
    if os.path.exists(str(dirPath)):
        #self.print_log(f'Directory {dirPath} exists.')
        pass
    else:
        print(f'Directory {dirPath} does not exist --> creating...')
        os.makedirs(dirPath)

os.system("cp join.py /usr/bin/join")
os.system("chmod +x /usr/bin/join")
check_dir("/etc/join")
print("setting up triggers")
os.system("cp user.txt /etc/join/")
os.system("key.txt /etc/join/key-chatroom.txt")
