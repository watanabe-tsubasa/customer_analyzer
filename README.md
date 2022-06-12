# customer_analyzer

<img src="https://static.camp-fire.jp/uploads/editor_uploaded_image/image/2108069/9b1c0328e8dc4bca9dc8db460e75bb7b.png?ixlib=rails-2.1.4&fit=max&auto=format" width=50%>

## はじめに
本プログラムは、小売業における店頭での顧客分析用に開発を進めている、OSSのAIカメラプロトタイプであり、以下のGitHubリポジトリのファイルをベースに作成させていただいております。
https://github.com/spmallick/learnopencv/tree/master/AgeGender

また、本リポジトリは
https://camp-fire.jp/projects/view/530144?list=channel_sparks
こちらのクラウドファンディングにてご支援いただいた方向けに、案内させていただいております。

商用利用や二次配布等、ご遠慮くださいますようお願いします。  

## 必要な準備
1. プログラムファイルのダウンロード（わかる方は`git clone`で問題ありません）
2. `Python`のインストール
3. `Python`ライブラリ `OpenCV`のインストール

### ■ プログラムファイルのダウンロード

- リポジトリ内緑色のボタン`Code`の矢印をクリックし、表示される`Download ZIP`をクリック
- ダウンロードされるZIPファイルを回答してください

<img src='https://i.gyazo.com/0f25ebaf3f3c0df6cd396239d625e09d.png' width=75%>

- お好きな場所にフォルダーをダウンロードしてください。こだわりがなければデスクトップで問題ありません
- 作成したフォルダーの中に、ファイルがダウンロードされていることを確認してください

`Customer_Analyzer`フォルダー直下

> camera.py  
> customer_analyzer.py  

`model`フォルダー内

> age_deploy.prototxt  
> age_net.caffemodel  
> gender_deploy.prototxt  
> gender_net.caffemodel  
> opencv_face_detector_uint8.pb  
> opencv_face_detector.pbtxt  

空の`data`フォルダーは削除しないでください

### ■ Pythonのインストール / OpenCVのインストール
#### OS別仕様書
利用環境に応じて、ご参照ください
- [for windows](https://qiita.com/watanabe-tsubasa/items/15f84224b04ad754d2f9)：作成中
- [for mac](https://qiita.com/watanabe-tsubasa/private/2a245fc06a2f678ff584)：作成中
- [for Raspberry Pi](https://qiita.com/watanabe-tsubasa/private/332d6d7a05d630b62c7b)：作成中
- [for Jetson Nano](https://qiita.com/watanabe-tsubasa/private/ad4eacff22f5d583cb6f)：作成中

## 利用方法

**より詳細な利用方法は、OS別仕様書に記載します。**

### ■ データの取得
- コマンドプロンプトやターミナルで`customer_analyzer.py`のファイルをPythonで実行してください
- カメラで顔が認識されると、PC上に画像が表示されます
- 終了する際は、画像が表示されているウィンドウをクリックして`esc`キーを押してください
- 不具合が起きた場合、コマンドプロンプトやターミナルをクリックして`control` + `C` で強制終了してください
- `data`フォルダー内に結果がcsvファイルで出力されます

### ■ カメラ位置の調整
- 実際に店頭に設置するなど、カメラの映像を見る際には`camera.py`のファイルをPythonで実行してください
- 認識したいお客さまの顔が映るように、カメラ位置を調整してください
- 終了する際は、画像が表示されているウィンドウをクリックして`esc`キーを押してください

### ■ 画像取得するカメラの変更
PC備え付けのwebカメラやUSBカメラなど、複数のwebカメラがPCに接続されている場合、以下の手順で取得するwebカメラを選択することが可能です。
#### camera.py
- 7行目 `cap = cv2.VideoCapture(0)`0を1や2など他の数字に変えると、取得する映像を変更できます
- 番号に該当するカメラが存在しない場合、エラーが出るので元の数字に戻してください。

#### customer_analyzer.py
- 87行目 `cap = cv2.VideoCapture(args.input if args.input else 0)` 0を1や2など他の数字に変えると、取得する映像を変更できます
- 番号に該当するカメラが存在しない場合、エラーが出るので元の数字に戻してください。

## 更新情報

- 6/12 version 1.0 release