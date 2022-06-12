# Import required modules
from os import listdir
import cv2
import math
import datetime
import time
import argparse
import csv

def getFaceBox(net, frame, conf_threshold=0.7):
    frameOpencvDnn = frame.copy()
    frameHeight = frameOpencvDnn.shape[0]
    frameWidth = frameOpencvDnn.shape[1]
    blob = cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)

    net.setInput(blob)
    detections = net.forward()
    bboxes = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            x1 = int(detections[0, 0, i, 3] * frameWidth)
            y1 = int(detections[0, 0, i, 4] * frameHeight)
            x2 = int(detections[0, 0, i, 5] * frameWidth)
            y2 = int(detections[0, 0, i, 6] * frameHeight)
            bboxes.append([x1, y1, x2, y2])
            cv2.rectangle(frameOpencvDnn, (x1, y1), (x2, y2), (0, 255, 0), int(round(frameHeight/150)), 8)
    return frameOpencvDnn, bboxes


parser = argparse.ArgumentParser(description='Use this script to run age and gender recognition using OpenCV.')
parser.add_argument('--input', help='Path to input image or video file. Skip this argument to capture frames from a camera.')
parser.add_argument('--device', default='cpu', help='Device to inference on')

args = parser.parse_args()

faceProto = './model/opencv_face_detector.pbtxt'
faceModel = './model/opencv_face_detector_uint8.pb'

ageProto = './model/age_deploy.prototxt'
ageModel = './model/age_net.caffemodel'

genderProto = './model/gender_deploy.prototxt'
genderModel = './model/gender_net.caffemodel'

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
genderList = ['Male', 'Female']

# Load network
ageNet = cv2.dnn.readNet(ageModel, ageProto)
genderNet = cv2.dnn.readNet(genderModel, genderProto)
faceNet = cv2.dnn.readNet(faceModel, faceProto)


if args.device == 'cpu':
    ageNet.setPreferableBackend(cv2.dnn.DNN_TARGET_CPU)
    genderNet.setPreferableBackend(cv2.dnn.DNN_TARGET_CPU)    
    faceNet.setPreferableBackend(cv2.dnn.DNN_TARGET_CPU)

    print('Using CPU device')

elif args.device == 'gpu':
    ageNet.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    ageNet.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

    genderNet.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    genderNet.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

    genderNet.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    genderNet.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
    print('Using GPU device')

#CSV出力用
today = datetime.date.today()
f = open(f'./data/{today}.csv','a')
csvWriter = csv.writer(f)

#時間計測・結果判定用の変数定義
start = None
end = 0
elapsed_time = 0
genResult = [0] * 2
ageResult = [0] * 8

# Open a video file or an image file or a camera stream
cap = cv2.VideoCapture(args.input if args.input else 0) #取得するカメラ映像はelse以下の番号で調整
padding = 20

def add_data_csv(gender, age, elapsed_time):
    output_time = datetime.datetime.now()
    print(f'output_time{output_time}')
    print(f'Gender: {gender}')
    print(f'Age: {age}')
    print(f'elapsed_time:{elapsed_time}')
    print(f'end:{end}')        
    listData = [output_time, gender, age, elapsed_time]
    csvWriter.writerow(listData)

# while cv2.waitKey(1) < 0:
while True:
    # Read frame            
    start = time.time()
    ret, frame = cap.read()
    if not ret:
        cv2.waitKey(0)
        break

    frameFace, bboxes = getFaceBox(faceNet, frame)
    if not bboxes:
        print('No face Detected, Checking next frame')
        k = cv2.waitKey(1)
        if k == 27:
            add_data_csv(gender, age, elapsed_time)
            break
        continue

    #検出に間が空いた場合、別の顧客とみなして結果を出力、変数を初期値に
    if end != 0 and start - end >1 :
        add_data_csv(gender, age, elapsed_time)

        print(f'genResult: {genResult}')
        print(f'ageResult: {ageResult}')
        print(f'elapsed_time: {elapsed_time}')

        genResult = [0] * 2
        ageResult = [0] * 8
        elapsed_time = 0

    for bbox in bboxes:
        # print(bbox)
        face = frame[max(0,bbox[1]-padding):min(bbox[3]+padding,frame.shape[0]-1),max(0,bbox[0]-padding):min(bbox[2]+padding, frame.shape[1]-1)]

        blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
        genderNet.setInput(blob)
        genderPreds = genderNet.forward()
        genResult = genResult+ genderPreds
        gender = genderList[genResult[0].argmax()]
        # print(f'Gender Output : {genderPreds}')
        # print(f'Gender : {gender}, conf = {genderPreds[0].max():.3f}')

        ageNet.setInput(blob)
        agePreds = ageNet.forward()
        ageResult = ageResult + agePreds
        age = ageList[ageResult[0].argmax()]        
        # print(f'Age Output : {agePreds}')
        # print(f'Age : {age}, conf = {agePreds[0].max():.3f}')

        label = '{},{},{}[s]'.format(gender, age, int(elapsed_time))
        #cv2.putText(frameFace, label, (bbox[0], bbox[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv.LINE_AA)
        cv2.putText(frameFace, label, (bbox[0], bbox[1]+20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow('customer analyzer', frameFace)
        #cv2.imwrite('age-gender-out-{}'.format(args.input),frameFace)
    end = time.time()
    elapsed_time = elapsed_time + (end - start)
    # print(f'time : {elapsed_time:.3f}')
    # print(f'genResult Output :{genResult}')
    # print(f'ageResult Output :{ageResult}')

    k = cv2.waitKey(1)
    if k == 27:
        add_data_csv(gender, age, elapsed_time)
        break

# cmake -DCMAKE_BUILD_TYPE=RELEASE -DCMAKE_INSTALL_PREFIX=~/opencv_gpu -DINSTALL_PYTHON_EXAMPLES=OFF -DINSTALL_C_EXAMPLES=OFF -DOPENCV_ENABLE_NONFREE=ON -DOPENCV_EXTRA_MODULES_PATH=~/cv2_gpu/opencv_contrib/modules -DPYTHON_EXECUTABLE=~/env/bin/python3 -DBUILD_EXAMPLES=ON -DWITH_CUDA=ON -DWITH_CUDNN=ON -DOPENCV_DNN_CUDA=ON  -DENABLE_FAST_MATH=ON -DCUDA_FAST_MATH=ON  -DWITH_CUBLAS=ON -DCUDA_TOOLKIT_ROOT_DIR=/usr/local/cuda-10.2 -DOpenCL_LIBRARY=/usr/local/cuda-10.2/lib64/libOpenCL.so -DOpenCL_INCLUDE_DIR=/usr/local/cuda-10.2/include/ ..