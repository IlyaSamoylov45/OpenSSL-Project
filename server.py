#!/usr/bin/python

import argparse
import socket
import sys

MAX_SIZE = (1024)

def main():
    # parse arguments to the client
    parser = argparse.ArgumentParser(description='Computer Security Server')
    parser.add_argument('-l','--local', help='local port', required=True)

    args = vars(parser.parse_args())
    #refers to local port
    local_port =  int(args['local'])

    # Create a TCP/IP socket
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port, '' can be address later for now it is local host
    server_sock.bind(('', local_port))

    # Listen for incoming connections listen() puts the socket into server mode, accept waits for incoming connections
    server_sock.listen(1)
    # waiting for message
    while True:
        print ("{}, waiting for connection from client".format(sys.stderr))
        connection, client_address = server_sock.accept()
        try:
            print ('{}, client connected: {}'.format(sys.stderr, client_address))
            while True:
                message = connection.recv(MAX_SIZE)
                print ('{}, recieved {}'.format(sys.stderr, message))
                if message:
                    connection.sendall(message)
                else:
                    break
        finally:
            connection.close()

# this gives a main function in Python
if __name__ == "__main__":
    main()
