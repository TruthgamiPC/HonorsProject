from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()
for i in range(5):
    sleep(5)
    camera.capture('/home/pi/Desktop/image%s.jpg' % i)
camera.stop_preview()

# Source: https://projects.raspberrypi.org/en/projects/getting-started-with-picamera/2

# Terminal command for taking a photo with custom size
# raspistill -o Desktop/image-small.jpg -w 640 -h 480
