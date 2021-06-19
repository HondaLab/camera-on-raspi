#!/usr/bin/python3
# Only read image from picamera (Yasushiu Honda 2021 6/20)

import cv2
import time
import picamera
import picamera.array

# 解像度 (ex. 640x480, 320x240)
WIDTH=320
HEIGHT=320

# Picameraを初期化する
cam = picamera.PiCamera()
cam.framerate = 30
#cam.brightness = 50
#cam.saturation = 50

# いったんホワイトバランスをオートにする
cam.awb_mode='auto'
time.sleep(1)
# 途中で色味が変化しないようにホワイトバランスを固定する
g = cam.awb_gains
cam.awb_mode = 'off'
cam.awb_gains = g

cam.iso=800
cam.shutter_speed=1000000
cam.exposure_mode = 'off' # off, auto, fixedfps

cam.resolution = (WIDTH, HEIGHT)
cam.rotation=0
cam.meter_mode = 'average' # average, spot, backlit, matrix
cam.exposure_compensation = 0

# キャプチャー用のRGB配列を用意する
rgb=picamera.array.PiRGBArray(cam, size=(WIDTH, HEIGHT))
rgb.truncate(0) # clear the stream for next frame

# camera capture loop
key=cv2.waitKey(1) & 0xFF
while key!=ord('q'):
   # rgb.arrayに画像を取り込む
   cam.capture(rgb, format="bgr", use_video_port="True")
   frame = rgb.array

   x=int(WIDTH/2); y=int(HEIGHT/2)
   print("\r %5d" % frame[y,x,0],end='')

   cv2.imshow('image',frame)

   key=cv2.waitKey(1) & 0xFF
   rgb.truncate(0) # clear the stream for next frame

cv2.destroyAllWindows()
