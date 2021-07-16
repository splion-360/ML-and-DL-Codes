import cv2
import numpy as np
from tensorflow.keras.models import load_model
#from Serial_check import *
(x,y,w,h) = (0,0,0,0)
import time
cap = cv2.VideoCapture(0)
model = load_model('/home/surya/Desktop/Kaggle/em_best.h5')
print("Communication Started")
face_cascade = cv2.CascadeClassifier('/home/surya/Desktop/Opencv/Computer-Vision-with-Python/DATA/haarcascades/haarcascade_frontalface_default.xml')

def detect_face(img):
    img_copy = img.copy()

    rect_cd = face_cascade.detectMultiScale(img_copy,scaleFactor=2,minNeighbors=1)

    for (x,y,w,h) in rect_cd:
        cv2.rectangle(img_copy,(x,y),(x+w+25,y+h+25),color=(0,0,255),thickness=5)

    return img_copy,rect_cd

def emotion_det(img,cord):
    global x,y,w,h
    img_copy = img.copy()
    for (x,y,w,h) in cord:
        (x,y,w,h) = (x,y,w,h)
    img_copy = img_copy[y:y+h,x:x+w]
    fontFace = cv2.FONT_HERSHEY_SIMPLEX
    img_copy = cv2.cvtColor(img_copy,cv2.COLOR_BGR2GRAY)
    modimage = cv2.resize(img_copy,(48,48))
    modimage = np.expand_dims(modimage,axis=0)
    modimage = np.expand_dims(modimage, axis=3)
    modimage = modimage/255.0
    emotion_dict = {0: 'angry', 1: 'fear', 2: 'happy', 3: 'neutral', 4: 'sad', 5: 'surprise'}
    predict = model.predict_classes(modimage)[0]
    text = emotion_dict[predict]
    cv2.putText(img, text=text, org=(400, 400), fontFace=fontFace, fontScale=2, color=(255, 0, 0), thickness=2)
    return img

while True :
    ret,frame = cap.read()
    frame_copy = frame.copy()
    img,cord = detect_face(frame_copy)
    img = emotion_det(img,cord)
    cv2.imshow('Face',img)

    if cv2.waitKey(2) & 0xFF == ord('q'):
        break

    #msg(emotion)



cap.release()
cv2.destroyAllWindows()