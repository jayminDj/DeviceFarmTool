import os
import sys
import boto3
import configparser
import zipfile
import requests
from .sysinfo import getIniFile,AWS_ACCESS_KEY,AWS_SECRET_ACCESS_KEY,AWS_REGION
from colorama import Fore,Style,Back


class devicefarmUtils:

    ANDROID_APP = "ANDROID_APP"
    IOS_APP = "IOS_APP"
    WEB_APP = "WEB_APP"
    EXTERNAL_DATA = "EXTERNAL_DATA"
    APPIUM_JAVA_JUNIT_TEST_PACKAGE = "APPIUM_JAVA_JUNIT_TEST_PACKAGE"
    APPIUM_JAVA_TESTNG_TEST_PACKAGE = "APPIUM_JAVA_TESTNG_TEST_PACKAGE"
    APPIUM_PYTHON_TEST_PACKAGE = "APPIUM_PYTHON_TEST_PACKAGE"
    APPIUM_WEB_JAVA_JUNIT_TEST_PACKAGE = "APPIUM_WEB_JAVA_JUNIT_TEST_PACKAGE"
    APPIUM_WEB_JAVA_TESTNG_TEST_PACKAGE = "APPIUM_WEB_JAVA_TESTNG_TEST_PACKAGE"
    APPIUM_WEB_PYTHON_TEST_PACKAGE = "APPIUM_WEB_PYTHON_TEST_PACKAGE"
    CALABASH_TEST_PACKAGE = "CALABASH_TEST_PACKAGE"
    INSTRUMENTATION_TEST_PACKAGE = "INSTRUMENTATION_TEST_PACKAGE"
    UIAUTOMATION_TEST_PACKAGE = "UIAUTOMATION_TEST_PACKAGE"
    UIAUTOMATOR_TEST_PACKAGE = "UIAUTOMATOR_TEST_PACKAGE"
    XCTEST_TEST_PACKAGE = "XCTEST_TEST_PACKAGE"
    XCTEST_UI_TEST_PACKAGE = "XCTEST_UI_TEST_PACKAGE"

    def __init__(self):
        config = configparser.ConfigParser()
        config.read(getIniFile())
        self.client = boto3.client('devicefarm',aws_access_key_id=config['aws'][AWS_ACCESS_KEY],
                              aws_secret_access_key=config['aws'][AWS_SECRET_ACCESS_KEY],
                              region_name=config['aws'][AWS_REGION])


    def getProjecList(self):
        try :
            response = self.client.list_projects()
        except Exception as Exc:
            print(Exc.args)
        return response

    def getlistUploads(self,project):
        upload_list = []
        nextToken = None
        while True:
            try:
                if nextToken == None:
                    response = self.client.list_uploads(arn=project['arn'])
                else:
                    response = self.client.list_uploads(arn=project['arn'], nextToken=nextToken)
                if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                    if len(response['uploads']) > 0:
                        for key, upload in enumerate(response['uploads']):
                            if upload['status'] == 'SUCCEEDED':
                                if upload['type'] == self.ANDROID_APP or upload['type'] == self.IOS_APP:
                                    upload_list.append(upload)
                if response['nextToken']:
                    nextToken = response['nextToken']
                    continue;
            except Exception as Exc:
                break

        return upload_list

    def createUpload(self, zipPath, project, removeList = []):
        fileInZip = zipfile.ZipFile(zipPath)
        files = fileInZip.namelist()
        uploadNames = {}
        for key,file in enumerate(files):
            if file in removeList:
                print(Fore.YELLOW + "[Info] : " + file + " is skipped , already available on deviceFarm.")
                print(Fore.RESET)
                continue
            tempName = file.split(".",-1)
            if  tempName[-1] == 'apk':
                print(Fore.YELLOW + "[Info] : Creating upload for android app..")
                print(Fore.RESET)
                response = self.client.create_upload(projectArn=project['arn'],
                                                     name=file,
                                                     type=self.ANDROID_APP,
                                                     contentType='application/octet-stream')
                if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                    print(Fore.GREEN + "[Info] : Initialized upload for android app is done.")
                    print(Fore.RESET)
                    uploadNames[self.ANDROID_APP] = {}
                    uploadNames[self.ANDROID_APP]['file'] = file
                    uploadNames[self.ANDROID_APP]['url'] = response['upload']['url']
                else:
                    print(Fore.RED + "[Error] : Creation upload for android app is fail.")
                    print(Fore.RESET)

            if tempName[-1] == 'ipa':
                print(Fore.YELLOW + "[Info] : Creating upload for ios app..")
                print(Fore.RESET)
                response = self.client.create_upload(projectArn=project['arn'],
                                                     name=file,
                                                     type=self.IOS_APP,
                                                     contentType='application/octet-stream')

                if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                    print(Fore.GREEN + "[Info] : Initialized upload for ios app is done.")
                    print(Fore.RESET)
                    uploadNames[self.IOS_APP] = {}
                    uploadNames[self.IOS_APP]['file'] = file
                    uploadNames[self.IOS_APP]['url'] = response['upload']['url']
                else:
                    print(Fore.RED + "[Error] : Creation upload for ios app is fail.")
                    print(Fore.RESET)


        self.uploadFile(zipPath,uploadNames)

    def uploadFile(self,zipPath,uploadMeta):
        if uploadMeta != {}:
            for key in uploadMeta:
                print(Fore.YELLOW + "[Info] : uploading "+ key)
                print(Fore.RESET)
                try:
                    result = requests.put(uploadMeta[key]['url'], data=upload_in_chunks(zipPath,uploadMeta[key]['file'],chunksize=10),
                                        headers={'content-type': 'application/octet-stream'})
                except ConnectionError as exce :
                    print(Fore.RED + "[Error] : Connection reset by peer.")
                    print(Fore.RESET)
                print(Fore.GREEN + "[Info] : Uploaded "+ key)
                print(Fore.RESET)



class upload_in_chunks(object):
    def __init__(self,zipPath, filename, chunksize=1 << 13):
        self.zipPath = zipPath
        self.filename = filename
        self.chunksize = chunksize
        self.readsofar = 0
        zip = zipfile.ZipFile(self.zipPath, 'r')
        self.totalsize = zip.getinfo(self.filename).file_size
        zip.close()

    def __iter__(self):
        with zipfile.ZipFile(self.zipPath, 'r') as files:
            with files.open(self.filename, 'r') as file:
                while True:
                    data = file.read(self.chunksize)
                    if not data:
                        sys.stderr.write("\n")
                        break
                    self.readsofar += len(data)
                    percent = self.readsofar * 1e2 / self.totalsize
                    sys.stderr.write("\ruploading - {percent:3.0f}%".format(percent=percent))
                    yield data

    def __len__(self):
        return self.totalsize