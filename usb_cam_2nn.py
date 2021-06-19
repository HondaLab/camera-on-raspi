#!/usr/bin/python3
# 210619 USBカメラで読み込んだframeをNNに入力
import cv2
import os
import time
import numpy as np
import modules.keyin as keyin

#(640x360),(1280x720),(1440x1440),... for SF360 4K
WIDTH=1280
HEIGHT=720
record_fps=18 # システムのスピードに応じて変更する必要あり
camera_dev='/dev/video0'
mozic=0.25 # モザイク処理のfactor

def area(img,px,py,w,h): # エリア内のRGB平均値

   rgb=[0,0,0]
   rgb[0]=np.sum(img[py:py+h,px:px+w,0])/(w*h)
   rgb[1]=np.sum(img[py:py+h,px:px+w,1])/(w*h)
   rgb[2]=np.sum(img[py:py+h,px:px+w,2])/(w*h)
   return rgb
     

# open camera
cap = cv2.VideoCapture(camera_dev, cv2.CAP_V4L2)
if cap.isOpened(): # カメラが開けた場合
   record_frame=input('# 録画しますか(y/n default=y)')
   if record_frame=='':
      record_frame='y'
   if record_frame=='y':
      OUT_FILE='out.mp4'
      while os.path.exists(OUT_FILE):
         print("# %sはすでに存在しています．" % OUT_FILE)
         OUT_FILE=input('## 新しい出力ファイル名:')
         OUT_FILE=OUT_FILE+'.mp4'
      print('%s に動画を書き出します．' % OUT_FILE)

   # set dimensions
   cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
   cap.set(cv2.CAP_PROP_FRAME_HEIGHT,HEIGHT)
   #cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
   cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('Y', 'U', 'Y', 'V'))
   cap.set(cv2.CAP_PROP_BUFFERSIZE, 4) # BUFFERSIZE を小さくするとレートが速くなる
   cap.set(cv2.CAP_PROP_FPS, 30)

   if record_frame=='y':
      # 保存用
      fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
      #frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
      width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
      height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
      size = (width, height)
      vw = cv2.VideoWriter(OUT_FILE, fmt, record_fps, size)

   count=0
   print("# Input 'q' to stop the camera.")
   now=time.time()
   start=now
   key=keyin.Keyboard()
   ch='c'  
   ch_im=cv2.waitKey(1)
   while not(ch=='q' or ch_im==ord('q') or ch=='Q' or ch_im==ord('Q')):
      # take frame
      ret, frame = cap.read()
      fr_h,fr_w=frame.shape[:2]
      kx=int(1/mozic);ky=int(1/mozic)
      # モザイク処理
      small=cv2.resize(frame,dsize=None,fx=mozic,fy=mozic,interpolation=cv2.INTER_NEAREST)
      img=cv2.resize(small,dsize=(fr_w,fr_h),interpolation=cv2.INTER_NEAREST)
      '''
      # フィルタリングを行う。
      kernel = np.ones((kx,ky))
      kernel=kernel/(kx*ky)
      img = cv2.filter2D(frame, -1, kernel)
      '''
      x=int(WIDTH/2);y=int(HEIGHT/2)
      rgb=area(img,x,y,kx,ky)
      print("\r %5d %5d %5d" % (rgb[0],rgb[1],rgb[2]),end='') 
      cv2.rectangle(img, tuple([x,y]), tuple([x+kx,y+ky]),(0,0,255),thickness=2)
      #rct=img[y:y+ky,x:x+kx]
      #cv2.imshow('rct'+str(kx)+'x'+str(ky),rct)
      #frame=cv2.rotate(frame,cv2.ROTATE_90_COUNTERCLOCKWISE)
      cv2.imshow('img'+str(WIDTH)+'x'+str(HEIGHT),img)
      ch_im=cv2.waitKey(1)
      ch=key.read()
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

else: # カメラが開けなかった場合
   print("# Camera is NOT opened.")
   print("# Connect and turn on USB camera.")
