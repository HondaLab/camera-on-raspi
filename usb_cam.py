#!/usr/bin/python3
import cv2
import os
import time

record_frame='y'
OUT_FILE='out.mp4'
while os.path.exists(OUT_FILE):
   print("# %sはすでに存在しています．" % OUT_FILE)
   OUT_FILE=input('## 新しい出力ファイル名:')
   OUT_FILE=OUT_FILE+'.mp4'
print('%s に動画を書き出します．' % OUT_FILE)


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

   if record_frame=='y':
      # 保存用
      fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
      #frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
      frame_rate = 4
      width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
      height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
      size = (width, height)
      vw = cv2.VideoWriter(OUT_FILE, fmt, frame_rate, size)

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
      if record_frame=='y':
         vw.write(frame)
        
      count+=1
      now=time.time()
      #time.sleep(0.1)

   now=time.time()
   rate=count/(now-start)
   speed=1.0/rate*1000
   print("rate=%5.2f (Hz)" % rate)
   print("speed=%5.2f (msec)" % speed)

   if record_frame=='y':
      print("%sに%7.2f(sec) 録画されました" % (OUT_FILE,now-start))
      vw.release()
   # release camera
   cap.release()

else:
   print("# Camera is NOT opened.")
   print("# Connect and turn on USB camera.")
