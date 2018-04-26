#!/usr/bin/python

import argparse
import socket
import sys
import ssl
import hashlib
import uuid
import os
import datetime
import time
import threading

MAX_SIZE = 1024

##########
## TODO: Make a lot of my functions more
## fault tolerant. I currently do no null
## checks which could be a huge issue is
## files doesn't exist or they are empty
##########



## Makes the connection a thread so that
## multiple users are able to connect at
## one time.
##########
class ClientThread(threading.Thread):
    def __init__(self,connection_stream):
        threading.Thread.__init__(self)
        self.connection_stream = connection_stream
    def run(self):
        try:
            authenticate(self.connection_stream)
            deal_with_msg(self.connection_stream)

        finally:
            self.connection_stream.shutdown(socket.SHUT_RDWR)
            self.connection_stream.close()

#lock
lock = threading.Lock()

## This might be combined with findGroup at some point
## returns true is a given user name is in users.txt and false
## otherwise.
##########
def findUser(name):
    with open("users.txt", "r") as usrFile:
        for line in usrFile:
            line = line.split(" : ")
            if line[0].lower() == name.lower():
                return True
            else:
                continue
        return False;

## Returns true is a given group name is in boards.txt and false
## otherwise.
##########
def findGroup(name):
    with open("boards.txt", "r") as bFile:
        for line in bFile:
            if line.lower().strip() == name.lower().strip():
                return True
            else:
                continue
        return False;

## Returns true if a given hashed and salted password is
## associated with a given user name and false otherwise.
##########
def checkPassword(name, pw):
    with open("users.txt", "r") as usrFile:
        for line in usrFile:
            line = line.split(" : ")
            if line[0].lower() == name.lower():
                if line[1] == hashPW(pw, line[2]):
                    return True
                else:
                    return False
            else:
                continue
        return False;

## Takes a user name, a hashed and salted password
## and the salt used as args and appends them to the
## users.txt file.
##########
def addUser(name, hash, salt):
    lock.acquire()
    with open("users.txt", "a") as usrFile:
        name = name.lower().strip()
        usrFile.write("\n" + name + " : " + hash + " : " + salt)
    lock.release()
## Takes a password and salt combines them and
## does a sha 512 hash on them. Returns said hash.
##########
def hashPW(pw, salt):
    return hashlib.sha512((pw.strip() + salt).encode('utf-8')).hexdigest()

## Just goes through the boards.txt file and spits out
## a string with all the extant boards.
##########
def displayBoards():
    with open("boards.txt", "r+") as boardFile:
        toReturn = "\n"
        for line in boardFile:
            toReturn += line
        return toReturn

## If the user entered "get ...." it splits up
## their input and looks a group name that's the same
## as whatever the user typed after get.
## I Think I still have some work to do on this function
## and the post function to make the inputs more consistent.
##########
def getPosts(message):
    message = message.split(" ")
    if len(message) == 1:
        #they didn't put in a group or they formatted their input poorly
        return "Sorry, I don't understand that input"
    else:
        if findGroup(message[1]):
            toReturn = "\n"
            group = message[1].lower().strip() + ".txt"
            with open(group, "r") as posts:
                for line in posts:
                    toReturn += line

            if len(toReturn) == 0:
                return "Empty"
            else:
                return toReturn
        else:
            return "Sorry, that group doesn't seem to exist"

## Takes in a message that starts with post,
## it then looks at the next word and checks if there
## is a group with that name. If yes, it takes the rest
## of the user input, timestamps it, and posts it to
## that given group. If it doesn't find the group it
## just apologized and moves on.
##########
def postComment(message):
    message = message.split(" ")
    if len(message) < 2:
        #they didn't put in a group or they formatted their input poorly
        return "Sorry, I don't understand that input"
    else:
        if findGroup(message[1]):
            toPost = " ".join(message[2:])
            group = message[1].lower().strip() + ".txt"
            lock.acquire()
            with open(group, "a") as posts:
                timeStamp = time.time()
                timeStamp = datetime.datetime.fromtimestamp(timeStamp).strftime('%Y-%m-%d %H:%M:%S')
                posts.write(timeStamp + " : " +  toPost + "\n")
            lock.release()
            return "Posted!"
        else:
            return "Sorry, that group doesn't seem to exist"

## TODO: Make this fucking thing.
def addGroup(message):
    pass

## As soon as a connection is made with the client
## authenticate() is run which will start by asking for
## a user name. After that it looks for that user name in
## the users.txt file. If found it asks for a password which
## it then salts and hashes and checks it against the hash
## in the users.txt file. If they match sends back a success
## message. If the user isn't found it just for a password
## and adds them as a new user.
##########
def authenticate(connection_stream):
    retry = False
    while True:
        if not retry:
            connection_stream.send(("Please enter your username: ").encode('utf-8'))
        else:
            connection_stream.send(("Sorry, wrong password. Try Again.\nPlease enter your username: ").encode('utf-8'))
        username = connection_stream.read(MAX_SIZE).decode()
        if findUser(username):
            connection_stream.send(("Please enter your password: ").encode('utf-8'))
            password = connection_stream.read(MAX_SIZE).decode()
            print(password)
            if checkPassword(username, password):
                connection_stream.send(("Success!").encode('utf-8'))
                return username
            else:
                retry = True
                continue
        else:
            connection_stream.send(("New User will be created with the name {}, enter your password: ").format(username).encode('utf-8'))
            password = connection_stream.read(MAX_SIZE).decode()
            print(password)
            salt = uuid.uuid4().hex
            password = hashPW(password, salt)
            addUser(username, password, salt)
            connection_stream.send(("Success! You were added as a new User.").encode('utf-8'))
            return username
## I hate the name of this function. I'm going to change it at
## some point. Bascially the main loop of the message board
## onces some one is authenticated it allows them to: get
## the messages from a given group, post a message to a group,
## list the groups, and *TODO* add a group. The user can
## end a session whenever they like with the end command.
##########
def deal_with_msg(connection_stream):
    # waiting for message
    while True:
        message = connection_stream.read(MAX_SIZE).decode()
        print ('Server: received {}'.format(message))
        if(message == "list"):
            connection_stream.send((displayBoards()).encode('utf-8'))
        elif(message.startswith("get".lower().strip())):
            connection_stream.send(getPosts(message).encode('utf-8'))
        elif(message.startswith("post".lower().strip())):
            connection_stream.send(postComment(message).encode('utf-8'))
        elif(message.startswith("add".lower().strip())):
            pass
        elif(message.startswith("end".lower().strip())):
            break
        #lets error check this later in case no get/post/end
        else:
            break
## TODO: Make this mutli threaded.
## Set up of ssl socket and waits for a client connection.
##########
def main():
    # parse arguments to the client
    parser = argparse.ArgumentParser(description='Computer Security Server')
    parser.add_argument('-l','--local', help='local port', required=True)

    args = vars(parser.parse_args())
    #refers to local port
    local_port =  int(args['local'])

    # Create a TCP/IP socket and wrap it
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port, '' can be address later for now it is local host
    server_sock.bind(('', local_port))
    threads = []

    # Listen for incoming connections listen() puts the socket into server mode, accept waits for incoming connections

    while True:
        server_sock.listen(10)
        print ("Waiting for connection from client")
        connection, client_address = server_sock.accept()
        print ('Client connected: (IP : Port) {}'.format(client_address))
        connection_stream = ssl.wrap_socket(connection, server_side = True, certfile = "domain.crt", keyfile = "domain.key")
        new_thread = ClientThread(connection_stream)
        new_thread.start()
        threads.append(new_thread)

    for t in threads:
        t.join()

# this gives a main function in Python
if __name__ == "__main__":
    main()
