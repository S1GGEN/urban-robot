import json


class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'message': self.parse_message,
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
            print("ELSE?")
            print(payload['response'])

    def parse_error(self, payload):
        # print("error")
        return str(payload['timestamp']) + ": ERROR: " + str(payload['content'])

    def parse_info(self, payload):
        # print("info")
        return str(payload['timestamp']) + ": " + str(payload['content'])

    def parse_message(self, payload):
        # print("msg")
        return str(payload['timestamp']) + ": " + payload['user'] + ": " + payload['content']

    def parse_history(self, payload):
        # print("history")
        return "History " + str(payload)
    # Include more methods for handling the different responses...


if __name__ == '__main__':
    """
    This is the main method

    No alterations are necessary
    """
    myParser = MessageParser()

    print(myParser.parse(payload="dsdsd"))
