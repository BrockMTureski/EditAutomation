from matplotlib.pyplot import plot
from pyAudioAnalysis import audioSegmentation as aS
from pyAudioAnalysis import audioBasicIO as aIO
import app as app
from os.path import exists
import os
from pathlib import *
import ffmpeg
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from csv import writer
import zipfile




def mp4ToWav(fileName,outFileName):

    """function for converting mp4 to wav
    
    Keyword arguments:
    fileName:   name of input file (include .mp4)
    outFileName: name of output file (dont include .wav)
    Return: if file is created successfully returns path to output file. if unsuccessful returns NULL
    """

    inPath=app.inputDir + fileName
    outFileName=outFileName + ".wav"

    input=ffmpeg.input(inPath)
    audio=input.audio
    stream=ffmpeg.output(audio,outFileName)
    ffmpeg.run(stream)


    outPath=str(Path(os.getcwd())) + '/' + outFileName

    print(outPath+"\n")

    outPath=Path(outPath)

    if exists(outPath):
        print(".wav created successfully.\n")
        return outPath

    else:
        print("ERROR:.wav not created successfully.\n")
        return None


def delFile(file):
    """function for deleting file using pathlib

    Args:
        file (path type file): file to be deleted

    Returns:
        True if deleted false if not
    """
    file=str(file)
    os.unlink(file)
    
    if exists(file):
        print("Error deleting: " + str(file))
        return False
    if exists(file) is False:
        print(file + " deleted successfully.")
        return True


def analyzeWavFile(file,sensitivity):

    """takes in file path for .wav and analyzes parts to keep

    Args:
        file: path to .wav file to analyze

    Returns:
        matrix of clip times
    """

    [Fs,x] = aIO.read_audio_file(file)
    segments = aS.silence_removal(x,Fs,0.020,0.020,smooth_window=1.0,weight=sensitivity,plot=False)
    return segments


def subclip(mp4FileName,timeMatrix):
    """takes in mp4 and returns subclips based on matrix of times

    Args:
        mp4FileName (string): name of input file in input folder
        timeMatrix (matrix): matrix of times to subclip

    """

    mp4Path=app.inputDir + mp4FileName
    
    outFileRoot=mp4FileName.split(".")
    outFileRoot=outFileRoot[0]

    f=1
    for i in timeMatrix:
        #create subclip
        starttime=i[0]
        endtime=i[1]
        temp_target=app.outputDir+outFileRoot+ str(f) + ".mp4"
        ffmpeg_extract_subclip(mp4Path, starttime, endtime, targetname=temp_target)
        print(outFileRoot+str(f)+".mp4 created successfully")
        #increment loop counter
        f=f+1
        #append changes made to end of log
        csvInput=[outFileRoot,starttime,endtime]
        with open("log.csv","a+") as log:
            logWrite=writer(log)
            logWrite.writerow(csvInput)

    return 0


def allowed_file(filename):
    ALLOWED_FILE_TYPE=set(['mp4'])
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_FILE_TYPE


def showDir(path):
    """lists directory, takes in folder path."""
    files=os.listdir(path)
    print(files)
    ret=""
    if not files:
        return "Input folder is empty."
    else:
        for file in files:
            #temp=str(file).split("\'")[1]
            ret=ret+str(file)+", "
    ret=ret[:-2]
    return ret


def clearDir(inputPath):
    """Clear directory of all files. 
    
    Takes path as input
    
    returns True if empy, else returns false."""
    directoryList=os.listdir(inputPath)
    newPath=str(Path(inputPath)) + "//"
    for inFile in directoryList:
        temp=newPath+str(inFile)
        print(temp)
        delFile(temp)
    print(os.listdir(inputPath))
    if not os.listdir(inputPath):
        return True
    else:
        return False


def zip(path,zipfolder):
    wdRestore=os.getcwd()
    os.chdir(path)
    for files in os.listdir(path):
        print(files)
        zipfolder.write(files)
    os.chdir(wdRestore)


def splitJsonResp(s):
    """splits a json http response into just the message, used for testing."""
    print(s)
    split= s.split('\"')
    split=split[3]
    return split


def unzip(pathOfZip,outputPath):
    with zipfile.ZipFile(pathOfZip,'r') as zip:
        zip.extractall(outputPath)
        return 0


def main(sensitivity, delInput=False,inputPath="",outputPath=""):

    if inputPath=="":
        inputPath=app.inputDir
    
    if outputPath=="":
        outputPath=app.outputDir
    
    directoryList=os.listdir(inputPath)
    print(directoryList)

    for inFile in directoryList:

        outRoot=inFile[:len(inFile)-4]
        outPath=mp4ToWav(inFile,outRoot)
        clip_segments=analyzeWavFile(outPath,float(sensitivity))
        delFile(outPath)
        subclip(inFile,clip_segments)
        delFile(inputPath + inFile)

    print("video automation is complete :).")
    return 0