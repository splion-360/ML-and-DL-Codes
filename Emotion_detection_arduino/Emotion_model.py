import cv2
import numpy as np
from tensorflow.keras.models import load_model
import time
time.sleep(0.5)
cap = cv2.VideoCapture(0)
model = load_model('/home/surya/Desktop/Kaggle/em_best.h5')
face_cascade = cv2.CascadeClassifier('/home/surya/Desktop/Opencv/Computer-Vision-with-Python/DATA/haarcascades/haarcascade_frontalface_default.xml')

def detect_face(img,text):
    img_copy = img.copy()

    rect_cd = face_cascade.detectMultiScale(img_copy,scaleFactor=2,minNeighbors=1)
    fontFace = cv2.FONT_HERSHEY_SIMPLEX
    for (x,y,w,h) in rect_cd:
        cv2.rectangle(img_copy,(x,y),(x+w+25,y+h+25),color=(0,0,255),thickness=5)
        cv2.putText(img_copy,text=text,org=(400,400),fontFace=fontFace,fontScale=2,color=(255,0,0),thickness=2)
    return img_copy

def emotion_det(img):
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    modimage = cv2.resize(img,(48,48))
    modimage = np.expand_dims(modimage,axis=0)
    modimage = np.expand_dims(modimage, axis=3)
    emotion_dict = {0: 'angry', 1: 'fear', 2: 'happy', 3: 'neutral', 4: 'sad', 5: 'surprise'}
    predict = model.predict_classes(modimage)[0]
    return emotion_dict[predict]
start_time = time.time()
delay = 5
while True :
    ret,frame = cap.read()
    if time.time()-start_time > 5:
        frame_copy = frame.copy()
        emotion = emotion_det(frame_copy)
        img = detect_face(frame_copy,text=emotion)
        cv2.imshow('Face',img)
    start_time = time.time()
        if cv2.waitKey(2) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

