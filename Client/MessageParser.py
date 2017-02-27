import json


class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'message': self.parse_message,
            'history': self.parse_history
            # More key:values pairs are needed

        }

    def parse(self, payload):
        payload = json.loads(payload)

        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            raise ValueError("Response not valid")
            # Response not valid

    def parse_error(self, payload):
        pass

    def parse_info(self, payload):
        pass

    def parse_message(self, payload):
        pass

    def parse_history(self, payload):
        pass
    # Include more methods for handling the different responses...


if __name__ == '__main__':
    """
    This is the main method

    No alterations are necessary
    """
    myParser = MessageParser()

    print(myParser.parse(payload="dsdsd"))
