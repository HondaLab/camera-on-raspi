ラズパイに接続したPicamera や Debian PCにつないだUSBカメラから，OpenCVで画像処理する．

### Requirements
 * apt-get install python3-opencv

### usb_cam.py: USBカメラ用
 * camera_dev='/dev/video0' : カメラデバイス．複数カメラがある場合など，/dev/video1 を使うときもある
 * record_fps=4 : 録画のフレームレートはimshowだけより落ちるので，観測値にあわせて指定する．
 
# 山田が改変した部分の説明(usb_cam.py)

## カメラのデバイスインデックスについて．

camera_devはカメラ1つにつき2つ生成される．ノートPCの内蔵カメラであれば，video0,video1が作成される．
次に接続されたUSBカメラはvideo2,video3となる．

## カメラチェック機能

私が作成したプログラムでは，接続されているカメラをチェックする機能を実装している．
23行目のcamera_checkをyesとすると，接続されているカメラの番号を返す仕様としている．
sys.exit()でプログラムから抜け出す仕様となっている．

## プログラムの仕様
様々な機能を追加しています．

camera_mirror = "n"       # 反転して映る際はyesに変更(主に内蔵カメラ使用時)
show_version = "y"        # pythonとopencvのバージョンを確認する場合はyes
save_fig = "n"            # 静止画保存
imshow = "y"              # キャプチャー画像を見る場合はyes
calibration = "n"         # センターキャリブレーション
rotation = "y"            # キャプチャ画像を回転
camera_check = "n"        # 接続されているカメラの番号を調べる
triming = "y"             # 指定箇所を切り抜き


## 諸注意

122行目のVideoWriterに与える引数の4つ目の引数は注意である．
保存するサイズと実際の動画のサイズが異なると，動画を撮影しても，再生することができなくなります．
その場合は，print(frame.shape)でframeのサイズを確認してください．
