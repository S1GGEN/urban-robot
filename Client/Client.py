# -*- coding: utf-8 -*-
import socket
#from MessageReceiver import MessageReceiver
#from MessageParser import MessageParser


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

        self.connection.bind((host, server_port))

        # TODO: Finish init process with necessary code
        self.run()

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))
        
    def disconnect(self):
        # TODO: Handle disconnection
        self.connection.close()
        pass

    def receive_message(self, message):
        # TODO: Handle incoming message
        print(message)
        pass

    def send_payload(self, data):
        # TODO: Handle sending of a payload
        self.connection.sendall(data.encode('utf-8'))
        pass
        
    # More methods may be needed!


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)
