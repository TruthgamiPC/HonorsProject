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

LARGE_FONT = ("Verdana",14)


class AppUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        # tk.Tk.attributes(self,'-fullscreen',True)
        # tk.geometry("800x600")

        tk.Tk.wm_title(self,'Translator')

        window = tk.Frame(self)

        window.pack(side="top", fill="both", expand=True)
        window.grid_rowconfigure(0, weight=1,uniform=1)
        window.grid_columnconfigure(0, weight=1,uniform=1)

        self.frames = {}
        for F in (MainPage, HistoryPage, TranslationPage,SettingsPage):
            page_name = F.__name__
            frame = F(parent=window, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainPage")

        # frame = HistoryPage(window,self)
        # self.frames[HistoryPage] = frame
        # frame.grid(row=0, column=0, sticky="nsew")
        # self.show_frame(HistoryPage)

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

        self.configure(bg="grey70")

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

        history_btn = Button(rightFrame,text="History",width=100,height=100, command = lambda : controller.show_frame("HistoryPage"))
        history_btn.grid(row=0,column=0,padx=5,pady=4)


        settings_btn = Button(rightFrame,text="Change Language",width=100,height=100, command = lambda : controller.show_frame("SettingsPage"))
        settings_btn.grid(row=1,column=0,padx=5,pady=4)

        takePhoto_btn = Button(rightFrame,text="Take photo",width=100,height=100, command = lambda : self.takePhoto())
        takePhoto_btn.grid(row=2,column=0,padx=5,pady=4)

        closeApp = Button(rightFrame,text="Quit",width=100,height=100, command= lambda : self.exitProgram())
        #closeApp.image = photo
        closeApp.grid(row=3,column=0,padx=5,pady=4)

        buttonList = [history_btn,settings_btn,takePhoto_btn,closeApp]
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
        # self.camera.capture(file_ver)

class HistoryPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.state = True
        self.curr_img_path = ''

        self.configure(bg='grey70')

        # Main functional area
        leftFrame = Frame(self,width=(800/4*3 ), height=600,bg="red")
        leftFrame.pack(side=LEFT,padx=5,pady=10)

        rightFrame = Frame(self,width=(800/4 ), height=600,bg="blue")
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
        self.imagesList.bind("<<ListboxSelect>>", lambda x: self.change_img())

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

    def change_img(self, *args):
        for each in self.fileReading.image_files:
            # print(each)
            if self.imagesList.get(ANCHOR) == each:
                print("Wow its the: " + each)
                self.curr_img_path = "../images_bound/" + each
                self.update_img()
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

        leftFrame = Frame(self,width=(800/4*3 ), height=600,bg="red")
        leftFrame.pack(side=LEFT,padx=5,pady=10)

        rightFrame = Frame(self,width=(800/4 ), height=600,bg="blue")
        rightFrame.pack(side=RIGHT,padx=5,pady=10)

        rightFrame.grid_propagate(False)
        leftFrame.grid_propagate(False)

        '''LEFT SIDE'''
        # Swap between 2 text boxes and the image

        # Translation version - Text Boxes - File_reading version

        # Image version - Full Dispaly og screen size Image

        ''' RIGHT SIDE '''
        # View Image
        history = Button(rightFrame,text="History",width=100,height=100, command = lambda : self.photoPreview())
        history.grid(row=0,column=0,padx=5,pady=4)

        # View Translation
        # history = Button(rightFrame,text="History",width=100,height=100, command = lambda : self.photoPreview())
        # history.grid(row=0,column=0,padx=5,pady=4)

        # Delete Save
        language = Button(rightFrame,text="Change Language",width=100,height=100, command = lambda : print("Change Language"))
        language.grid(row=1,column=0,padx=5,pady=4)

        # Device Settings
        takePhoto = Button(rightFrame,text="Take photo",width=100,height=100, command = lambda : self.takePhoto())
        takePhoto.grid(row=2,column=0,padx=5,pady=4)

        # Back To Main screen
        closeApp = Button(rightFrame,text="Quit",width=100,height=100, command= lambda : self.exitProgram())
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

class SettingsPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)

    def exitProgram(self):
        self.destroy()
        exit()

app = AppUI()
app.mainloop()
