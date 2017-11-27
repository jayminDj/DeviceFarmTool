import os
import configparser
from .sysinfo import getIniFile,AWS_ACCESS_KEY,AWS_SECRET_ACCESS_KEY
from .commands import *

class commandParser:

    exclude_commands = ['configure']
    global AWS_ACCESS_KEY
    global AWS_SECRET_ACCESS_KEY

    def __init__(self,command,options):
        self.inItCommands(command,options)

    def inItCommands(self,command,options):
        if command not in self.exclude_commands:
            self.checkConfigure()
        eval(command)(options)

    def checkConfigure(self):
        config = configparser.ConfigParser()
        config.read(getIniFile())
        if (config['aws'][AWS_ACCESS_KEY] is not None) and (config['aws'][AWS_SECRET_ACCESS_KEY] is not None):
            pass
        else:
            raise ValueError('AWS_ACCESS_KEY or AWS_SECRET_ACCESS_KEY not set, please configure deviceFarm tool.')


