import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import font as tkFont

from PIL import ImageTk, Image

from file_reading import ReadingFiles

import datetime

import os
import io

# Source Github - https://gist.github.com/mp035/9f2027c3ef9172264532fcd6262f3b01
class ScrollFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.canvas = tk.Canvas(self, width=(screen_width/4*3), height=screen_height,  borderwidth=0, background="#c7c7c7")          #place canvas on self
        self.viewPort = tk.Frame(self.canvas, background="#c7c7c7")
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas_window = self.canvas.create_window((4,4), window=self.viewPort, anchor="nw", tags="self.viewPort")

        self.viewPort.bind("<Configure>", self.onFrameConfigure)
        self.canvas.bind("<Configure>", self.onCanvasConfigure)

        self.onFrameConfigure(None)

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))                 #whenever the size of the frame changes, alter the scroll region respectively.

    def onCanvasConfigure(self, event):
        '''Reset the canvas window to encompass inner frame when required'''
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width = canvas_width)            #whenever the size of the canvas changes alter the window region respectively.


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
        leftFrame = Frame(self,width=(screen_width/4*3), height=screen_height,bg="#c7c7c7")
        leftFrame.pack(side=LEFT,padx=5,pady=10)

        # Button Area
        rightFrame = Frame(self,width=(screen_width/4), height=screen_height,bg="blue")
        rightFrame.pack(side=RIGHT,padx=5,pady=10)

        rightFrame.grid_propagate(False)
        leftFrame.grid_propagate(False)


        '''LEFT SIDE'''
        # Displaying A list of all files, possibly with image by side
        # ReadingFiles Class
        self.controller.fileReading = ReadingFiles()

        list_frame = Frame(leftFrame)
        list_frame.grid(row=0,column=0)

        list_scrollbar = Scrollbar(list_frame, orient="vertical")

        # List boxes
        self.imagesList = Listbox(list_frame, yscrollcommand= list_scrollbar.set ,bd=5,height=15,width=23)
        self.imagesList.pack(side="left")

        list_scrollbar.config(command = self.imagesList.yview)
        list_scrollbar.pack(side="right",fill="y")

        # Bind The Listbox
        self.imagesList.bind("<<ListboxSelect>>", lambda x: self.listbox_func())

        self.controller.selected_img = self.controller.fileReading.image_files[0]
        img= (Image.open("./images_bound/" + self.controller.recive_selected_img()))
        resized_image= img.resize((250,250), Image.ANTIALIAS)
        new_image= ImageTk.PhotoImage(resized_image)

        self.img_label = Label(leftFrame, image = new_image)
        self.img_label.image = new_image
        self.img_label.grid(row=0, column=2,padx=5,pady=50)

        objList = [self.imagesList,self.img_label]

        leftFrame.grid_columnconfigure(0,weight=1)
        leftFrame.grid_columnconfigure(1,weight=1)
        leftFrame.grid_rowconfigure(0,weight=1)
        leftFrame.grid_rowconfigure(1,weight=1)

        # add items to list1
        for item in self.controller.fileReading.image_files:
        	self.imagesList.insert(END, item)


        ''' RIGHT SIDE '''
        # Device Settings
        settings_btn = Button(rightFrame,text="Settings", font = self.controller.button_font,width=100,height=100, command = lambda : self.transition_func("SettingsPage"))
        settings_btn.grid(row=0,column=0,padx=5,pady=4)

        # Back To Main screen
        takePhoto_btn = Button(rightFrame,text="Take a\nNew Photo", font = self.controller.button_font,width=100,height=100, command= lambda : self.transition_func("MainPage"))
        takePhoto_btn.grid(row=1,column=0,padx=5,pady=4)

        # Delete Save
        delete_btn = Button(rightFrame,text="Delete Save", font = self.controller.button_font,width=100,height=100, command = lambda : self.delete_func())
        delete_btn.grid(row=2,column=0,padx=5,pady=4)

        # Open Translation
        translation_btn = Button(rightFrame,text="View\nTranslation", font = self.controller.button_font,width=100,height=100, command = lambda : self.transition_func("TranslationPage"))
        translation_btn.grid(row=3,column=0,padx=5,pady=4)



        buttonList = [translation_btn,delete_btn,settings_btn,takePhoto_btn]
        counter = 0
        for x in buttonList:
            rightFrame.grid_columnconfigure(counter,weight=1)
            rightFrame.grid_rowconfigure(counter,weight=1)
            counter += 1

    def delete_func(self):
        dirs = ['./images_bound/','./images/','./text_data/']
        i_img_name = self.controller.selected_img
        t_img_name = self.controller.fileReading.stripper(i_img_name)
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
        self.update_delete()
        self.controller.update_select(self.controller.fileReading.image_files[0])

    def update_list(self):
        self.controller.fileReading.searchDir()
        for x, fileDetection in enumerate(self.controller.fileReading.image_files):
            self.imagesList.delete(x)
            self.imagesList.insert(x,self.controller.fileReading.image_files[x])

    def update_delete(self):
        self.controller.fileReading.searchDir()
        detected_num = len(self.controller.fileReading.image_files)
        # print(detected_num)
        for x, listbox_entry in enumerate(self.imagesList.get(0,END)):
            self.imagesList.delete(x)
            # print(x)
            if (x) <= (detected_num-1):
                self.imagesList.insert(x,self.controller.fileReading.image_files[x])

    def change_img(self, n_img_name):
        self.curr_img_path = "./images_bound/" + n_img_name
        self.update_img()

    def listbox_func(self, *args):
        for each in self.controller.fileReading.image_files:
            if self.imagesList.get(ANCHOR) == each:
                self.controller.update_select(each)
            else:
                continue

    def update_font(self):
        loader = self.controller.settings_page.load_file()
        tmp_font = tkFont.Font(family='Helvetica', size = 18)
        self.imagesList.configure(width=23, height=18)        # for each_ele in self.imagesList:
        self.imagesList.configure(fg=loader.get('device_settings','text_colour'), bg=loader.get('device_settings','bg_colour'), font = tmp_font)

    def update_frame(self):
        # print("History Page Update")

        self.update_list()
        self.update_font()

        self.controller.main_page.camera.stop_preview()
        self.controller.main_page.state = True

    def update_img(self):
        # Use Selected image
        img = (Image.open(self.curr_img_path))

        resized_image= img.resize((250,250), Image.ANTIALIAS)
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

        self.configure(bg='grey70')

        self.state_display = True
        self.curr_img_path = ''
        self.list_of_text_objects = []
        font_first = tkFont.Font(family='Helvetica',size=22)


        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.leftFrame = Frame(self, width=(screen_width/4*3), height=screen_height, bg="#c7c7c7")
        self.leftFrame.pack(side=LEFT,padx=5,pady=10)

        self.ls_frame = ScrollFrame(self.leftFrame)
        self.ls_frame.pack(side="top", fill="both", expand=True)

        # Button Area
        rightFrame = Frame(self,width=(screen_width/4), height=screen_height,bg="blue")
        rightFrame.pack(side=RIGHT,padx=5,pady=10)

        rightFrame.grid_propagate(False)
        self.leftFrame.grid_propagate(False)

        '''LEFT SIDE'''
        self.og_label = Label(self.ls_frame.viewPort, text="Original Text:", font = font_first)
        self.og_label.grid(column=0,row=0, pady = 10)
        # language = loader.get('device_settings','target_language')
        self.trans_label = Label(self.ls_frame.viewPort, text="", font = font_first)
        self.trans_label.grid(column=1,row=0, pady = 10)
        # - - - - - - - - - - - - - - - - - - - - - - - - - - -

        self.img_label = Label(self.leftFrame)
        self.img_label.grid(row=200, column=200,padx=5,pady=50)

        self.leftFrame.grid_columnconfigure(200,weight=1)
        self.leftFrame.grid_rowconfigure(200,weight=1)


        ''' RIGHT SIDE '''
        # Device Settings
        settings_btn = Button(rightFrame,text="Settings", font = self.controller.button_font,width=100,height=100, command = lambda : self.transition_func("SettingsPage"))
        settings_btn.grid(row=0,column=0,padx=5,pady=4)

        # Back to Main Page
        main_page_btn = Button(rightFrame,text="Take a \nNew Photo", font = self.controller.button_font,width=100,height=100, command = lambda : self.transition_func("MainPage"))
        main_page_btn.grid(row=1,column=0,padx=5,pady=4)

        # Back to history
        history_btn = Button(rightFrame,text="History", font = self.controller.button_font,width=100,height=100, command= lambda : self.transition_func("HistoryPage"))
        history_btn.grid(row=2,column=0,padx=5,pady=4)

        # View Image
        self.updatable_btn = Button(rightFrame,text="View Image", font = self.controller.button_font, width=100, height=100, command = lambda : self.switch_display())
        self.updatable_btn.grid(row=3,column=0,padx=5,pady=4)

        buttonList = [self.updatable_btn, settings_btn, history_btn, main_page_btn]
        counter = 0
        for x in buttonList:
            rightFrame.grid_columnconfigure(counter,weight=1)
            rightFrame.grid_rowconfigure(counter,weight=1)
            counter += 1

    def language_detect(self,lang_pass):
        if lang_pass == "en":
            return "English"
        elif lang_pass == "de":
            return "German"
        elif lang_pass == "bg":
            return "Bulgarian"
        elif lang_pass == "ru":
            return "Russian "
        elif lang_pass == "nl":
            return "Dutch"
        elif lang_pass == "it":
            return "Italian"
        elif lang_pass == "fr":
            return "French"
        else:
            return "No Language"

    # Constructing the text boxes with translation text
    def receive_text_data(self):
        loaded_json = self.controller.fileReading.targeted_text(self.controller.recive_selected_img())

        img_language = self.controller.selected_img
        lang_full = self.language_detect(img_language[:2])
        self.trans_label.configure(text=f"Translated Text\n- {lang_full} -")


        self.ls_frame.viewPort.grid_columnconfigure(0,weight=1)
        self.ls_frame.viewPort.grid_columnconfigure(1,weight=1)

        row_counter = 1
        for num in range(0,len(loaded_json)):
            for n,each_seg in enumerate(loaded_json[f'block{num}']):
                if each_seg['translated_text'] == "Invalid Translation #000044":
                    continue
                if (each_seg['translated_text'].replace(' ','')) == (each_seg['original_text'].replace(' ','')):
                    continue
                og_text = tk.Text(self.ls_frame.viewPort,width=20)
                trans_text = tk.Text(self.ls_frame.viewPort,width=20)
                og_text.grid(column=0,row=(row_counter),padx=10, pady=10) # num+n+1,ipadx=25,ipady=5
                trans_text.grid(column=1,row=(row_counter),padx=10, pady=10) # ipadx=25,ipady=5

                og_text.insert(tk.END,each_seg['original_text'])
                trans_text.insert(tk.END,each_seg['translated_text'])

                og_text.configure(state='disabled')
                trans_text.configure(state='disabled')

                self.list_of_text_objects.append(og_text)
                self.list_of_text_objects.append(trans_text)

                self.leftFrame.grid_columnconfigure(num,weight=1)
                row_counter += 1

    def delete_page_data(self):
        for each_el in self.list_of_text_objects:
            each_el.destroy()
        self.list_of_text_objects.clear()

    def hide_text_data(self):
        self.og_label.grid_remove()
        self.trans_label.grid_remove()
        for each_el in self.list_of_text_objects:
            each_el.grid_remove()

    def unhide_text_data(self):
        self.og_label.grid()
        self.trans_label.grid()
        for each_el in self.list_of_text_objects:
            each_el.grid()

    def switch_display(self):
        # print(self.state_display)
        if self.state_display:
            # Text Version
            if len(self.list_of_text_objects) < 2:
                self.receive_text_data()

            self.updatable_btn.configure(text="View Image",command = lambda: self.switch_display())
            self.img_label.grid_remove()
            self.unhide_text_data()

        else:
            # Image Version
            self.hide_text_data()
            self.updatable_btn.configure(text="View Text",command = lambda: self.switch_display())
            self.img_label.grid()

        self.state_display = not self.state_display

    def change_img(self, n_img_name):
        self.curr_img_path = "./images_bound/" + n_img_name
        self.update_img()

    def update_img(self):
        # Use Selected image
        img = (Image.open(self.curr_img_path))

        resized_image= img.resize((500,500), Image.ANTIALIAS)
        new_image= ImageTk.PhotoImage(resized_image)

        self.img_label.configure(image = new_image)
        self.img_label.image = new_image

    def transition_func(self,directory):
        # Default type of function to transition in between frames
        # Used to allow for page updates from a lambda command call
        self.controller.show_frame(directory)

    def update_font(self):
        loader = self.controller.settings_page.load_file()
        n_font_size = loader.get('device_settings','font_size')
        n_font_type = loader.get('device_settings','font_type')
        tmp_font = tkFont.Font(family=n_font_type, size = n_font_size)

        for each_ele in self.list_of_text_objects:
            each_ele.configure(fg=loader.get('device_settings','text_colour'), bg=loader.get('device_settings','bg_colour'), font = tmp_font)

            if int(n_font_size) == 14:
                each_ele.configure(width=26, height=(self.length_validaiton(int(len(each_ele.get(1.0,END))), 26)))
            elif int(n_font_size) == 18:
                each_ele.configure(width=21, height=(self.length_validaiton(int(len(each_ele.get(1.0,END))), 21)))
            elif int(n_font_size) == 22:
                each_ele.configure(width=17, height=(self.length_validaiton(int(len(each_ele.get(1.0,END))), 17)))
            elif int(n_font_size) == 26:
                each_ele.configure(width=14, height=(self.length_validaiton(int(len(each_ele.get(1.0,END))), 14)))
            elif int(n_font_size) == 30:
                each_ele.configure(width=12, height=(self.length_validaiton(int(len(each_ele.get(1.0,END))), 12))) # , height=4

    def length_validaiton(self, text_length, max_length):
        if (int(text_length / max_length) + (text_length % max_length > 0)) < 7:
            return (int(text_length / max_length) + (text_length % max_length > 0))
        else:
            return 7

    # Updates the frame on call
    def update_frame(self):
        # ensure list_of_text_objects is empty
        self.delete_page_data()
        # ensure the image is the correct one
        self.controller.update_translate()

        # reset the state to default one so always boots the same way
        self.state_display = True
        self.switch_display()
        self.update_font()

        self.controller.main_page.camera.stop_preview()
        self.controller.main_page.state = True
