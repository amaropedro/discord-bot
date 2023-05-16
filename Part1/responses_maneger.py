"""
Pedro Amaro
"""

import random

class ResponseManeger():
    """For a given message, responds accordingly.
    Messages starting with '?' will be answered in private chat

    Parameters
    -----------
        context:
        The received message
    """

    def __init__(self, context):
        self.message = context
        self.content = str(context.content)
        self.author = str(context.author)
        self.is_private = False

    def respond(self) -> str:

        message = self.content

        if message[0] == '?':
            self.is_private = True
            message = message[1:]
        else:
            self.is_private = False

        #possible responses
        if message == '!bot':
            return self.author
        
        if message == 'ditto':
            return 'ditto'

        if message == 'hello':
            return 'HI! How are you?'
        
        if message == 'roll':
            return str(random.randint(1,6)) 
        
        if message == '!help':
            return '`let me see what I can do...`'

    async def send(self):
        try:
            response = self.respond()
            await self.message.author.send(response) if self.is_private else await self.message.channel.send(response)
        except Exception as e:
            #print(e)
            pass