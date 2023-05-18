"""
Pedro Amaro
"""

import configparser

class ConfigManeger():
    """Reads a config.ini file.

    Methods
    -----------
    is_allowed() takes current_channel and checks if it's equal to the channel_ID set in the config.ini file.
    """

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')


    def is_allowed(self, current_channel):
        default_channel = self.config['server']['channel_ID']
        return current_channel == default_channel
