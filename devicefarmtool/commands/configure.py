import os
import configparser
from ..sysinfo import *

class configure:

    options = [
        '--config',
    ]
    global os_name
    global current_user
    global user_home_dir

    def __init__(self,options):
        self.checkOption(options)
        self.inputOptions = options
        self.setOptionVal()
        self.execute()

    def checkOption(self,options):
        if type(options) == dict:
            for option in options:
                if option not in self.options:
                    raise IOError('Invalid Option is provided with configure command.')
        else:
            raise RuntimeError('Tool not able to find options')


    def setConfigKeyVal(self):
        keyValPair = {}
        count = 0
        for pair in self.inputOptions['--config']:
            if pair.find('=') != -1:
                keyValPair['key'+str(count)] = pair[0:pair.find('=')]
                keyValPair['val'+str(count)] = pair[pair.find('=')+1:]
                count += 1
        self.inputOptions['--config'] = keyValPair


    def setOptionVal(self):
        if  '--config' in self.inputOptions.keys():
            self.setConfigKeyVal()

    def execute(self):
        for option in self.options:
            if option in self.inputOptions.keys():
                self.excuteConfig()

    def excuteConfig(self):
        config = configparser.ConfigParser()
        if os.path.exists(getIniFile()) == True:
            config.read(getIniFile())
            if 'aws' not in config.sections():
                config['aws'] = {}
        else:
            config['aws'] = {}
        for i in range(len(self.inputOptions['--config'])):
            if 'key'+str(i) in self.inputOptions['--config'].keys():
                if 'val'+str(i) in self.inputOptions['--config'].keys():
                    config['aws'].update({self.inputOptions['--config']['key'+str(i)]:self.inputOptions['--config']['val'+str(i)]})
        with open(getIniFile(),'w') as congfigFile:
            config.write(congfigFile)
        print('DeviceFarmTool successfully configure...')








