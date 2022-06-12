import cv2
# numpyは画像データの格納に必要です。
import numpy as np


def camera():
    cap = cv2.VideoCapture(0) #この番号を変更して、取得するカメラを変更
    isOpened = cap.isOpened()
    if not isOpened:
        return
    while True:
        result, frame = cap.read()
        if not result:
            return
        # 画像表示
        cv2.imshow('camera', frame)
        # キー入力受付
        key = cv2.waitKey(1)
        # 終了キー（EnterかEscで終了）
        if (key == 13) or (key == 27):
            break
    # カメラ終了
    cap.release()
    cv2.destroyAllWindows()

camera()