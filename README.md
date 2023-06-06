# mrrobot-chatroom
Chatroom from the famous Mr.Robot TV show.

# Setup

## 1.Download files

`git clone https://github.com/rysecx/mrrobot-chatroom && cd mrrobot-chatroom`

## 2.Server setup 

At first you have to change the server ip address and port to your destinations.
Then you can setup the server by running the following code:

`python3 server-setup.py`

This will create the files *key.txt*, *rooms.txt*, *validUsers.txt*, *bannedUsers.txt* and *user.txt*.
They are necessary for the message encryption and user authentification.

## 3.Client setup

To setup the client you have to change the ip address and port again. 
Then you can run the following code to setup the rest of it:

`python3 client-setup.py`

Note: Keep in mind that the encryption key and user file have to be in the same directory as the client-setup script.

You can now connect to the example server with `join fsociety`

All files are csv files. Therefore it has to be a comma between every value.

Enjoy!
