import cv2
import numpy as np
import time
import HandTrackingModule as htm
import os

folderPath = "header"
mylist = os.listdir(folderPath)
print(mylist)
overlayList = []
#######################
brushThickness = 25
eraserThickness = 150
########################
for imgPath in mylist:
    image = cv2.imread(f'{folderPath}/{imgPath}')
    overlayList.append(image)
print(len(overlayList))
header = overlayList[0]

drawColor=(0,0,255)
cap = cv2.VideoCapture(1)
cap.set(3, 1280)
cap.set(4, 720)

detector = htm.handDetector(detectionCon=0.45, maxHands=1)
xp, yp = 0, 0
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

while True:
    success, img = cap.read()
    # img = cv2.flip(img, 1)
    img = detector.findHands(img)
    
    # Handle the case where findPosition returns both landmarks and bounding box
    lmList, bbox = detector.findPosition(img, draw=False)
    
    if len(lmList) != 0:
        # print("Landmark List:", lmList)
        # print("Number of landmarks:", len(lmList))
        
        if len(lmList) > 12:  # Ensure lmList has at least 13 landmarks (0-12)
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]

            # 3. Check which fingers are up
            fingers = detector.fingersUp()
            # print("Fingers:", fingers)

            if isinstance(fingers, list) and len(fingers) == 5:
                # Your logic here using x1, y1, x2, y2, and fingers
                if fingers[1] and fingers[2]:
                    xp, yp = 0, 0
                    if y1 < 142:
                        print(x1)
                        if 70 < x1 < 230:
                           header = overlayList[4]
                           print("red")
                           drawColor = (0, 0, 255)
                        elif 240 < x1 < 430:
                            header = overlayList[3]
                            print("green")
                            drawColor = (0, 255, 0)
                        elif 440 < x1 < 620:
                            header = overlayList[1]
                            print("blue")
                            drawColor = (255, 0, 0)
                        elif 660 < x1 < 880:
                            header = overlayList[2]
                            print("eraser")
                            drawColor = (0, 0, 0)
                    cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)
                    # print("selection mofe")

                if fingers[1] and fingers[2]==False:
                    cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
                    print("Draw Mode")   
                    if xp == 0 and yp == 0:
                       xp, yp = x1, y1     
                    cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
                    xp, yp = x1, y1


  






                # pass
            else:
                print("Unexpected output from fingersUp():", fingers)
        else:
            print("lmList does not contain enough landmarks")
    




    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img,imgInv)
    img = cv2.bitwise_or(img,imgCanvas)

    img[0:142, 0:1280] = header
    cv2.imshow("Image", img)
    cv2.imshow("Canvas", imgCanvas)

    cv2.waitKey(1)
