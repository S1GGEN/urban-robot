# -*- coding: utf-8 -*-
import socket
import json
from typing import re
import atexit
import time
import sys

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

        #print("connected")

        self.message_receiver = MessageReceiver(self, self.connection)
        self.message_receiver.start()

        print(bcolors.HEADER + bcolors.BOLD + ' Urban Robot Advanced Chat System')
        print(' --------------------------------' + bcolors.ENDC)
        self.help()

        while True:
            time.sleep(0.01)

            if self.program_die:
                break

            command = input('\t>>> ')

            splitted_command = command.lower().split()
            stripped_command = command.lower().strip()
            lstripped_command = command.lower().lstrip()

            no_content_commands=['logout', 'help', 'names']

            if len(splitted_command) > 1:
                if splitted_command[0] == 'login':
                    self.send_request('login', splitted_command[1])
                elif lstripped_command[:3] == 'msg':
                    self.send_request('msg', lstripped_command[3:])
                else:
                    print(bcolors.FAIL + '\tInvalid command!' + bcolors.ENDC)
            else:
                if stripped_command in no_content_commands:
                    self.send_request(command.lower(), '')
                elif stripped_command == 'msg':
                    message = input('\tEnter message >> ')
                    self.send_request('msg', message)
                elif stripped_command == 'login':
                    username = input('\tEnter username >> ')
                    self.send_request('login', username)
                else:
                    print(bcolors.FAIL + '\tInvalid command!' + bcolors.ENDC)


    def disconnect(self):
        # TODO: Handle disconnection
        self.connection.close()

    def receive_message(self, message):
        parser = MessageParser()
        parsed_message = MessageParser.parse(parser, message)
        # print("--------- Received: " + str(message) + " ---------")
        print('\t' + parsed_message)

    def help(self):
        self.send_request('help', '')

    def send_request(self, request, content):
        response = {
            'request': request,
            'content': content
        }
        self.connection.sendall(json.dumps(response).encode('utf-8'))


if __name__ == '__main__':


    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """

    client = Client('localhost', 9999)  # TODO: Allow switching between servers

