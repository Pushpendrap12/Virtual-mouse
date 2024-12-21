import cv2
import  numpy as np
import handtrackingmodule as htm
import time
import pyautogui
##########
wCam, hCam = 640, 480
frameR=100 #frame reduction
smoothening = 5
##############
cap = cv2.VideoCapture(0)

cap.set(3,640)
cap.set(4,480)
pTime = 0
plocx , plocy = 0,0
clocx, clocy = 0,0
detector = htm.handDetector(maxHands=1)
wScr ,hScr = pyautogui.size()
print(wScr,hScr)
while True:
    #1.Find the landmark
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    #2.get the tip of the index and middle
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        # print(x1, y1, x2, y2)
        #3. check which finger are up
        fingers = detector.fingersUp()
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
        # print(fingers)
        #4.only index finger :movig mode
        if fingers[1]==1 and fingers[2]==0:
            # 5. convert our cordinate
            x3=np.interp(x1,(frameR,wCam-frameR),(0,wScr))
            y3 = np.interp(x1, (frameR, hCam-frameR),(0, hScr))
            #6.smooothen the values
            clocx=plocx+(x3-plocx)/smoothening
            clocy=plocy+(y3-plocy)/smoothening
            #7.move Mouse
            pyautogui.moveTo(wScr-clocx,clocy)
            cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
            plocx,plocy=clocx,clocy
        #8.Both index are up : then it is clicking mode
        if fingers[1] == 1 and fingers[2] == 1:
            # 9.find distance between finegers
            length , img ,lineinfo= detector.findDistance(8,12,img)
            # 10click mouse if distance is short
            if length<40:
                cv2.circle(img,(lineinfo[4],lineinfo[5]),15,(0,255,0),cv2.FILLED)
                pyautogui.click()
    #11. Frame rate
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),3)
    #12. Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)