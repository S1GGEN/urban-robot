# -*- coding: utf-8 -*-
import sys
import socket
import json
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser


class Client:
    """
    This is the chat client class
    """

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """
        self.host = host
        self.server_port = server_port

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # TODO: Finish init process with necessary code

        self.run()

    def run(self):

        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))

        print("connected")

        self.message_receiver = MessageReceiver(self, self.connection)
        self.message_receiver.start()

        print('Welcome to URACS blabalabla')

        while True:

            request = input('Enter a request >> ')

            if(request == 'login'):
                self.send_payload(self.login())
            elif(request == 'logout'):
                self.send_payload(self.logout())
            elif(request == 'msg'):
                self.send_payload(self.msg())
            elif(request == 'names'):
                self.send_payload(self.names())
            elif(request == 'help'):
                self.send_payload(self.help())
            elif(request == 'error'):
                self.send_payload(self.error())
            else:
                # TODO : Do something here
                print('U suck')



    def disconnect(self):
        # TODO: Handle disconnection
        self.connection.close()

    def receive_message(self, message):
        # TODO: Handle incoming message
        parser = MessageParser()
        parsed_message = MessageParser.parse(parser, message)
        print(message)
        print(parsed_message)

    def send_payload(self, data):
        payload = json.dumps(data).encode('ascii')
        self.connection.sendall(payload)

    def login(self):
        username = input('Enter username >> ')
        return {'request' : 'login', 'content' : username}

    def logout(self):
        return{'request' : 'logout', 'content' : ''}


    def msg(self):
        message = input('Enter message >> ')
        return {'request' : 'msg', 'content' : message}

    def names(self):
        return{'request' : 'names', 'content' : ''}

    def help(self):
        return{'request' : 'help', 'content' : ''}

    def error(self):
        return{'request' : 'error', 'content' : ''}


if __name__ == '__main__':

    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9999)
