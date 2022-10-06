from asyncio.windows_events import NULL
from matplotlib.pyplot import plot
from pyAudioAnalysis import audioSegmentation as aS
from pyAudioAnalysis import audioBasicIO as aIO
import subprocess
import settings
from os.path import exists
import os
from pathlib import *
import ffmpeg
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


def mp4ToWav(fileName,outFileName):

    """function for converting mp4 to wav
    
    Keyword arguments:
    fileName:   name of input file (include .mp4)
    outFileName: name of output file (dont include .wav)
    Return: if file is created successfully returns path to output file. if unsuccessful returns NULL
    """


    inPath=settings.inputDir + fileName
    outFileName=outFileName+".wav"

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
        return NULL


def delFile(file):
    """function for deleting file using pathlib

    Args:
        file (path type file): file to be deleted

    Returns:
        True if deleted false if not
    """

    file.unlink()
    
    if exists(file):
        print("Error deleting: " + str(file) + "\n")
        return False
    else:
        print(str(file) + " deleted successfully.\n")
        return True


def analyzeWavFile(file):

    """takes in file path for .wav and analyzes parts to keep

    Args:
        file: path to .wav file to analyze

    Returns:
        matrix of clip times
    """

    [Fs,x] = aIO.read_audio_file(file)
    segments=aS.silence_removal(x,Fs,0.020,0.020,smooth_window=1.0,weight=.3,plot=False)
    return segments


def subclip(mp4FileName,timeMatrix):
    """takes in mp4 and returns subclips based on matrix of times

    Args:
        mp4FileName (string): name of input file in input folder
        timeMatrix (matrix): matrix of times to subclip

    Returns:
        _type_: _description_
    """

    mp4Path=settings.inputDir + mp4FileName
    
    outFileRoot=mp4FileName.split(".")
    outFileRoot=outFileRoot[0]
    
    newDir=settings.outputDir+outFileRoot
    os.mkdir(newDir)

    f=1
    for i in timeMatrix:
        starttime=i[0]
        endtime=i[1]
        temp_target=settings.outputDir + outFileRoot+str(f) + ".mp4"
        ffmpeg_extract_subclip(mp4Path, starttime, endtime, targetname=temp_target)

    return 0


def main(delInput=True,)