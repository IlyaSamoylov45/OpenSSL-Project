# OpenSSL-Project

Joseph Klaszky
Ilya Samoylov


How to get our program running:

We never got to set default values if no args are passed so
sadly you'll have to use pass some values to get going.

To run the server use something like:

>python server.py -l 10000

The -l stands for local port so in this example 10000 will be the port that we will bind to the server. 
The program automatically sets the IP to localhost
The server will wait until a client connects (we can connect multiple clients)



To run client.py you would type something like this:

>python client.py -d localhost -p 10000 -l 14000

The -d stands for the destination IP which in our case was set to the local host.
The -p stands for the destination port which we had set to 10000 in our previous example
The -l stands for the local port which will be the port the client will be using. In our example the port is 14000 which we will bind to the client.


General design:

Client.py

Pretty standard stuff really, parse the args, use the 
args to make a connection to the server then use an SSL
wrapped socket and start communicating back and for with
the server. Once that's done the code'll enter the auth()
function and start to authenticate. It doesn't hash the
password on the client's side, but it's an ssl connection
so it should be fine in transit.

Once authenticated to the server (or a new account is made)
it enters the main loop of: take an input command, 
send to the server and display the response.


Server.py

Like the client, pretty standard startup. Take the args
set up the SSL sockets and stuff and start listening. 
When a client connects it the server creates a new thread and starts
to authenticate them. After making the thread 
the main method just goes back to listening for more
connections. 

Authentication asks for a username, if found
it it prompts for a password. After the password is
grabbed it looks up the salt used for that user
and salts and hashes the given password then checks if
the two match. If yes, then authenticate the user and move
one. If not ask user to try again. Once the user
is authenticated: print the welcome message, and the
list of available groups to post in. Then it's a
simple a loop of wait for a message, do a command
and respond.

Two things we did differently than what the description
says: I don't list the boards after every command, I 
felt that would be a bit cluttered looking so I just made
a "list" command that can be called whenever. Also, you can
add a group in two ways: posting with a group name that
doesn't exist or using the add command. 