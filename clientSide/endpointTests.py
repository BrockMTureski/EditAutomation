import json
import requests
import os
import shutil
import zipfile
import clientModules

BASE = "http://127.0.0.1:5000/"

#blackbox endpoint tests

def test1():
    #clear output dir
    r = requests.get(BASE+'clear-output')
    t=clientModules.splitJsonResp(r.text)
    print(t)
    if t == "Output folder cleared.":
        assert True
    else:
        assert False


def test2():
    #clear input dir
    r = requests.get(BASE+'clear-input')
    t=clientModules.splitJsonResp(r.text)
    print(t)
    if t == "Input folder cleared.":
        assert True
    else:
        assert False


def test3():
    #test show endpoint on empty dir
    r = requests.get(BASE+'show-input')
    print(r.text)
    t=clientModules.splitJsonResp(r.text)
    
    if t == "Input folder is empty.":
        assert True
    else:
        assert False


def test4():
    #test upload endpoint w single file upload
    file = {'file': open(os.getcwd()+'\\coolvid.mp4',mode='rb')}
    r = requests.post(BASE+'upload', files=file)
    print(clientModules.splitJsonResp(r.text))
    if clientModules.splitJsonResp(r.text) == "File successfully uploaded":
        assert True
    else:
        assert False


def test5():
    #test show endpoint on directory with files
    r = requests.get(BASE+'show-input')
    t=clientModules.splitJsonResp(r.text)
    
    if t == "coolvid.mp4":
        assert True
    else:
        assert False


def test6():
    #testing run function
    r=requests.get(BASE+'run/0.5')
    t=clientModules.splitJsonResp(r.text)
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
    if os.path.exists(os.getcwd()+'\\EditedFiles.zip'):
        assert True
    else:
        assert False


def test8():
    #clear input dir
    r = requests.get(BASE+'clear-input')
    t=clientModules.splitJsonResp(r.text)
    if t == "Input folder cleared.":
        assert True
    else:
        assert False


def test9():
    #delete zip file
    r = requests.get(BASE+'delZip')
    t=clientModules.splitJsonResp(r.text)
    if t == "Download file deleted.":
        assert True
    else:
        assert False

def test10():
    #clear output dir
    r = requests.get(BASE+'clear-output')
    t=clientModules.splitJsonResp(r.text)
    if t == "Output folder cleared.":
        assert True
    else:
        assert False


r = requests.get(BASE+'test')
print(r)