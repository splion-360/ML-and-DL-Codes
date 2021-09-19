import cv2
import mediapipe
import time
import warnings
import math
import serial
warnings.filterwarnings("ignore")
board = serial.Serial('COM4', 9600)
class Detector:
    def __init__(self, mode = False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mphands = mediapipe.solutions.hands
        self.hands = self.mphands.Hands(mode,maxHands,detectionCon,trackCon)
        self.mpdraw = mediapipe.solutions.drawing_utils

    def findhand(self, img, draw=True):
        imgrgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgrgb)
        if self.results.multi_hand_landmarks:
            for self.handlms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpdraw.draw_landmarks(img, self.handlms, self.mphands.HAND_CONNECTIONS)
        return img

    def findposition(self, img,draw=True):
        lmlist = []
        if self.results.multi_hand_landmarks:
            for id, lm in enumerate(self.handlms.landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id,cx,cy])

                if draw:
                    cv2.circle(img,(cx,cy),15,(255,0,255),thickness = -1)

        return lmlist

    def linedraw(self,img,lmlist):
        if len(lmlist) == 0:
            return

        lpt1 = lmlist[4]
        lpt2 = lmlist[8]

        cv2.line(img, (lpt1[1], lpt1[2]), (lpt2[1], lpt2[2]), (0, 0, 255), thickness=1)
        cv2.circle(img,(lpt1[1],lpt1[2]),5,(0,0,255),thickness = -1)
        cv2.circle(img, (lpt2[1], lpt2[2]), 5, (0, 0, 255), thickness=-1)
        midx, midy = int((lpt1[1] + lpt2[1]) / 2), int((lpt1[2] + lpt2[2]) / 2)
        cv2.circle(img,(midx,midy),5,color=(0,0,255),thickness = -1)
        distance = math.hypot(lpt2[1]-lpt1[1],lpt2[2]-lpt1[2])

        if distance < 50:
            cv2.circle(img, (midx, midy), 5, color=(0, 255, 0), thickness=-1)

        return int(distance)

    def sendsignal(self, x):

        if (x <= 50):
            board.write(b'1')
        elif (x > 50):
            board.write(b'0')

def main():
    cap = cv2.VideoCapture(0)
    detector = Detector()
    ptime = 0
    while True:
        state, img = cap.read()
        img = detector.findhand(img, draw=False)
        lmlist = detector.findposition(img, draw=False)
        distance = detector.linedraw(img, lmlist)
        if distance!=None:
            detector.sendsignal(distance)

        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), thickness=4)
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0XFF == ord('q'):
            break
    cv2.destroyAllWindows()
    return
if __name__  ==  '__main__':
    main()
