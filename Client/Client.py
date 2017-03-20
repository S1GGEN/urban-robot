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

        # self.connection.bind((self.host, self.server_port))

        # TODO: Finish init process with necessary code
        self.run()

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))

        print("connected")
        # receiver = MessageReceiver(self, self.connection)
        # self.receive_message(self)
        # self.disconnect()

    def disconnect(self):
        # TODO: Handle disconnection
        self.connection.close()
        pass

    def receive_message(self, message):
        # TODO: Handle incoming message
        parser = MessageParser()
        parsed_message = MessageParser.parse(parser, message)
        print(message)
        print(parsed_message)
        pass

    def send_payload(self, data):
        # TODO: Handle sending of a payload

        # payload = json.dumps(data).encode()
        self.connection.sendall(data)
        pass
        
    # More methods may be needed!


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)
    client.send_payload(b'csssd')
    # client.connection.sendall(b'csssd')
