#!/usr/bin/python3
import cv2
import time

# open camera
cap = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L2)
if cap.isOpened():

   # set dimensions
   cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
   cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
   #cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
   cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('Y', 'U', 'Y', 'V'))
   cap.set(cv2.CAP_PROP_BUFFERSIZE, 4) # BUFFERSIZE を小さくするとレートが速くなる
   cap.set(cv2.CAP_PROP_FPS, 30)


   count=0
   print("# Input 'q' to stop the camera.")
   key=cv2.waitKey(1)
   now=time.time()
   start=now
   while key!=ord('q'):
      # take frame
      ret, frame = cap.read()
      cv2.imshow('frame',frame)
      key=cv2.waitKey(1)
      count+=1
      now=time.time()
      #time.sleep(0.1)

   now=time.time()
   rate=count/(now-start)
   speed=1.0/rate*1000
   print("rate=%5.2f (Hz)" % rate)
   print("speed=%5.2f (msec)" % speed)


   # write frame to file
   #cv2.imwrite('image.jpg', frame)
   # release camera
   cap.release()

else:
   print("# Camera is NOT opened.")
   print("# Connect and turn on USB camera.")
