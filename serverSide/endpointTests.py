import json
import requests
import pytest
import shlex
import modules
import os
import shutil
import zipfile

BASE = "http://127.0.0.1:5000/"

#blackbox endpoint tests

def test():
    #clear output dir
    r = requests.get(BASE+'clear-output')
    t=modules.splitJsonResp(r.text)
    print(t)
    if t == "Output folder cleared.":
        assert True
    else:
        assert False


def test1():
    #clear input dir
    r = requests.get(BASE+'clear-input')
    t=modules.splitJsonResp(r.text)
    print(t)
    if t == "Input folder cleared.":
        assert True
    else:
        assert False


def test2():
    #test show endpoint on empty dir
    r = requests.get(BASE+'show-input')
    print(r.text)
    t=modules.splitJsonResp(r.text)
    
    if t == "Input folder is empty.":
        assert True
    else:
        assert False


def test3():
    #test upload endpoint w single file upload
    file = {'file': open('C:\\Users\\Brock\\Desktop\\editAutomation\\serverSide\\coolvid.mp4',mode='rb')}
    r = requests.post(BASE+'upload', files=file)
    print(modules.splitJsonResp(r.text))
    if modules.splitJsonResp(r.text) == "File successfully uploaded":
        assert True
    else:
        assert False


def test4():
    #test show endpoint on directory with files
    r = requests.get(BASE+'show-input')
    print(r.text)
    t=modules.splitJsonResp(r.text)
    
    if t == "coolvid.mp4":
        assert True
    else:
        assert False


def test69():
    #testing run function
    r=requests.get(BASE+'run/0.5')
    t=modules.splitJsonResp(r.text)
    if t == "Video automation complete. Download available.":
        assert True
    else: 
        assert False


def test7():
    #test for file download
    r=requests.get(BASE+'download')
    fd = open('EditedFiles.zip','wb')
    fd.write(r.content)
    fd.close()
    if os.path.exists("C:\\Users\\Brock\\Desktop\\editAutomation\\serverSide\\EditedFiles.zip"):
        assert True
    else:
        assert False


def test5():
    #clear input dir
    r = requests.get(BASE+'clear-input')
    t=modules.splitJsonResp(r.text)
    print(t)
    if t == "Input folder cleared.":
        assert True
    else:
        assert False


#def test6():
    #test upload endpoint w multiple file upload
    #file = {'file1': open('C:\\Users\\Brock\\Desktop\\editAutomation\\serverSide\\coolvid.mp4',mode='rb'),
     #'file2': open('C:\\Users\\Brock\\Desktop\\editAutomation\\serverSide\\test1.mp4',mode='rb')}
    #r = requests.post(BASE+'upload', files=file)
    #print(modules.splitJsonResp(r.text))
    #if modules.splitJsonResp(r.text) == "File successfully uploaded":
        #assert True
    #else:
        #assert True


r=requests.get(BASE+'download')
fd = open('EditedFiles.zip','wb')
fd.write(r.content)
fd.close()