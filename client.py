#!/usr/bin/python

import argparse
import sys
import socket

def main():
    # parse all the arguments to the client and get the arguments into local variables
    parser = argparse.ArgumentParser(description='Computer Security Client')
    parser.add_argument('-m','--message', help='Message to send', required=False)
    parser.add_argument('-d','--destinationIP', help='Destination IP Host', required=True)
    parser.add_argument('-p','--des_port', help='remote port', required=False)
    parser.add_argument('-l','--local_port', help='local port', required=True)

    args = vars(parser.parse_args())
    message = args['message']
    destinationIP = args['destinationIP']
    des_port = args['des_port']
    local_port =  args['local_port']


    # create a socket and connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_addr = (destinationIP, int(des_port))

    print ("{}, connecting to server {} port {}".format(sys.stderr ,destinationIP, des_port))
    client_socket.connect(server_addr)

    try:
        print ("{}, sending message: {}".format(sys.stderr, message))
        client_socket.sendall(message.encode('utf-8'))
        print ("{}, recieved message {}".format(sys.stderr, message))
    finally:
        client_socket.close()

# this gives a main function in Python
if __name__ == "__main__":
    main()
