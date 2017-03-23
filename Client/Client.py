# -*- coding: utf-8 -*-
import socket
import json
import re
import time

from MessageReceiver import MessageReceiver
from MessageParser import MessageParser
from MessageParser import bcolors


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



        self.message_receiver = MessageReceiver(self, self.connection)
        self.message_receiver.start()

        print(bcolors.HEADER + bcolors.BOLD + ' Urban Robot Advanced Chat System')
        print(' --------------------------------' + bcolors.ENDC)
        print('You are now connected')
        self.help()

        while True:
            time.sleep(0.03)

            request = input('>>> ').lower().lstrip().rstrip()
            request_lower = request.lower()

            if re.search('^login((  *[^\s]+)|((\s)*(?!.)))', request_lower):
                self.login(request[6:].lstrip())
            elif request_lower == 'logout':
                self.logout()
            elif re.search('^msg((  *[^\s]+)|((\s)*(?!.)))', request_lower):
                self.msg(request[4:].lstrip())
            elif request_lower == 'names':
                self.names()
            elif request_lower == 'help':
                self.help()
            else:
                # TODO : Do something here
                print(bcolors.FAIL + '\tInvalid command!' + bcolors.ENDC)
                self.help()

    def disconnect(self):
        self.connection.close()

    def receive_message(self, message):
        parser = MessageParser()
        parsed_message = MessageParser.parse(parser, message)
        print(str(parsed_message))

    def login(self, username):
        if username:
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
        self.connection.sendall(json.dumps(response).encode('utf-8'))


if __name__ == '__main__':

    '''
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    '''

    client = Client('localhost', 9998)  # TODO: Allow switching between servers
