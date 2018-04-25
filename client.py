#!/usr/bin/python

import argparse
import sys
import socket

MAX_SIZE = 1024

def main():
    # parse all the arguments to the client and get the arguments into local variables
    parser = argparse.ArgumentParser(description='Computer Security Client')

    parser.add_argument('-d','--destinationIP', help='Destination IP Host', required=True)
    parser.add_argument('-p','--des_port', help='destination port', required=True)
    parser.add_argument('-l','--local_port', help='local port', required=True)

    args = vars(parser.parse_args())

    destinationIP = args['destinationIP']
    des_port = args['des_port']
    local_port =  args['local_port']


    # create a socket and connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_addr = (destinationIP, int(des_port))

    print ("{}, connecting to server {} port {}".format(sys.stderr ,destinationIP, des_port))
    client_socket.connect(server_addr)

    #authenticate user
    username = input("Username: ")
    password = input("Password: ")
    print ("{}, sending username: {}, password: {}".format(sys.stderr, username, password))

    client_socket.sendall(username.encode('utf-8'))
    client_socket.sendall(password.encode('utf-8'))


    message = input("Post: ")
    while message != "logout":
        print ("{}, sending message: {}".format(sys.stderr, message))
        client_socket.sendall(message.encode('utf-8'))
        data = client_socket.recv(MAX_SIZE).decode()
        print ("{}, recieved message {}".format(sys.stderr, message))

        message = input("Post: ")

    client_socket.close()

# this gives a main function in Python
if __name__ == "__main__":
    main()
