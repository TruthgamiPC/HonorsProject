from picamera import PiCamera
from time import sleep

def photoTake(camera):
    camera.resolution = (720, 540)
    camera.framerate = 30

    camera.start_preview()
    sleep(5)
    camera.capture('../images/image.jpg')
    camera.stop_preview()


camera = PiCamera()
photoTake(camera)

'''
camera.start_preview()
for i in range(5):
    sleep(5)
    camera.capture('/home/pi/Desktop/image%s.jpg' % i)
camera.stop_preview()
'''
