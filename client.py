#!/usr/bin/python

import argparse
import sys
import socket
import ssl
import pprint

MAX_SIZE = 1024

##########
## So this all seems to be working, but it's
## pretty dependent on the user entering correct
## input. I'll try to make it a little more fault
## tolerant I have time.
##########

## Once a connection with the server is made we go right into
## auth(). This sticks the user in a loop until they end the session
## or the successfully make a new user account of authenticate
## to the server. Also, we're sending the password over as it
## at the moment because the ssl connection should encrypt it
## in transit. Worse case: I can just hash it before
## I send it over which would be a bit annoying, but not too hard.
##########
def auth(sslSock):
    data = sslSock.read(MAX_SIZE).decode()

    print ("Client: received message {}".format(data))

    message = input("Reply: ")

    sslSock.write(message.encode('utf-8'))

    while message != "end" :
        data = sslSock.read(MAX_SIZE).decode()
        print ("Client: received message {}".format(data))
        if data == "Success! You were added as a new User." or data == "Success!":
            break
        message = input("Reply: ")
        print ("Client: sending message: {}".format(message))
        sslSock.write(message.encode('utf-8'))

    msgBoard(sslSock)

## Main loop onces a client has been authenticated.
## Checks the client's input and if it matches a command
## that we support we run the appropriate function or
## end the session. Not fault tolerant at the moment though.
## I need to do some error checking on the input and need to
## handle being given something that we don't have a command
## for.
##########
def msgBoard(sslSock):
    print ("List of boards:")
    sslSock.write(("list").encode('utf-8'))
    data = sslSock.read(MAX_SIZE).decode()
    print ("Client: received message {}".format(data))

    message = input("Reply: ")

    sslSock.write(message.encode('utf-8'))

    while message != "end" :
        data = sslSock.read(MAX_SIZE).decode()
        print ("Client: received message {}".format(data))
        message = input("Reply: ")
        print ("Client: sending message: {}".format(message))
        sslSock.write(message.encode('utf-8'))

## Makes a connection to the server on a user supplied port.
##########
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


    # create a socket, bind to local specified port, get server destination then connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.bind(('', int(local_port)))

    server_addr = (destinationIP, int(des_port))

    print ("Client connecting to (Server IP , Port Number")
    ssl_client_sock = ssl.wrap_socket(client_socket, ca_certs = "domain.crt", cert_reqs = ssl.CERT_REQUIRED)
    ssl_client_sock.connect(server_addr)

    #information
    print(repr(ssl_client_sock.getpeername()))
    pprint.pprint(ssl_client_sock.getpeercert())
    print(pprint.pformat(ssl_client_sock.getpeercert()))

    auth(ssl_client_sock)

    ssl_client_sock.close()

if __name__ == "__main__":
    main()
