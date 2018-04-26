#!/usr/bin/python

import argparse
import sys
import socket
import ssl

MAX_SIZE = 1024

def auth(sslSock):
    data = sslSock.read(MAX_SIZE).decode()
    
    print ("{}, recieved message {}".format(sys.stderr, data))

    message = input("Reply: ")

    sslSock.write(message.encode('utf-8'))

    while message != "end" :
        data = sslSock.read(MAX_SIZE).decode()
        print ("{}, recieved message {}".format(sys.stderr, data)) 
        if data == "Success! You were added as a new User." or data == "Success!":
            break
        message = input("Reply: ")
        print ("{}, sending message: {}".format(sys.stderr, message))
        sslSock.write(message.encode('utf-8'))

    msgBoard(sslSock)


def msgBoard(sslSock):
    print ("List of boards:")
    sslSock.write(("listB").encode('utf-8'))
    data = sslSock.read(MAX_SIZE).decode()
    print ("{}, recieved message {}".format(sys.stderr, data))
    
    message = input("Reply: ")

    sslSock.write(message.encode('utf-8'))

    while message != "end" :
        data = sslSock.read(MAX_SIZE).decode()
        print ("{}, recieved message {}".format(sys.stderr, data))
        message = input("Reply: ")
        print ("{}, sending message: {}".format(sys.stderr, message))
        sslSock.write(message.encode('utf-8'))

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
    ssl_client_sock = ssl.wrap_socket(client_socket, ca_certs = "domain.crt", cert_reqs = ssl.CERT_REQUIRED)
    ssl_client_sock.connect(server_addr)

    auth(ssl_client_sock)
    

    ssl_client_sock.close()

if __name__ == "__main__":
    main()