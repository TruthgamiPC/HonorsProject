from picamera import PiCamera
from time import sleep

from tkinter import *
from tkinter import ttk
import tkinter.font as tkFont

win = Tk()
win.title("Epic Moment?")
win.geometry("480x320")
win.configure(background="gray")

# Setting up the buttons
button_4 = ttk.Button(win, text="Take Photo4",width=13).place(x=350,y=130)
button_3 = ttk.Button(win, text="Take Photo3",width=13).place(x=350,y=90)
button_2 = ttk.Button(win, text="Take Photo2",width=13).place(x=350,y=50)
button_1 = ttk.Button(win, text="Take Photo1",width=13)

#button_1.grid(ipady=20,ipadx=20)
button_1.place(x=350,y=10)

def exitProgram():
    print("Exit button pressed")
    win.quit()


win.mainloop()


'''        
def photoTake(camera):
    camera.resolution = (800, 600)
    camera.framerate = 15
    
    camera.start_preview()
    sleep(5)
    camera.capture('/home/pi/Desktop/Honours Code - 1/images/image1.jpg')
    camera.stop_preview()


camera = PiCamera()
photoTake(camera)

camera.start_preview()
for i in range(5):
    sleep(5)
    camera.capture('/home/pi/Desktop/image%s.jpg' % i)
camera.stop_preview()
'''
# Source: https://projects.raspberrypi.org/en/projects/getting-started-with-picamera/2

# Terminal command for taking a photo with custom size
# raspistill -o Desktop/image-small.jpg -w 640 -h 480
