import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import font as tkFont

from PIL import ImageTk, Image
from google.cloud import translate_v2 as translate

from picamera import PiCamera
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
        tk.Tk.attributes(self,'-fullscreen',True)

        tk.Tk.wm_title(self,'Translator')
        self.selected_img = ""
        self.fileReading = ReadingFiles()
        self.button_font = tkFont.Font(family='Helvetica',size=16)

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
        self.camera = PiCamera()

        #Camera Setup - re-initialise on page load
        self.camera.resolution = (1200,1200)
        self.camera.framerate = 30
        self.camera.rotation = 90

        self.configure(bg="grey70")
        self.controller = controller

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Main functional area
        leftFrame = Frame(self,width=(screen_width/4*3), height=screen_height, bg="#c7c7c7")
        leftFrame.pack(side=LEFT,padx=5,pady=10)

        # Button Area
        rightFrame = Frame(self,width=(screen_width/4), height=screen_height, bg="blue")
        rightFrame.pack(side=RIGHT,padx=5,pady=10)

        rightFrame.grid_propagate(False)
        leftFrame.grid_propagate(False)

        # photo = PhotoImage(file = "button.png")

        settings_btn = Button(rightFrame,text="Settings", font = self.controller.button_font,width=100,height=7, command = lambda : self.transition_func("SettingsPage"))
        settings_btn.grid(row=0,column=0,padx=5,pady=4)

        history_btn = Button(rightFrame,text="History",font = self.controller.button_font,width=100,height=7, command = lambda : self.transition_func("HistoryPage"))
        history_btn.grid(row=1,column=0,padx=5,pady=4)

        self.view_translation_btn = Button(rightFrame,text="View Translation",font = self.controller.button_font,width=100,height=7, command= lambda : self.transition_func("TranslationPage"))
        self.view_translation_btn.grid(row=2,column=0,padx=5,pady=4)

        takePhoto_btn = Button(rightFrame,text="Take photo",font = self.controller.button_font,width=100,height=10, command = lambda : self.takePhoto())
        takePhoto_btn.grid(row=3,column=0,padx=5,pady=4)

        buttonList = [history_btn,settings_btn,takePhoto_btn,self.view_translation_btn]
        counter = 0
        for x in buttonList:
            rightFrame.grid_columnconfigure(counter,weight=1)
            rightFrame.grid_rowconfigure(counter,weight=1)
            counter += 1

        # self.photoPreview()

    #Preview Method needed to display the camera - overlaps 'leftFrame' as picamera has higher priority for display
    def photoPreview(self):
        # return
        if self.state:
            print("on")
            self.camera.start_preview(fullscreen=False,window=(20,10,580,580))
        else:
            print("off")
            self.camera.stop_preview()
        self.state = not self.state

    def post_takePhoto(self,n_img_name):
        self.controller.selected_img = n_img_name

        vision_func = VisionEntry(n_img_name)
        vision_func.vision_op()
        sleep(3)

        stripped_img_name = self.controller.fileReading.og_strip(n_img_name)
        self.controller.selected_img = stripped_img_name

        print(n_img_name, ' - - - ',stripped_img_name)

    def takePhoto(self):
        # Takes a photo the moment the button is pressed
        # Stores it in format : dd-mm-yyyy-HH-MM-SS.jpg
        date = datetime.datetime.now()
        file_ver = str(self.controller.settings_page.target_lang + "-" + date.strftime("%y") + "-" + date.strftime("%m") + "-"  + date.strftime("%d") + "-" + date.strftime("%H") + "-" + date.strftime("%M") + "-" + date.strftime("%S"))
        # file_ver = "3"
        file_ver = "../images/"+ file_ver + ".png"
        print(file_ver)
        self.camera.capture(file_ver)

        self.post_takePhoto(file_ver)

    def transition_func(self,directory):
        # Default type of function to transition in between frames
        # Used to allow for page updates from a lambda command call
        self.photoPreview()
        self.controller.show_frame(directory)

    def update_frame(self):
        self.photoPreview()
        print("Main Page Update")

class SettingsPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)

        self.configure(bg='grey70')
        self.controller = controller
        font_first = tkFont.Font(family='Helvetica',size=28)
        self.settings_translate = translate.Client()
        self.target_lang = ""

        font_options = [14,18,22,26,30]
        self.selected_font_size = StringVar(self)

        f_colour_options = ['Black','Red','Yellow','White']
        self.selected_f_colour = StringVar(self)

        bg_colour_options = ['White','Yellow','Orange','Black']
        self.selected_bg_colour = StringVar(self)

        language_options = ['English','French','German','Bulgarian','Italian','Dutch','Russian']
        self.selected_language = StringVar(self)

        self.loading_settings()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        leftFrame = Frame(self,width=(screen_width/4*3), height=screen_height, bg="#c7c7c7")
        leftFrame.pack(side=LEFT,padx=5,pady=10)

        # Button Area
        rightFrame = Frame(self,width=(screen_width/4), height=screen_height,bg="blue")
        rightFrame.pack(side=RIGHT,padx=5,pady=10)

        rightFrame.grid_propagate(False)
        leftFrame.grid_propagate(False)

        ''' LEFT SIDE'''
        self.font_text_box = tkFont.Font(family='Helvetica',size=self.selected_font_size.get())

        # Frame for buttons
        self.button_hold_frame = Frame(leftFrame,bg="#c7c7c7")
        self.button_hold_frame.grid(column=0,row=0, pady=(40,0))


         # Frame for text demo
        self.child_left_frame = Frame(leftFrame, highlightbackground="black", highlightthickness=2,bg="#c7c7c7")
        self.child_left_frame.grid(column=0, row=1, padx=40,pady=20)


        # Original Text display
        self.og_text_box = tk.Text(self.child_left_frame, height=1, width=20)
        self.og_text_box.grid(column=0,row=0,pady=10,padx=10)
        self.og_text_box.insert(tk.END,'Sample text for demo')
        self.og_text_box.configure(state ='disabled')
        self.og_text_box.configure(font = self.font_text_box)

         # Translated Text display
        self.trans_text_box = tk.Text(self.child_left_frame, height=1, width=20)
        self.trans_text_box.grid(column=1,row=0,pady=10,padx=10)
        self.trans_text_box.insert(tk.END,'Sample text for demo')
        self.trans_text_box.configure(state ='disabled')
        self.trans_text_box.configure(font = self.font_text_box)


        ''' FIRST DROP DOWN '''
        font_size_dropdown = OptionMenu(self.button_hold_frame, self.selected_font_size, *font_options, command= self.update_font)
        font_size_dropdown.grid(row=0,column=0,padx=(20,5),pady=25)
        font_size_dropdown.configure(font=font_first)

        size_menu = self.button_hold_frame.nametowidget(font_size_dropdown.menuname)
        size_menu.config(font=font_first)  # Set the dropdown menu's font

        ''' SECOND DROP DOWN '''
        font_colour_dropdown = OptionMenu(self.button_hold_frame, self.selected_f_colour, *f_colour_options, command= self.update_font)
        font_colour_dropdown.grid(row=0,column=1,padx=5,pady=25)
        font_colour_dropdown.configure(font=font_first)

        f_colour_menu = self.button_hold_frame.nametowidget(font_colour_dropdown.menuname)
        f_colour_menu.config(font=font_first)

        ''' THIRD DROP DOWN '''
        bg_colour_dropdown = OptionMenu(self.button_hold_frame, self.selected_bg_colour, *bg_colour_options, command= self.update_font)
        bg_colour_dropdown.grid(row=0, column=2, padx=5, pady=25)
        bg_colour_dropdown.configure(font=font_first)

        bg_colour_menu = self.button_hold_frame.nametowidget(bg_colour_dropdown.menuname)
        bg_colour_menu.config(font= font_first)

        ''' FORTH DROP DOWN '''
        language_dropdown = OptionMenu(self.button_hold_frame, self.selected_language, *language_options, command= self.update_font)
        language_dropdown.grid(row=0, column=3, padx=(5,20), pady=25)
        language_dropdown.configure(font=font_first)

        language_menu = self.button_hold_frame.nametowidget(language_dropdown.menuname)
        language_menu.config(font= font_first)

        self.update_font_c()

        ''' RIGHT SIDE '''
        # Back to history
        history_btn = Button(rightFrame,text="History", font = self.controller.button_font ,width=70,height=5, command= lambda : self.transition_func("HistoryPage"))
        history_btn.grid(row=0,column=0,padx=5,pady=4)

        # Back to Main Page
        main_page_btn = Button(rightFrame,text="New Photo", font = self.controller.button_font ,width=70,height=5, command = lambda : self.transition_func("MainPage"))
        main_page_btn.grid(row=2,column=0,padx=5,pady=4)

        trans_page_btn = Button(rightFrame,text="View\nTranslation", font = self.controller.button_font ,width=70,height=5, command = lambda : self.transition_func("TranslationPage"))
        trans_page_btn.grid(row=1,column=0,padx=5,pady=4)


        buttonList = [history_btn,main_page_btn,trans_page_btn]
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

        self.og_text_box.configure(font = self.font_text_box)
        self.og_text_box.configure(fg=self.selected_f_colour.get())
        self.og_text_box.configure(bg=self.selected_bg_colour.get())

        self.trans_text_box.configure(font = self.font_text_box)
        self.trans_text_box.configure(fg=self.selected_f_colour.get())
        self.trans_text_box.configure(bg=self.selected_bg_colour.get())

        n_font_size = self.selected_font_size.get()

        for x in [self.og_text_box,self.trans_text_box]:
            if int(n_font_size) == 14:
                x.configure(width=20, height=(self.length_validaiton(int(len(x.get(1.0,END))), 20)))
            elif int(n_font_size) == 18:
                x.configure(width=17, height=(self.length_validaiton(int(len(x.get(1.0,END))), 17)))
            elif int(n_font_size) == 22:
                x.configure(width=14, height=(self.length_validaiton(int(len(x.get(1.0,END))), 14)))
            elif int(n_font_size) == 26:
                x.configure(width=12, height=(self.length_validaiton(int(len(x.get(1.0,END))), 12)))
            elif int(n_font_size) == 30:
                x.configure(width=10, height=(self.length_validaiton(int(len(x.get(1.0,END))), 10)))

        if self.selected_language.get() == "English":
            self.target_lang = "en"
        if self.selected_language.get() == "Bulgarian":
            self.target_lang = "bg"
        if self.selected_language.get() == "French":
            self.target_lang = "fr"
        if self.selected_language.get() == "Russian":
            self.target_lang = "ru"
        if self.selected_language.get() == "German":
            self.target_lang = "de"
        if self.selected_language.get() == "Italian":
            self.target_lang = "it"
        if self.selected_language.get() == "Dutch":
            self.target_lang = "nl"

        temp_og_text = "Sample text for demo"
        temp_text_hold = (self.settings_translate.translate(temp_og_text,target_language= self.target_lang))["translatedText"]
        self.trans_text_box.configure(state=NORMAL)
        self.trans_text_box.delete(1.0,END)
        self.trans_text_box.insert(1.0,temp_text_hold)
        self.trans_text_box.configure(state="disabled")

    def length_validaiton(self, text_length, max_length):
        int(21 / 5) + (21 % 5 > 0)
        if (int(text_length / max_length) + (text_length % max_length > 0)) < 5:
            return (int(text_length / max_length) + (text_length % max_length > 0))
        else:
            return 5

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
