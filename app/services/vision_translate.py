import tkinter as tk
from tkinter import *
from tkinter import ttk

from PIL import ImageTk, Image

# from picamera import PiCamera
from time import sleep

from file_reading import ReadingFiles

import datetime

import os
import io


class HistoryPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller

        self.state = True
        self.curr_img_path = ''

        self.configure(bg='grey70')

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


        '''LEFT SIDE'''
        # Displaying A list of all files, possibly with image by side
        # ReadingFiles Class
        self.fileReading = ReadingFiles()

        # List boxes
        self.imagesList = Listbox(leftFrame,font="Arial 19",bd=5,height=21,width=22)
        self.imagesList.grid(row=0, column=0,padx=5,pady=50)

        # Bind The Listbox
        self.imagesList.bind("<<ListboxSelect>>", lambda x: self.listbox_func())

        # img = PhotoImage(file="../images_bound/"+fileReading.image_files[0])
        # img = ImageTk.PhotoImage(Image.open("../images_bound/" + fileReading.image_files[0]))
        # print("../images_bound/" + self.fileReading.image_files[0])

        img= (Image.open("../images_bound/" + self.fileReading.image_files[0]))
        resized_image= img.resize((300,300), Image.ANTIALIAS)
        new_image= ImageTk.PhotoImage(resized_image)

        self.img_label = Label(leftFrame, image = new_image)
        self.img_label.image = new_image
        self.img_label.grid(row=0, column=1,padx=5,pady=50)

        objList = [self.imagesList,self.img_label]

        leftFrame.grid_columnconfigure(0,weight=1)
        leftFrame.grid_columnconfigure(1,weight=1)
        leftFrame.grid_rowconfigure(0,weight=1)
        leftFrame.grid_rowconfigure(1,weight=1)

        # add items to list1
        for item in self.fileReading.image_files:
        	self.imagesList.insert(END, item)


        ''' RIGHT SIDE '''
        # Open Translation
        translation_btn = Button(rightFrame,text="View Translation",width=100,height=100, command = lambda : controller.show_frame("TranslationPage"))
        translation_btn.grid(row=0,column=0,padx=5,pady=4)

        # Delete Save
        delete_btn = Button(rightFrame,text="Delete Save",width=100,height=100, command = lambda : print("wow"))
        delete_btn.grid(row=1,column=0,padx=5,pady=4)

        # Device Settings
        settings_btn = Button(rightFrame,text="Settings",width=100,height=100, command = lambda : controller.show_frame("SettingsPage"))
        settings_btn.grid(row=2,column=0,padx=5,pady=4)

        # Back To Main screen
        closeApp = Button(rightFrame,text="Quit",width=100,height=100, command= lambda : self.exitProgram())
        closeApp.grid(row=3,column=0,padx=5,pady=4)

        buttonList = [translation_btn,delete_btn,settings_btn,closeApp]
        counter = 0
        for x in buttonList:
            rightFrame.grid_columnconfigure(counter,weight=1)
            rightFrame.grid_rowconfigure(counter,weight=1)
            counter += 1

    def change_img(self, n_img_name):
        self.curr_img_path = "../images_bound/" + n_img_name
        self.update_img()
        # self.controller.update_select(n_img_name)


    def listbox_func(self, *args):
        for each in self.fileReading.image_files:
            if self.imagesList.get(ANCHOR) == each:
                # self.change_img(each)
                self.controller.update_select(each)
            else:
                continue

    def update_img(self):
        # Use Selected image
        img = (Image.open(self.curr_img_path))

        resized_image= img.resize((300,300), Image.ANTIALIAS)
        new_image= ImageTk.PhotoImage(resized_image)

        self.img_label.configure(image = new_image)
        self.img_label.image = new_image

    def exitProgram(self):
        self.destroy()
        exit()

class TranslationPage(tk.Frame):
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

        '''LEFT SIDE'''
        # Swap between 2 text boxes and the image

        # Translation version - Text Boxes - File_reading version

        # Image version - Full Dispaly og screen size Image

        ''' RIGHT SIDE '''
        # View Image
        view_img_btn = Button(rightFrame,text="View Image", width=100, height=100, command = lambda : print("Image preview"))
        view_img_btn.grid(row=0,column=0,padx=5,pady=4)

        # View Translation
        view_translation_btn = Button(rightFrame,text="View Translation", width=100, height=100, command = lambda : print("Translate"))
        view_translation_btn.grid(row=1,column=0,padx=5,pady=4)

        # Device Settings
        settings_btn = Button(rightFrame,text="Settings",width=100,height=100, command = lambda : controller.show_frame("SettingsPage"))
        settings_btn.grid(row=2,column=0,padx=5,pady=4)

        # Back to history
        history_btn = Button(rightFrame,text="History",width=100,height=100, command= lambda : controller.show_frame("HistoryPage"))
        history_btn.grid(row=3,column=0,padx=5,pady=4)

        # Back to Main Page
        main_page_btn = Button(rightFrame,text="New Photo",width=100,height=100, command = lambda : controller.show_frame("MainPage"))
        main_page_btn.grid(row=4,column=0,padx=5,pady=4)

        buttonList = [view_img_btn, view_translation_btn, settings_btn, history_btn, main_page_btn]
        counter = 0
        for x in buttonList:
            rightFrame.grid_columnconfigure(counter,weight=1)
            rightFrame.grid_rowconfigure(counter,weight=1)
            counter += 1

    def focus(self,img_name):
        print("wow we translated?")
