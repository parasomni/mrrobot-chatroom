#!/usr/bin/python3
# chatroom server
import threading
import socket
from datetime import datetime
import sys
import time
from cryptography.fernet import Fernet

def write_log(log):
    with open ('chat_log.txt', 'ab') as logFile:
        nl = '\r\n'
        log += nl.encode()
        logFile.write(log)
    logFile.close()

def log(msg):
    current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_ = (f'[{current_date_time}] -- {msg}:')
    return log_

def encrypt_data(fileData):
        with open('key.txt', 'rb') as keyFile:
            key = keyFile.read()
        keyFile.close()
        fernet = Fernet(key)
        encryptedData = fernet.encrypt(fileData)
        return encryptedData

def decrypt_data(fileData):
        with open('key.txt', 'rb') as keyFile:
            key = keyFile.read()
        keyFile.close()
        fernet = Fernet(key)
        decryptedData = fernet.decrypt(fileData)
        return decryptedData

def valid_check(user):
    with open('validUsers.txt', 'r') as f:
        userFile = f.read()
    f.close()
    users = []
    comma = ','
    commaPos = []
    for pos, char in enumerate(userFile):
        if (char == comma):
            commaPos.append(pos)
    userCount = len(commaPos) - 1
    for count in range(userCount):
        users.append(userFile[commaPos[count]+1:commaPos[count+1]])
    #print(f'{user} == {users[0]}')
    if user in users:
        return True
    else:
        return False

def banned_check(user):
    with open('bannedUsers.txt', 'r') as f:
        userFile = f.read()
    f.close()
    users = []
    comma = ','
    commaPos = []
    for pos, char in enumerate(userFile):
        if (char == comma):
            commaPos.append(pos)
    userCount = len(commaPos) - 1
    for count in range(userCount):
        users.append(userFile[commaPos[count]+1:commaPos[count+1]])
    #if user in users:
    if user == users[0]:
        return True
    else:
        return False

def userCheck(user):
    valid = 'valid'
    banned = 'banned'
    invalid = 'invalid'
    check = valid_check(user)
    #print (check)
    check2 = banned_check(user)
    if check:
        return valid
    elif check2:
        return banned
    else:
        return invalid

def room_check(room):
    with open('rooms.txt', 'r') as f:
        roomFile = f.read()
    f.close()
    rooms = []
    comma = ','
    commaPos = []
    for pos, char in enumerate(roomFile):
        if (char == comma):
            commaPos.append(pos)
    roomCount = len(commaPos) - 1
    #print(f'{room} == {rooms[0]}')
    for count in range(roomCount):
        rooms.append(roomFile[commaPos[count]+1:commaPos[count+1]])
    if room in rooms:
        return True
    else:
        return False

def main():
    host = '192.0.0.1'
    port = 1001
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    clients = []
    users = []

    def broadcast(message):
        for client in clients:
            write_log(message)
            message = encrypt_data(message)
            client.send(message)

    def log(msg):
        current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_ = (f'[{current_date_time}] -- {msg}')
        return log_

    def handle(client):
        while True:
            try:
                msg = client.recv(1024)
                msg = decrypt_data(msg)
                msg = msg.decode()
                msg = log(msg)
                broadcast(msg.encode())
            except:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                user = users[index]
                log_ = f'{user} left the chat!'
                log_ = log(log_)
                log_ = log_.encode()
                write_log(log_)
                broadcast(log_)
                users.remove(user)
                break

    def receive():
        def log(msg):
                current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                log_ = (f'[{current_date_time}] -- {msg}')
                return log_
        while True:
            client, address = server.accept()
            #print(f"Connected with {str(address)}")
            room = client.recv(1024)
            room = decrypt_data(room)
            room = room.decode()
            if room_check(room):
                client.send(('ack').encode())
                time.sleep(0.2)
                user = client.recv(1024)
                user = decrypt_data(user)
                user = user.decode()
                check = userCheck(user)
                #print(check)
                if check == 'valid':
                    client.send(('200').encode())
                    time.sleep(0.2)
                    users.append(user)
                    clients.append(client)
                    msg = f'{user} joined the chat!'
                    msg = log(msg)
                    msg = msg.encode()
                    write_log(msg)
                    broadcast(msg)
                    msg = f'connected to {room}!'
                    msg = log(msg)
                    msg = msg.encode()
                    msg = encrypt_data(msg)
                    client.send(msg)

                elif check == 'banned':
                    client.send(('404').encode())
                    time.sleep(0.2)
                    log_ = f'{user} is banned from {room}'
                    log_ = log(log_)
                    log = log_.encode()
                    write_log(log)
                    log = encrypt_data(log)
                    client.send(log)

                else:
                    client.send(('403').encode())

            else:
                client.send(('rst').encode())

            thread = threading.Thread(target=handle, args=(client,))
            thread.start()

    #print(bcolors.RED + "Server is online...")
    try:
        receive()
    except Exception as e:
        print(e)
        pass

try:
    main()

except KeyboardInterrupt:
    print("Server closes...")
    sys.exit()
except Exception as e:
    print(e)
    pass
