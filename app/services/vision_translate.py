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
        translation_btn = Button(rightFrame,text="View Translation",width=100,height=100, command = lambda : self.transition_func("TranslationPage"))
        translation_btn.grid(row=0,column=0,padx=5,pady=4)

        # Delete Save
        delete_btn = Button(rightFrame,text="Delete Save",width=100,height=100, command = lambda : self.delete_func())
        delete_btn.grid(row=1,column=0,padx=5,pady=4)

        # Device Settings
        settings_btn = Button(rightFrame,text="Settings",width=100,height=100, command = lambda : self.transition_func("SettingsPage"))
        settings_btn.grid(row=2,column=0,padx=5,pady=4)

        # Back To Main screen
        takePhoto_btn = Button(rightFrame,text="Quit",width=100,height=100, command= lambda : self.transition_func("MainPage"))
        takePhoto_btn.grid(row=3,column=0,padx=5,pady=4)

        buttonList = [translation_btn,delete_btn,settings_btn,takePhoto_btn]
        counter = 0
        for x in buttonList:
            rightFrame.grid_columnconfigure(counter,weight=1)
            rightFrame.grid_rowconfigure(counter,weight=1)
            counter += 1

    def delete_func(self):
        dirs = ['../images_bound/','../images/','../text_data/']
        i_img_name = self.controller.selected_img
        t_img_name = self.fileReading.stripper(i_img_name)
        for n,each in enumerate(dirs):
            if not n == 2:
                if os.path.exists(each + i_img_name):
                    os.remove(each + i_img_name)
                else:
                    print("Image file not found: " + each + i_img_name)
            else:
                if os.path.exists(each + t_img_name + '.json'):
                    os.remove(each + t_img_name + '.json')
                else:
                    print("Json file not found: " + each + t_img_name + '.json')

        # Updating the list after a delete has been done.
        self.update_list()
        self.controller.update_select(self.fileReading.image_files[0])

    def update_list(self):
        self.fileReading.searchDir()
        detected_num = len(self.fileReading.image_files)
        print(detected_num)
        for x, listbox_entry in enumerate(self.imagesList.get(0,END)):
            self.imagesList.delete(x)
            print(x)
            if (x) <= (detected_num-1):
                self.imagesList.insert(x,self.fileReading.image_files[x])

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

    def transition_func(self,directory):
        # Default type of function to transition in between frames
        # Used to allow for page updates from a lambda command call
        self.controller.show_frame(directory)

class TranslationPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        # self.fileReading = ReadingFiles

        self.configure(bg='grey70')
        self.curr_img_path = ''

        self.state_display = False

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
        # img= (Image.open("../images_bound/" + self.fileReading.image_files[0]))
        # resized_image= img.resize((300,300), Image.ANTIALIAS)
        # new_image= ImageTk.PhotoImage(resized_image)

        self.img_label = Label(leftFrame)
        self.img_label.grid(row=0, column=0,padx=5,pady=50)

        leftFrame.grid_columnconfigure(0,weight=1)
        # leftFrame.grid_columnconfigure(1,weight=1)
        leftFrame.grid_rowconfigure(0,weight=1)
        # leftFrame.grid_rowconfigure(1,weight=1)

        ''' RIGHT SIDE '''
        # View Image
        self.updatable_btn = Button(rightFrame,text="View Image", width=100, height=100, command = lambda : self.switch_display())
        self.updatable_btn.grid(row=0,column=0,padx=5,pady=4)

        # View Translation
        # view_translation_btn = Button(rightFrame,text="View Translation", width=100, height=100, command = lambda : print("Translate"))
        # view_translation_btn.grid(row=1,column=0,padx=5,pady=4)

        # Device Settings
        settings_btn = Button(rightFrame,text="Settings",width=100,height=100, command = lambda : self.transition_func("SettingsPage"))
        settings_btn.grid(row=1,column=0,padx=5,pady=4)

        # Back to history
        history_btn = Button(rightFrame,text="History",width=100,height=100, command= lambda : self.transition_func("HistoryPage"))
        history_btn.grid(row=2,column=0,padx=5,pady=4)

        # Back to Main Page
        main_page_btn = Button(rightFrame,text="New Photo",width=100,height=100, command = lambda : self.transition_func("MainPage"))
        main_page_btn.grid(row=3,column=0,padx=5,pady=4)

        buttonList = [self.updatable_btn, settings_btn, history_btn, main_page_btn]
        counter = 0
        for x in buttonList:
            rightFrame.grid_columnconfigure(counter,weight=1)
            rightFrame.grid_rowconfigure(counter,weight=1)
            counter += 1

    def receive_text_data(self):
        loaded_json = self.controller.fileReading.targeted_text(self.controller.recive_selected_img())

        for num in range(0,len(loaded_json)):
            for n,each_seg in enumerate(loaded_json[f'block{num}']):
                print(each_seg['original_text'])
                print(each_seg['translated_text'])


    def switch_display(self):
        # wow
        # print("We switchin")
        print(self.state_display)
        if self.state_display:
            self.state_display = not self.state_display
            self.receive_text_data()
            self.updatable_btn.configure(text="View Image",command = lambda: self.switch_display())
            # print("Text Version")
        else:
            self.state_display = not self.state_display
            self.updatable_btn.configure(text="View Text",command = lambda: self.switch_display())
            # print("Image Version")

    def change_img(self, n_img_name):
        self.curr_img_path = "../images_bound/" + n_img_name
        self.update_img()
        # self.controller.update_select(n_img_name)

    def update_img(self):
        # Use Selected image
        img = (Image.open(self.curr_img_path))

        resized_image= img.resize((500,500), Image.ANTIALIAS)
        new_image= ImageTk.PhotoImage(resized_image)

        self.img_label.configure(image = new_image)
        self.img_label.image = new_image

    def focus(self,img_name):
        print("wow we translated?")

    def transition_func(self,directory):
        # Default type of function to transition in between frames
        # Used to allow for page updates from a lambda command call
        self.controller.show_frame(directory)
