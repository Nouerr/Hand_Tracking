import cv2 
import mediapipe as mp

capture = cv2.VideoCapture(0)

mphands = mp.solutions.hands
hands = mphands.Hands()
mpdraw = mp.solutions.drawing_utils
tipids=[4,8,12,16,20]

while True :
    success, pic = capture.read()
    #pic =cv2.flip(pic,0)
 
    picRgb= cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)

    results = hands.process(picRgb)
    lmlist=[]

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id,lm in enumerate (handLms.landmark):
                h,w,c =pic.shape
                cx , cy=int (lm.x * w) ,int (lm.y * h)
                lmlist.append([id,cx,cy])
                #print(lmlist)
                mpdraw.draw_landmarks(pic,handLms,mphands.HAND_CONNECTIONS)
                
                if id==8:
                    cv2.circle(pic,(cx , cy),10,(0,255,0),cv2.FILLED)

                if len(lmlist)==21:
                    fingers=[]
                    if lmlist [tipids[0]][1] <lmlist[tipids[0]-2][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                    for tip in range (1,5):
                        if lmlist [tipids[tip]][2] <lmlist[tipids[tip]-2][2]:
                            fingers.append(1)
                        else:
                            fingers.append(0)
                    #print(fingers)

                    totalfingers =fingers.count(1)
                    print(totalfingers)
                    cv2.putText(pic,f'{totalfingers}',(40,80),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,3,(0,255,0),4)

        
    cv2.imshow('Hand Tracker' , pic)
    if cv2.waitKey(5) & 0xff==27 :
        break
