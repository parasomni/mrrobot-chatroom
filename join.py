#!/usr/bin/python3
# client script
import socket
import threading
import sys
import time
import getpass
from cryptography.fernet import Fernet

def encrypt_data(fileData):
        with open('/etc/join/key-chatroom.txt', 'rb') as keyFile:
            key = keyFile.read()
        keyFile.close()
        fernet = Fernet(key)
        encryptedData = fernet.encrypt(fileData)
        return encryptedData

def decrypt_data(fileData):
        with open('/etc/join/key-chatroom.txt', 'rb') as keyFile:
            key = keyFile.read()
        keyFile.close()
        fernet = Fernet(key)
        decryptedData = fernet.decrypt(fileData)
        return decryptedData

def main():
    address = '192.0.0.1'
    port = 1001

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        #print("Connecting to the server...")
        client.connect((address, port))
    except ConnectionRefusedError:
        print("Failed to connect to the server!")
        sys.exit()

    print("connected successfully.")
    with open('/etc/join/user.txt', 'r') as f:
        userFile = f.read()
    f.close()
    comma = ','
    userName = ''
    commaPos = []
    for pos, char in enumerate(userFile):
        if (char == comma):
            commaPos.append(pos)
    userCount = len(commaPos) - 1
    for count in range(userCount):
        userName = userFile[commaPos[count]+1:commaPos[count+1]]
    rtk = sys.argv[1]
    #print("Sending roomtoken")
    rtk = rtk.encode()
    rtk = encrypt_data(rtk)
    client.send(rtk)
    time.sleep(0.2)
    answ = client.recv(1024).decode()
    if answ == 'ack':
        userName_ = userName.encode()
        userName_ = encrypt_data(userName_)
        client.send(userName_)
        time.sleep(0.2)
        answ = client.recv(1024).decode()
        #print(answ)
        if answ == '200':
            pass
        elif answ == '404':
            msg = client.recv(1024).decode()
            print(msg)
            sys.exit()
        else:
            print('an error occurred')
            sys.exit()

    elif answ == 'rst':
        print('invalid chatroom')
        sys.exit()

    def receive():
        while True:
            try:
                message = client.recv(1024)
                if not message:
                    break
                message = decrypt_data(message)
                try:
                    message = decrypt_data(message)
                except Exception as e:
                    pass
                message = message.decode()
                print(message)

            except Exception as e:
                client.close()
                print (e)

            except KeyboardInterrupt:
                client.shutdown(socket.SHUT_RDWR)
                client.close()
                sys.exit()

            except:
                print('ERROR 204: connection lost!')
                #client.shutdown(socket.SHUT_RDWR)
                client.close()
                sys.exit()


    def write():
        try:
            while True:
                #message = getpass.getpass()
                message = input()
                print('''\033[A                                                            \033[A''')
                if message == 'exit':
                    print('exiting.')
                    client.shutdown(socket.SHUT_RDWR)
                    client.close()
                    sys.exit()
                else:
                    pass
                message = f'{userName}: {message}'
                message = message.encode()
                message = encrypt_data(message)
                client.send(message)

        except Exception as e:
            print('ERROR:', e)

        except KeyboardInterrupt:
            client.shutdown(socket.SHUT_RDWR)
            client.close()
            sys.exit()


    receive_thread = threading.Thread(target=receive)
            #print('recieve-thread started')
    receive_thread.start()

    write_thread = threading.Thread(target=write)
            #print('write-thread started')
    write_thread.start()

try:
    main()

except KeyboardInterrupt:
    sys.exit()

except Exception as e:
    sys.exit(e)
