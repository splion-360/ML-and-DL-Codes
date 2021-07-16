import cv2
import numpy as np
from tensorflow.keras.models import load_model
cap = cv2.VideoCapture(0)
model = load_model('/home/surya/Downloads/Sign_language_model.h5')
print("Communication Started")
sign_dict = {'0': 0,
             '1': 1,
             '2': 2,
             '3': 3,
             '4': 4,
             '5': 5,
             '6': 6,
             '7': 7,
             '8': 8,
             '9': 9,
             'unknown': 10}
sign_dict = {v:k for k,v in sign_dict.items()}
def put_bounding_box(img):
    x,y,w,h = 85,85,350,350
    cv2.rectangle(img,(y,x),(y+h,x+w),color=(0,0,255),thickness=5)
    return img,(x,y,w,h)

def sign_det(img,cord):
    (x,y,w,h) = cord
    img_copy = img.copy()
    img_copy = img_copy[y:y+h,x:x+w]
    img_copy= cv2.cvtColor(img_copy,cv2.COLOR_BGR2GRAY)
    fontFace = cv2.FONT_HERSHEY_SIMPLEX
    modimage = cv2.resize(img_copy,(90,82))
    modimage = modimage/255.0
    modimage = np.expand_dims(modimage,axis=0)
    modimage = np.expand_dims(modimage, axis=3)
    predict = model.predict_classes(modimage)[0]
    text = sign_dict[predict]
    cv2.putText(img, text=text, org=(50,50), fontFace=fontFace, fontScale=2, color=(255, 0, 0), thickness=2)
    return img

while True :
    ret,frame = cap.read()
    frame_copy = frame.copy()
    empty_img,(x,y,w,h) = put_bounding_box(frame_copy)
    cord = (x,y,w,h)
    img = sign_det(empty_img,cord)
    cv2.imshow('Sign',img)
    if cv2.waitKey(2) & 0xFF == ord('q'):
        break

    #msg(emotion)



cap.release()
cv2.destroyAllWindows()