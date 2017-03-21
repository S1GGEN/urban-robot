import json


class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'msg': self.parse_message,
            'history': self.parse_history
            # More key:values pairs could be needed
        }

    def parse(self, data):
        try:
            payload = json.loads(data)
        except Exception as e:
            return {
                'title': 'Nothing in response',
                'message': e
            }
        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            print(payload['response'])


    def parse_error(self, payload):
        return "ERROR: " + str(payload)

    def parse_info(self, payload):
        return "some info " + str(payload)

    def parse_message(self, payload):
        return "Sigurd said blablabla " + str(payload)

    def parse_history(self, payload):
        return "History " + str(payload)
    # Include more methods for handling the different responses...


if __name__ == '__main__':
    """
    This is the main method

    No alterations are necessary
    """
    myParser = MessageParser()

    print(myParser.parse(payload="dsdsd"))
