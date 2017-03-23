    # -*- coding: utf-8 -*-
from threading import Thread
from MessageParser import bcolors


class MessageReceiver(Thread):
    """
    This is the message receiver class. The class inherits Thread, something that
    is necessary to make the MessageReceiver start a new thread, and it allows
    the chat client to both send and receive messages at the same time
    """

    def __init__(self, client, connection):
        """
        This method is executed when creating a new MessageReceiver object
        """
        Thread.__init__(self)
        # Flag to run thread as a daemon
        self.daemon = True
        self.client = client
        self.connection = connection

        # On message receive:
        #    client.receiveMessage(message)

    def run(self):
        while True:
            message = self.connection.recv(4096).decode()

            if not message:
                print(bcolors.FAIL + 'Lost connection to server' + bcolors.ENDC)

            self.client.receive_message(message)
