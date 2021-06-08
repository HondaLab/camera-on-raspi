ラズパイに接続したPicamera や Debian PCにつないだUSBカメラから，OpenCVで画像処理する．

### usb_cam.py: USBカメラ用
 * camera_dev='/dev/video0' : カメラデバイス．複数カメラがある場合など，/dev/video1 を使うときもある
 * record_fps=4 : 録画のフレームレートはimshowだけより落ちるので，観測値にあわせて指定する．
