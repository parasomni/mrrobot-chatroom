#!/bin/python3
import os 

os.system("cp join.py /usr/bin/join")
os.system("chmod +x /usr/bin/join")
check_dir("/etc/join")
print("setting up triggers")
