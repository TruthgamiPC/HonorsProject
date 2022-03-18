import tkinter as tk

LARGE_FONT = ("Verdana",14)

class AppUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        tk.Tk.attributes(self,'-fullscreen',True)
        tk.Tk.wm_title(self,'Translator')

        window = tk.Frame(self)
        window.pack(side="top", fill="both", expand=True)
        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(0, weight=1)

        self.frames = {}

        frame = StartPage(window,self)

        self.frames[StartPage] = frame

        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self,cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        myCanvas = tk.Canvas(self, bg="black", width=(screen_width/4*3 - 10), height=screen_height-5)
        myCanvas.grid(row=0,column=0)

        pane_buttons = tk.Canvas(self, bg="cyan", width=(screen_width/4), height = screen_height-5)
        pane_buttons.grid(row=0,column=1)

        myCanvas.tag_

        label = tk.Label(self, text="Starting Page", font=LARGE_FONT)
        label.grid(row=0, column=1)
        #
        button = tk.Button(self,text="Close",fg,command=self.quit)
        button.grid(row=0, column=2)

#
# def CameraPreview(tk.Frame):
#
#     def __init__(self,parent,controller):
#         tk.Frame.__init__(self,parent)
#
#         myCanvas = tk.Canvas(root, bg="black", height=600, width=800)
#         myCanvas.pack()

app = AppUI()
app.mainloop()




# class WindowUI():
#     def __init__(self,window):
#         self.window = window
#         window.title("Translator GUI")
#
#         self.label = Label(window,text="This is our first GUI")
#         self.label.pack()
#
#         self.greet_button = Button(window,text="Greet", command=self.greet())
#         self.greet_button.pack()
#
#         self.close_button = Button(window,text="Close", command=window.quit)
#         self.close_button.pack()
#
#     def greet(self):
#         print("Greetings")
