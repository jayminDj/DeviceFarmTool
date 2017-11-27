import os
from .sysinfo import (
    os_name,
    os_release,
    hostname,
    user_home_dir,
    current_user,
    getLocalDir
)
from .commandparser import commandParser

class utility:

    local_dir = ''
    global os_name
    global os_release
    global current_user
    global user_home_dir
    global hostname

    def __init__(self,commnads,options):
        self.commands = commnads
        self.options = options
        self.setLocalDir()
        self.parseCommands(commnads,options)

    def setLocalDir(self):
        self.local_dir = getLocalDir()
        if not os.path.exists(self.local_dir):
            try:
                os.makedirs(self.local_dir)
            except OSError as exception:
                raise


    def parseCommands(self,command,option):
        data = commandParser(command[0],option)



