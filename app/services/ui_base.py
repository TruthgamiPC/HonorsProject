import tkinter as tk
from tkinter import *
from tkinter import ttk

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

        self.configure(bg="grey70")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Main functional area
        leftFrame = Frame(self,width=(screen_width/4*3), height=screen_height,bg="red")
        leftFrame.pack(side=LEFT,padx=5,pady=10)

        # Button Area
        rightFrame = Frame(self,width=(screen_width/4), height=screen_height,bg="blue")
        rightFrame.pack(side=RIGHT,padx=5,pady=10)

        rightFrame.grid_propagate(False)
        leftFrame.grid_propagate(False)

        photo = PhotoImage(file = "button.png")

        history = Button(rightFrame,text="History",image=photo,
        command = lambda : print("History"))
        history.grid(row=0,column=0,padx=5,pady=4)
        history.image = photo
        history.configure(width=250,height=250)


        language = Button(rightFrame,text="Change Language",image=photo,
        command = lambda : print("Change Language"))
        language.image = photo
        language.grid(row=1,column=0,padx=5,pady=4)

        takePhoto = Button(rightFrame,text="Take photo",image=photo,
        command = lambda : print("Take photo"))
        takePhoto.image = photo
        takePhoto.grid(row=2,column=0,padx=5,pady=4)
        # print(takePhoto.winfo_width())

        closeApp = Button(rightFrame,text="Quit",image=photo,command=self.quit)
        closeApp.image = photo
        closeApp.grid(row=3,column=0,padx=5,pady=4)

        buttonList = [history,language,takePhoto,closeApp]
        counter = 0
        for x in buttonList:
            rightFrame.grid_columnconfigure(counter,weight=1)
            rightFrame.grid_rowconfigure(counter,weight=1)
            counter += 1


app = AppUI()
app.mainloop()
