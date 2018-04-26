#!/usr/bin/python

import argparse
import socket
import sys
import ssl

MAX_SIZE = 1024

def authenticate(connection_stream):
    #get username and password this is where we will deal with username an password
    username = connection_stream.read(MAX_SIZE).decode()
    password = connection_stream.read(MAX_SIZE).decode()
    return

def deal_with_msg(connection_stream):
        # waiting for message
        while True:
            message = connection_stream.read(MAX_SIZE).decode()
            print ('{}, recieved {}'.format(sys.stderr, message))

            #temporary until i figure out how to close connection without closing cmd
            if message == "shutdown":
                break

            if not message:
                break
            else:
                print ('{}, sending {}'.format(sys.stderr, message))
                connection_stream.sendall(message.encode())
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

    # Listen for incoming connections listen() puts the socket into server mode, accept waits for incoming connections
    server_sock.listen(1)
    print ("{}, waiting for connection from client".format(sys.stderr))
    connection, client_address = server_sock.accept()
    print ('{}, client connected: {}'.format(sys.stderr, client_address))
    connection_stream = ssl.wrap_socket(connection, server_side = True, certfile = "domain.crt", keyfile = "domain.key")

    try:
        authenticate(connection_stream)
        deal_with_msg(connection_stream)
    finally:
        connection_stream.shutdown(socket.SHUT_RDWR)
        connection_stream.close()
# this gives a main function in Python
if __name__ == "__main__":
    main()