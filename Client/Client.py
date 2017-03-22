# -*- coding: utf-8 -*-
import socket
import json
import re

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

        self.run()

    def run(self):

        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))

        print("connected")

        self.message_receiver = MessageReceiver(self, self.connection)
        self.message_receiver.start()

        print('   Urban Robot Advanced Chat System')
        print('   --------------------------------')
        self.help()

        while True:
            request = input('').lower().lstrip().rstrip()

            if re.search('^login((  *[^\s]+)|((\s)*(?!.)))', request):
                self.login(request[6:])
            elif request == 'logout':
                self.logout()
            elif re.search('^msg((  *[^\s]+)|((\s)*(?!.)))', request):
                self.msg(request[4:])
            elif request == 'names':
                self.names()
            elif request == 'help':
                self.help()
            else:
                # TODO : Do something here
                print('Invalid command')
                self.help()

    def disconnect(self):
        # TODO: Handle disconnection
        self.connection.close()

    def receive_message(self, message):
        # TODO: Handle incoming message
        parser = MessageParser()
        parsed_message = MessageParser.parse(parser, message)
        # print("--------- Received: " + str(message) + " ---------")
        print(parsed_message)

    def login(self, username):
        if username:  # Reasoning:    (message = '') would be asserted as False
            self.send_request('login', username)
        else:
            un = input('Enter username >> ')
            self.login(un)

    def msg(self, message):
        if message:
            self.send_request('msg', message)
        else:
            ms = input('Enter message >> ')
            self.msg(ms)

    def logout(self):
        self.send_request('logout', '')

    def names(self):
        self.send_request('names', '')

    def help(self):
        self.send_request('help', '')

    def send_request(self, request, content):
        response = {
            'request': request,
            'content': content
        }
        self.connection.sendall(json.dumps(response).encode('ascii'))


if __name__ == '__main__':

    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """

    client = Client('localhost', 9998)  # TODO: Allow switching between servers
