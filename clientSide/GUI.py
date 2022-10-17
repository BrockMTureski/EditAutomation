from PIL import ImageTk as itk
from tkinter import *

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
    instruction.grid(row=0,column=0)
    inputFolder= Label(top,text="Input Path",fg="white",bg=color)
    inputFolder.grid(row=0,column=1)
    outputFolder= Label(top,text="Output Path",fg="white",bg=color)
    outputFolder.grid(row=0,column=2)
    sensitivity= Label(top,text="Sensitivity (0.1-1)",fg="white",bg=color)
    sensitivity.grid(row=0,column=3)
    defaultIn= Label(top,text="Default Input Path= "+settings.inputDir,fg="white",bg=color)
    defaultIn.grid(row=0,column=4)
    defaultOut= Label(top,text="Default Input Path= "+settings.outputDir,fg="white",bg=color)
    defaultOut.grid(row=0,column=5)

    e1 = Entry(top,width=30)
    e1.grid(row=2,column=1)
    e2 = Entry(top,width=30)
    e2.grid(row=2,column=2)
    e3 = Entry(top,width=30)
    e3.grid(row=2,column=3)

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