from matplotlib.pyplot import plot
from pyAudioAnalysis import audioSegmentation as aS
from pyAudioAnalysis import audioBasicIO as aIO
import settings
from os.path import exists
import os
from pathlib import *
import ffmpeg
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from csv import writer
from PIL import ImageTk as itk
from tkinter import *


def mp4ToWav(fileName,outFileName):

    """function for converting mp4 to wav
    
    Keyword arguments:
    fileName:   name of input file (include .mp4)
    outFileName: name of output file (dont include .wav)
    Return: if file is created successfully returns path to output file. if unsuccessful returns NULL
    """


    inPath=settings.inputDir + fileName
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

    file.unlink()
    
    if exists(file):
        print("Error deleting: " + str(file) + "\n")
        return False
    else:
        print(str(file) + " deleted successfully.\n")
        return True


def analyzeWavFile(file,sensitivity):

    """takes in file path for .wav and analyzes parts to keep

    Args:
        file: path to .wav file to analyze

    Returns:
        matrix of clip times
    """

    [Fs,x] = aIO.read_audio_file(file)
    segments=aS.silence_removal(x,Fs,0.020,0.020,smooth_window=1.0,weight=sensitivity,plot=False)
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
    print(newDir+" created successfully.\n")

    f=1
    for i in timeMatrix:
        #create subclip
        starttime=i[0]
        endtime=i[1]
        temp_target=settings.outputDir + outFileRoot + "/" +outFileRoot+ str(f) + ".mp4"
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


def main(sensitivity, delInput=False,inputPath="",outputPath=""):

    if inputPath=="":
        inputPath=settings.inputDir
    
    if outputPath=="":
        outputPath=settings.outputDir
    
    archivePath=str(Path(os.getcwd()))+'/archive/'
    
    directoryList=os.listdir(inputPath)
    print(directoryList)

    for inFile in directoryList:

        outRoot=inFile[:len(inFile)-4]
        outPath=mp4ToWav(inFile,outRoot)
        clip_segments=analyzeWavFile(outPath,float(sensitivity))
        delFile(outPath)
        subclip(inFile,clip_segments)

        #if delInput==False:
            #os.rename(inputPath + inFile, archivePath + inFile)
        #else:
            #delFile(inputPath + inFile)

    print("video automation is complete :).")
    return 0  


def guiInit():
    """
    gui function
    
    """
    top = Tk()

    def rgb_hack(rgb):
        return "#%02x%02x%02x" % rgb

    def move_window(event):
        top.geometry('+{0}+{1}'.format(event.x_root, event.y_root))

    def quitter(event):
        top.quit()

    color="#181818"
    barColor="#404040"
    runButtonColor="#b3b3b3"


    top.geometry("500x300+200+200")
     
    top.overrideredirect(True)
    titleBar=Frame(top,bg=barColor,relief='flat', bd=1)
    closeButtonLabel=Label(titleBar,fg="white",text='X',bg=barColor,width=5)
    window=Canvas(top,bg=color,bd=0)
    titleLabel=Label(titleBar,text="Minute Study Automations",bg=barColor,fg="white")

    minuteStudy = "minutestudy16.png"
    menuImage=itk.PhotoImage(file=minuteStudy)
    menuButton=Button(titleBar,image=menuImage,bg=barColor,fg=barColor,highlightbackground=barColor,bd=0)

    titleBar.pack(expand=1,fill=X)
    closeButtonLabel.pack(side=RIGHT)
    window.pack(expand=1,fill=BOTH)
    menuButton.pack(side=LEFT)
    titleLabel.pack(side=LEFT,padx=2)

    closeButtonLabel.bind("<Button-1>",quitter)
    titleBar.bind('<B1-Motion>',move_window)

    instruction= Label(top,text="Leave input and output fields empty for default.",fg="white",bg=color)
    instruction.place(x=15,y=45)
    inputFolder= Label(top,text="Input Path",fg="white",bg=color)
    inputFolder.place(x=30,y=70)
    outputFolder= Label(top,text="Output Path",fg="white",bg=color)
    outputFolder.place(x=30,y=110)
    sensitivity= Label(top,text="Sensitivity (0.1-1)",fg="white",bg=color)
    sensitivity.place(x=30,y=150)
    defaultIn= Label(top,text="Default Input Path= "+settings.inputDir,fg="white",bg=color)
    defaultIn.place(x=15,y=205)
    defaultOut= Label(top,text="Default Input Path= "+settings.outputDir,fg="white",bg=color)
    defaultOut.place(x=15,y=225)

    e1 = Entry(top,width=30)
    e1.place(x = 140, y = 70)
    e2 = Entry(top,width=30)
    e2.place(x = 140, y = 110)
    e3 = Entry(top,width=30)
    e3.place(x = 140, y = 150)

    run=Button(top,text="  Run  ",bg=runButtonColor,fg="black",bd=0)

    def automate(event):
        """
        Run function that takes in gui text input then runs edit automations
        """
        sens=e3.get()
        inputt=e1.get()
        out=e2.get()
        e1.destroy()
        e2.destroy()
        e3.destroy()
        instruction.destroy()
        inputFolder.destroy()
        outputFolder.destroy()
        sensitivity.destroy()
        defaultIn.destroy()
        defaultOut.destroy()
        run.destroy()
        processing=Label(top,text="processing...",fg="white",bg=color,bd=0)
        processing.place(x=200,y=125)
        temp=main(sens,inputPath=inputt,outputPath=out)
        processing.destroy()
        done=Label(top,text="Automation complete.",fg="white",bg=color,bd=0).place(x=180,y=125)

    run.place(x=450,y=149)
    run.bind("<Button-1>",automate)

    top.mainloop()