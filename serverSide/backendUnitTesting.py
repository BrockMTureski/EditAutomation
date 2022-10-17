import pytest
import modules
from os.path import exists


def test1():
    #test mp4 to .wav
    r = modules.mp4ToWav('test1.mp4','test')
    if r != False: 
        if exists("C:\\Users\\Brock\\Desktop\\editAutomation\\serverSide\\test.wav"):
            assert True
    else: 
        assert False


def test2():
    #test analyzeWavFile and subclip function
    r = modules.analyzeWavFile("C:\\Users\\Brock\\Desktop\\editAutomation\\serverSide\\test.wav",0.5)
    f = modules.subclip('test1.mp4', r)
    if f == 0:
        assert True
    else:
        assert False


def test3():
    #test delFile
    r = modules.delFile('C:\\Users\\Brock\\Desktop\\editAutomation\\serverSide\\input\\test1.mp4')
    assert r


def test4():
    #test clearDir
    r = modules.clearDir('C:\\Users\\Brock\\Desktop\\editAutomation\\serverSide\\output')
    assert r


def test5():
    #test delFile
    r = modules.delFile('C:\\Users\\Brock\\Desktop\\editAutomation\\serverSide\\test.wav')
    assert r