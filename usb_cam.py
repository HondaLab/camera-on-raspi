#!/usr/bin/python3
import cv2
import os
import time
import modules.keyin as keyin
import numpy as np

#(640x360),(1280x720),(1440x1440),... for SP360 4K
WIDTH=1440
HEIGHT=1440
size = (WIDTH , HEIGHT)
disp_size = (720,720)
record_fps=10 # システムのスピードに応じて変更する必要あり
camera_dev='/dev/video2'

camera_mirror = "n"       # 反転して映る際はyesに変更      
show_version = "y"        # pythonとopencvのバージョンを確認する場合はyes
save_fig = "n"            # 静止画保存
imshow = "y"              # キャプチャー画像を見る場合はyes
calibration = "n"         # センターキャリブレーション
rotation = "y"            # キャプチャ画像を回転
camera_check = "n"        # 接続されているカメラの番号を調べる
triming = "y"             # 指定箇所を切り抜き


# 撮影する画像を回転させる角度
# ラジアンではなく，角度(°)ディグリー
ANGLE =3

# 拡大比率
SCALE = 1.0


#キャリブレーションするときのレンジ
calib_range = 100
calib_start_x = (WIDTH//2) - (calib_range//2)
calib_start_y = (HEIGHT//2) - (calib_range//2)

#画像切り抜きのサイズ
triming_range = 600
triming_start_x = (WIDTH//2) - (triming_range//2)
triming_start_y = (HEIGHT//2) - (triming_range//2)


def check_camera_connection():
    """
    接続されているカメラをチェックする
    sys.exitで強制的に抜け出す
    """

    print('接続されているカメラの番号を調べています...')
    true_camera_is = []  # 空の配列を用意
    cam_number = []

    # カメラ番号を0～9まで変えて、COM_PORTに認識されているカメラを探す
    for camera_number in range(0, 10):
        try:
            cap = cv2.VideoCapture(camera_number)
            ret, frame = cap.read()
        except:
            ret = False
        if ret == True:
            true_camera_is.append(camera_number)
            print("カメラ番号->", camera_number, "接続済")

            cam_number.append(camera_number)
        else:
            print("カメラ番号->", camera_number, "未接続")
    print("接続されているカメラは", len(true_camera_is), "台です。")
    print("カメラのインデックスは", true_camera_is,"です。")
    sys.exit("カメラ番号を調べ終わりました。")
    return 0


if camera_check == "y":
    check_camera_connection()



# open camera
#cap = cv2.VideoCapture(camera_dev, cv2.CAP_V4L2)
cap = cv2.VideoCapture(2)
if cap.isOpened(): # カメラが開けた場合
   save_video=input('# 録画しますか(y/n default=y)')
   if save_video=='':
      save_video='y'
   if save_video=='y':
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
   #cap.set(cv2.CAP_PROP_BUFFERSIZE, 10) # BUFFERSIZE を小さくするとレートが速くなる
   cap.set(cv2.CAP_PROP_FPS, 30)

   if save_video=='y':
      # 保存用
      fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
      #frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
      WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
      HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
      size = (WIDTH, HEIGHT)
      vw = cv2.VideoWriter(OUT_FILE, fmt, record_fps, size)

   count=0
   print("# Input 'q' to stop the camera.")
   now=time.time()
   start=now
   key=keyin.Keyboard()
   ch='c'  
   ch_im=cv2.waitKey(1)
   while not(ch=='q' or ch_im==ord('q') or ch=='Q' or ch_im==ord('Q')):
      ret, frame = cap.read()

      if camera_mirror == "y":
         frame = frame[:,::-1]

      if save_fig == "y":
         cap_time = dt.datetime.now()
         cap_time = str(cap_time.strftime('%y%m%d_%H%M%S'))
         cap_time = cap_time.replace("'",'')
         picname = cap_time+".png"
         cv2.imwrite(picname, frame)


      if rotation == "y":
           #回転させる処理
         center2 = tuple(np.array([frame.shape[1] * 0.5, frame.shape[0] * 0.5]))
         rotation_matrix = cv2.getRotationMatrix2D(center2, ANGLE, SCALE)
         frame = cv2.warpAffine(frame, rotation_matrix, size, flags=cv2.INTER_CUBIC)
         #frame = cv2.resize(frame, disp_size)

      if triming == "y":
         frame = frame[triming_start_x:triming_start_x + triming_range , triming_start_y:triming_start_y + triming_range]
         frame = cv2.resize(frame, disp_size)

      if save_video == "y":
         vw.write(frame)

      if calibration == "y":
           #キャプチャ画像のセンターを表示する処理
         frame = frame[calib_start_x:calib_start_x + calib_range , calib_start_y:calib_start_y + calib_range]
         #frame = cv2.resize(frame, disp_size)



      if imshow == "y":
         cv2.imshow("camera", frame)
         if cv2.waitKey(1) & 0xFF == ord('q'):
            break
      count+=1
      now=time.time()
      #time.sleep(0.1)

   now=time.time()
   rate=count/(now-start)
   speed=1.0/rate*1000
   print("rate=%5.2f (Hz)" % rate)
   print("speed=%5.2f (msec)" % speed)

   if save_video=='y':
      print("%sに%7.2f(sec) 録画されました" % (OUT_FILE,now-start))
      vw.release()
   # release camera
   cap.release()

else: # カメラが開けなかった場合
   print("# Camera is NOT opened.")
   print("# Connect and turn on USB camera.")
