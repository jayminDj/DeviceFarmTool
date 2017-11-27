import os
import configparser
import zipfile
from ..sysinfo import *
from ..devicefarmUtils import devicefarmUtils
from colorama import Fore,Style,Back

class upload:

    global AWS_ACCESS_KEY
    global AWS_SECRET_ACCESS_KEY
    options = [
        '--upload-zip',
        '--project',
        '--check-version'
    ]
    project = None
    checkVersion = False
    description = "Provides uploading for IOS app, Andriod app, Web app and test pacj"


    def __init__(self,options = {}):
        self.checkOption(options)
        self.inputOptions = options
        self.setOptionVal()
        print("Checking available projects on devicefarm ....")
        projects_resposnse = devicefarmUtils().getProjecList()
        if projects_resposnse['projects'] is not None:
            projects = projects_resposnse['projects']
            if self.project == None:
                user_select = self.userInputProject(projects)
            else:
                for key, project in enumerate(projects):
                    if project['name'] == self.project:
                        user_select = key
            try:
                user_select
                if self.checkVersion == True:
                    upload_list = self.getListUploads(projects[user_select])
                    removeList = self.checkUploadVersion(upload_list,self.inputOptions['--upload-zip'])
                devicefarmUtils().createUpload(self.inputOptions['--upload-zip'],projects[user_select],removeList)
            except UnboundLocalError as Exc:
                print(Fore.RED + "[Error] : "+ self.project + " project not found on deviceFarm")
                print(Fore.RESET)
        else:
            print('[Info] : There is no project found on devicefarm.')

    def checkOption(self,options):
        if type(options) == dict:
            for option in options:
                if option not in self.options:
                    raise IOError('Invalid Option is provided with upload command.')
        else:
            raise RuntimeError('Tool not able to find options')

    def setOptionVal(self):
        if  '--upload-zip' in self.inputOptions.keys():
            self.setUploadZip()
        else:
            print("Missing option --upload-zip with upload command")
            exit(1)

        if '--project' in self.inputOptions.keys():
            self.setProject()
        if '--check-version' in self.inputOptions.keys():
            self.checkVersion = True



    def setUploadZip(self):
        if len(self.inputOptions['--upload-zip']) == 0:
            print("[Info]: Please provide zip file to upload...")
            exit(1)
        self.inputOptions['--upload-zip'] = self.inputOptions['--upload-zip'][0]
        self.isZip(self.inputOptions['--upload-zip'])


    def isZip(self,path):
        if os.path.isfile(path) == False:
            print(Fore.RED + "[Error]: File not found.")
            print(Fore.RESET + "[Info]: please provide only zip file")
            exit(1)
        if os.path.splitext(path)[-1].lower() != '.zip':
            print(Fore.RED + "[Error]: Unsupported file.")
            print(Fore.RESET + "[Info]: please provide only zip file")
            exit(1)

    def setProject(self):
        if len(self.inputOptions['--project']) == 0:
            print(Fore.YELLOW +"[Info]: Please provide projct name...")
            print(Fore.RESET)
            exit(1)
        self.project = self.inputOptions['--project'][0]


    def getListUploads(self,project):
        return devicefarmUtils().getlistUploads(project)

    def userInputProject(self,projects):
        while True:
            print(Fore.RESET + "Please provide project number for upload, Enter project number to select project")
            for key, project in enumerate(projects):
                print(str(key) + ". " + project['name'])
            user_select = input()
            try:
                user_select = int(user_select)
                if len(projects) < user_select or user_select < 0:
                    print(Fore.RED + '[ERROR] : Please provide value from available project.')
                    continue
                else:
                    return user_select
                break
            except ValueError as exc:
                print(Fore.RED + '[ERROR] : Invalid value, please provide numeric number.')


    def checkUploadVersion(self,upload_list,zipPath):
        fileInZip = zipfile.ZipFile(zipPath)
        files = fileInZip.namelist()
        removeList = []
        for uploadedFile in upload_list:
                if uploadedFile['name'] in files:
                    removeList.append(uploadedFile['name'])
        return removeList
