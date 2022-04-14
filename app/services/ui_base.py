import tkinter as tk
from tkinter import *
from tkinter import ttk

from PIL import ImageTk, Image

# from picamera import PiCamera
from time import sleep

from file_reading import ReadingFiles
from vision_translate import HistoryPage, TranslationPage

import datetime

import os
import io

LARGE_FONT = ("Verdana",14)


class AppUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        # tk.Tk.attributes(self,'-fullscreen',True)

        tk.Tk.wm_title(self,'Translator')
        self.selected_img = ""
        self.fileReading = ReadingFiles()

        window = tk.Frame(self)
        window.pack(side="top", fill="both", expand=True)
        window.grid_rowconfigure(0, weight=1,uniform=1)
        window.grid_columnconfigure(0, weight=1,uniform=1)

        self.frames = {}
        for F in (MainPage, HistoryPage, TranslationPage,SettingsPage):
            page_name = F.__name__
            frame = F(parent=window, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location the one on the top of the stacking order will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainPage")

    def recive_selected_img(self):
        return self.selected_img

    def update_select(self,img_name):
        self.selected_img = img_name
        self.update_translate()
        self.update_history()


    def update_translate(self):
        frame = self.frames["TranslationPage"]
        frame.change_img(self.selected_img)

    def update_history(self):
        frame = self.frames["HistoryPage"]
        frame.change_img(self.selected_img)

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class MainPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.state = True
        # self.camera = PiCamera()

        #Camera Setup - re-initialise on page load
        # self.camera.resolution = (1200,1200)
        # self.camera.framerate = 30
        # self.camera.rotation = 90

        self.configure(bg="grey70")
        self.controller = controller

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Main functional area
        leftFrame = Frame(self,width=(screen_width/4*3 - 400), height=screen_height-200,bg="red")
        leftFrame.pack(side=LEFT,padx=5,pady=10)

        # Button Area
        rightFrame = Frame(self,width=(screen_width/4 - 100), height=screen_height-200,bg="blue")
        rightFrame.pack(side=RIGHT,padx=5,pady=10)

        rightFrame.grid_propagate(False)
        leftFrame.grid_propagate(False)

        # photo = PhotoImage(file = "button.png")

        history_btn = Button(rightFrame,text="History",width=100,height=88, command = lambda : self.transition_func("HistoryPage"))
        history_btn.grid(row=0,column=0,padx=5,pady=4)

        settings_btn = Button(rightFrame,text="Change Language",width=100,height=88, command = lambda : self.transition_func("SettingsPage"))
        settings_btn.grid(row=1,column=0,padx=5,pady=4)

        self.view_translation_btn = Button(rightFrame,text="View Translation",width=100,height=88, command= lambda : self.transition_func("TranslationPage"))
        self.view_translation_btn.grid(row=2,column=0,padx=5,pady=4)

        takePhoto_btn = Button(rightFrame,text="Take photo",width=100,height=100, command = lambda : self.takePhoto())
        takePhoto_btn.grid(row=3,column=0,padx=5,pady=4)

        self.view_translation_btn.configure(state = DISABLED)

        buttonList = [history_btn,settings_btn,takePhoto_btn,self.view_translation_btn]
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
            # self.camera.start_preview(fullscreen=False,window=(5,10,580,580))
        else:
            print("off")
            # self.camera.stop_preview()
        self.state = not self.state

    def takePhoto(self):
        # Takes a photo the moment the button is pressed
        # Stores it in format : dd-mm-yyyy-HH-MM-SS.jpg
        date = datetime.datetime.now()
        file_ver = str(date.strftime("%d") + "-" + date.strftime("%m") + "-" + date.strftime("%Y") + "-" + date.strftime("%H") + "-" + date.strftime("%M") + "-" + date.strftime("%S"))
        file_ver = "../images/"+ file_ver + ".jpg"
        print(file_ver)
        self.view_translation_btn.configure(state = NORMAL)
        # self.camera.capture(file_ver)

    def transition_func(self,directory):
        # Default type of function to transition in between frames
        # Used to allow for page updates from a lambda command call
        self.view_translation_btn.configure(state = DISABLED)
        self.controller.show_frame(directory)

class SettingsPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.configure(bg='grey70')
        self.controller = controller

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        leftFrame = Frame(self,width=(screen_width/4*3 - 400), height=screen_height-200,bg="red")
        leftFrame.pack(side=LEFT,padx=5,pady=10)

        # Button Area
        rightFrame = Frame(self,width=(screen_width/4 - 100), height=screen_height-200,bg="blue")
        rightFrame.pack(side=RIGHT,padx=5,pady=10)

        rightFrame.grid_propagate(False)
        leftFrame.grid_propagate(False)

        ''' RIGHT SIDE '''
        # View Image
        # view_img_btn = Button(rightFrame,text="View Image",width=100,height=100, command = lambda : print("Image Preview"))
        # view_img_btn.grid(row=0,column=0,padx=5,pady=4)

        # View Translation
        # view_translation_btn = Button(rightFrame,text="View Translation",width=100,height=100, command = lambda : print("Translate"))
        # view_translation_btn.grid(row=1,column=0,padx=5,pady=4)

        # Device Settings
        settings_btn = Button(rightFrame,text="Settings",width=100,height=100, command = lambda : self.transition_func("SettingsPage"))
        settings_btn.grid(row=0,column=0,padx=5,pady=4)

        # Back to history
        history_btn = Button(rightFrame,text="History",width=100,height=100, command= lambda : self.transition_func("HistoryPage"))
        history_btn.grid(row=1,column=0,padx=5,pady=4)

        # Back to Main Page
        main_page_btn = Button(rightFrame,text="New Photo",width=100,height=100, command = lambda : self.transition_func("MainPage"))
        main_page_btn.grid(row=2,column=0,padx=5,pady=4)

        buttonList = [settings_btn,history_btn,main_page_btn]
        counter = 0
        for x in buttonList:
            rightFrame.grid_columnconfigure(counter,weight=1)
            rightFrame.grid_rowconfigure(counter,weight=1)
            counter += 1


    def transition_func(self,directory):
        # Default type of function to transition in between frames
        # Used to allow for page updates from a lambda command call
        self.controller.show_frame(directory)


app = AppUI()
app.mainloop()
