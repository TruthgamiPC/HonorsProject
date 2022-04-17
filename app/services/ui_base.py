import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import font as tkFont

from PIL import ImageTk, Image

# from picamera import PiCamera
from time import sleep

from file_reading import ReadingFiles
from vision_translate import HistoryPage, TranslationPage
from improved_vision import *

import datetime
from configparser import ConfigParser

import os
import io


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

        self.settings_page = self.frames["SettingsPage"]
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
        frame.update_frame()
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

        settings_btn = Button(rightFrame,text="Settings",width=100,height=88, command = lambda : self.transition_func("SettingsPage"))
        settings_btn.grid(row=0,column=0,padx=5,pady=4)

        history_btn = Button(rightFrame,text="History",width=100,height=88, command = lambda : self.transition_func("HistoryPage"))
        history_btn.grid(row=1,column=0,padx=5,pady=4)

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

    def post_takePhoto(self,n_img_name):
        # self.controller.selected_img = n_img_name

        vision_func = VisionEntry(n_img_name)
        vision_func.vision_op()
        sleep(3)

        stripped_img_name = self.controller.fileReading.og_strip(n_img_name)
        self.controller.selected_img = stripped_img_name

        print(n_img_name, ' - - - ',stripped_img_name)
        self.view_translation_btn.configure(state = NORMAL)

    def takePhoto(self):
        # Takes a photo the moment the button is pressed
        # Stores it in format : dd-mm-yyyy-HH-MM-SS.jpg
        date = datetime.datetime.now()
        # file_ver = str(date.strftime("%d") + "-" + date.strftime("%m") + "-" + date.strftime("%Y") + "-" + date.strftime("%H") + "-" + date.strftime("%M") + "-" + date.strftime("%S"))
        file_ver = "3"
        file_ver = "../images/"+ file_ver + ".png"
        print(file_ver)
        # self.camera.capture(file_ver)
        self.post_takePhoto(file_ver)

    def transition_func(self,directory):
        # Default type of function to transition in between frames
        # Used to allow for page updates from a lambda command call
        self.view_translation_btn.configure(state = DISABLED)
        self.controller.show_frame(directory)

    def update_frame(self):
        print("Main Page Update")

class SettingsPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)

        self.configure(bg='grey70')
        self.controller = controller
        font_first = tkFont.Font(family='Helvetica',size=28)

        font_options = [10,14,18,22,26,30]
        self.selected_font_size = StringVar(self)

        f_colour_options = ['Black','Red','Yellow','White','Peach']
        self.selected_f_colour = StringVar(self)

        bg_colour_options = ['White','Peach','Yellow','Orange']
        self.selected_bg_colour = StringVar(self)

        language_options = ['English','French','German','Bulgarian','Italian','Dutch','Russian']
        self.selected_language = StringVar(self)

        self.loading_settings()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        leftFrame = Frame(self,width=(screen_width/4*3 - 400), height=screen_height-200,bg="red")
        leftFrame.pack(side=LEFT,padx=5,pady=10)

        # Button Area
        rightFrame = Frame(self,width=(screen_width/4 - 100), height=screen_height-200,bg="blue")
        rightFrame.pack(side=RIGHT,padx=5,pady=10)

        rightFrame.grid_propagate(False)
        leftFrame.grid_propagate(False)

        ''' LEFT SIDE'''
        self.font_text_box = tkFont.Font(family='Helvetica',size=self.selected_font_size.get())
        self.text_box = tk.Text(leftFrame, height=1, width=30)
        self.text_box.grid(column=1,row=1)

        self.text_box.insert(tk.END,'Sample text for demo')
        self.text_box.configure(state ='disabled')

        self.text_box.configure(font = self.font_text_box)

        self.text_box.tag_configure("colour")


        ''' FIRST DROP DOWN '''
        font_size_dropdown = OptionMenu(leftFrame, self.selected_font_size, *font_options, command= self.update_font)
        font_size_dropdown.grid(row=0,column=0,padx=5,pady=25)
        font_size_dropdown.configure(font=font_first)

        size_menu = leftFrame.nametowidget(font_size_dropdown.menuname)
        size_menu.config(font=font_first)  # Set the dropdown menu's font

        ''' SECOND DROP DOWN '''
        font_colour_dropdown = OptionMenu(leftFrame, self.selected_f_colour, *f_colour_options, command= self.update_font)
        font_colour_dropdown.grid(row=0,column=1,padx=5,pady=25)
        font_colour_dropdown.configure(font=font_first)

        f_colour_menu = leftFrame.nametowidget(font_colour_dropdown.menuname)
        f_colour_menu.config(font=font_first)

        ''' THIRD DROP DOWN '''
        bg_colour_dropdown = OptionMenu(leftFrame, self.selected_bg_colour, *bg_colour_options, command= self.update_font)
        bg_colour_dropdown.grid(row=0, column=2, padx=5, pady=25)
        bg_colour_dropdown.configure(font=font_first)

        bg_colour_menu = leftFrame.nametowidget(bg_colour_dropdown.menuname)
        bg_colour_menu.config(font= font_first)

        ''' FORTH DROP DOWN '''
        language_dropdown = OptionMenu(leftFrame, self.selected_language, *language_options, command= self.update_font)
        language_dropdown.grid(row=0, column=3, padx=5, pady=25)
        language_dropdown.configure(font=font_first)

        language_menu = leftFrame.nametowidget(language_dropdown.menuname)
        language_menu.config(font= font_first)

        self.update_font_c()

        ''' RIGHT SIDE '''
        # Back to history
        history_btn = Button(rightFrame,text="History",width=70,height=15, command= lambda : self.transition_func("HistoryPage"))
        history_btn.grid(row=0,column=0,padx=5,pady=4)

        # Back to Main Page
        main_page_btn = Button(rightFrame,text="New Photo",width=70,height=15, command = lambda : self.transition_func("MainPage"))
        main_page_btn.grid(row=1,column=0,padx=5,pady=4)

        buttonList = [history_btn,main_page_btn]
        counter = 0
        for x in buttonList:
            rightFrame.grid_columnconfigure(counter,weight=1)
            # rightFrame.grid_rowconfigure(counter,weight=1)
            counter += 1

    def write_settigns(self):
        # Export settings to the settings file
        config = ConfigParser()

        config['device_settings'] = {
            'font_size' : str(self.selected_font_size.get()),
            'text_colour' : str(self.selected_f_colour.get()),
            'bg_colour' : str(self.selected_bg_colour.get()),
            'target_language' : str(self.selected_language.get())
        }

        with open('setting.ini','w') as f:
            config.write(f)

    def load_file(self):
        loader = ConfigParser()
        loader.read('setting.ini')

        return loader

    def loading_settings(self):
        loader = self.load_file()

        self.selected_font_size.set(loader.get('device_settings','font_size'))
        self.selected_f_colour.set(loader.get('device_settings','text_colour'))
        self.selected_bg_colour.set(loader.get('device_settings','bg_colour'))
        self.selected_language.set(loader.get('device_settings','target_language'))

    def update_font_c(self):
        self.font_text_box = tkFont.Font(family='Helvetica' ,size=self.selected_font_size.get())

        self.text_box.configure(font = self.font_text_box)
        self.text_box.configure(fg=self.selected_f_colour.get())
        self.text_box.configure(bg=self.selected_bg_colour.get())

    def update_font(self, event):
        # Burner function that is used to accept event state
        self.update_font_c()

    def transition_func(self,directory):
        # Default type of function to transition in between frames
        # Used to allow for page updates from a lambda command call
        self.write_settigns()
        self.controller.show_frame(directory)

    def update_frame(self):
        return


app = AppUI()
app.mainloop()
