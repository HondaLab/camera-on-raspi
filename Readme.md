ラズパイに接続したPicamera や Debian PCにつないだUSBカメラから，OpenCVで画像処理する．

### Requirements
 * apt-get install python3-opencv

### usb_cam.py: USBカメラ用
 * camera_dev='/dev/video0' : カメラデバイス．複数カメラがある場合など，/dev/video1 を使うときもある
 * record_fps=4 : 録画のフレームレートはimshowだけより落ちるので，観測値にあわせて指定する．

### picam.py
ラズパイのカメラインターフェイスにつないだPiカメラから画像を取り込むためのコード．
PI_CAMERA という名前のクラスにしてあるので，このコードをmoduleとしてimportして他の
プログラムからも使うことができる．

captureメソッドで，画像フレームがリターンされる．

OpenCVのVideoWriterを使ってキャプチャーしたフレームをmp4動画として/tmpに保存
する例を__main__のなかに示した．



