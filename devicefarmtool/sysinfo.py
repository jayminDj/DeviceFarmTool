import os
import sys
import platform
import getpass
import socket

os_name = platform.system()
os_release = platform.release()
current_user = getpass.getuser()
user_home_dir = os.path.expanduser('~')
hostname = socket.gethostname()
inifile = 'devicefarm.ini'
AWS_ACCESS_KEY = 'AWS_ACCESS_KEY'
AWS_SECRET_ACCESS_KEY = 'AWS_SECRET_ACCESS_KEY'
AWS_REGION = 'region'

def getLocalDir():
    global os_name
    global user_home_dir

    if os_name == 'Linux':
        return user_home_dir + r'/.aws'
    elif os_name == 'Windows':
        return user_home_dir + r'\.aws'
    else:
        return ''

def getIniFile():
    global os_name
    global user_home_dir
    global inifile
    local_dir = getLocalDir()
    if os_name == 'Linux':
        return local_dir + r'/' + inifile
    elif os_name == 'Windows':
        return local_dir + '\\' + inifile
    else:
        return ''





