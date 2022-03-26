import tkinter as tk
from tkinter import *
from tkinter import ttk

from picamera import PiCamera
from time import sleep

import datetime

import os
import io

LARGE_FONT = ("Verdana",14)


class AppUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        tk.Tk.attributes(self,'-fullscreen',True)
        tk.Tk.wm_title(self,'Translator')

        window = tk.Frame(self)
        window.pack(side="top", fill="both", expand=True)
        window.grid_rowconfigure(0, weight=1,uniform=1)
        window.grid_columnconfigure(0, weight=1,uniform=1)

        self.frames = {}

        frame = PageStructure(window,self)

        self.frames[PageStructure] = frame

        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(PageStructure)

    def show_frame(self,cont):
        frame = self.frames[cont]
        frame.tkraise()

class PageStructure(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.state = True
        self.camera = PiCamera()

        #Camera Setup - re-initialise on page load
        self.camera.resolution = (1200,1200)
        self.camera.framerate = 30

        self.configure(bg="grey70")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Main functional area
        leftFrame = Frame(self,width=(screen_width/4*3 - 20), height=screen_height,bg="red")
        leftFrame.pack(side=LEFT,padx=5,pady=10)

        # Button Area
        rightFrame = Frame(self,width=(screen_width/4), height=screen_height,bg="blue")
        rightFrame.pack(side=RIGHT,padx=5,pady=10)

        rightFrame.grid_propagate(False)
        leftFrame.grid_propagate(False)

        photo = PhotoImage(file = "button.png")

        history = Button(rightFrame,text="History",width=100,height=100,
                         command = lambda : self.photoPreview())
        history.grid(row=0,column=0,padx=5,pady=4)
        #history.image = photo
        #history.configure(width=250,height=250)


        language = Button(rightFrame,text="Change Language",width=100,height=100,
                          command = lambda : print("Change Language"))
        #language.image = photo
        language.grid(row=1,column=0,padx=5,pady=4)

        takePhoto = Button(rightFrame,text="Take photo",width=100,height=100,
                           command = lambda : self.takePhoto())
        #takePhoto.image = photo
        takePhoto.grid(row=2,column=0,padx=5,pady=4)
        # print(takePhoto.winfo_width())

        closeApp = Button(rightFrame,text="Quit",width=100,height=100,
                          command= lambda : self.exitProgram())
        #closeApp.image = photo
        closeApp.grid(row=3,column=0,padx=5,pady=4)

        buttonList = [history,language,takePhoto,closeApp]
        counter = 0
        for x in buttonList:
            rightFrame.grid_columnconfigure(counter,weight=1)
            rightFrame.grid_rowconfigure(counter,weight=1)
            counter += 1


    def exitProgram(self):
        self.destroy()
        exit()

    #Preview Method needed to display the camera - overlaps 'leftFrame' as picamera has higher priority for display
    def photoPreview(self):
        # return
        if self.state:
            print("on")
            self.camera.start_preview(fullscreen=False,window=(5,10,580,580))
        else:
            print("off")
            self.camera.stop_preview()
        self.state = not self.state

    def takePhoto(self):
        # Takes a photo the moment the button is pressed
        # Stores it in format : dd-mm-yyyy-HH-MM-SS.jpg
        date = datetime.datetime.now()
        file_ver = str(date.strftime("%d") + "-" + date.strftime("%m") + "-" + date.strftime("%Y") + "-" + date.strftime("%H") + "-" + date.strftime("%M") + "-" + date.strftime("%S"))
        file_ver = "../images/"+ file_ver + ".jpg"
        self.camera.capture(file_ver)



app = AppUI()
app.mainloop()
