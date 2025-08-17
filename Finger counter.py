import cv2 as cv
import os
import mediapipe as mp
import HandTracking as ht

# Start webcam
webcam = cv.VideoCapture(0)
detector = ht.handDetector()

# import our images
FolderPath = r"Hands Images"
myList = os.listdir(FolderPath)

# create list of images
overlayList = []
for imgPath in myList:
    image = cv.imread(f'{FolderPath}/{imgPath}')
    overlayList.append(image)

while True:
    # Read the Frame
    isTrue, frame = webcam.read()
    frame = cv.flip(frame, 1)

    # Detect hands
    frame = detector.findHands(frame)
    lmList = detector.findPosition(frame, draw=False)

    # Working with LandMarks for only the right hand
    tipsId = [4, 8, 12, 16, 20]

    if len(lmList) != 0 :
        fingers = []
        # working with Thumb
        if lmList[tipsId[0]][1] < lmList[tipsId[0] - 1][1]:
            fingers.append(True)
        else:
            fingers.append(False)

        # working for 4 fingers
        # lmList[finger_index][0,1,2]
        for id in range(1,5):
            if lmList[tipsId[id]][2] < lmList[tipsId[id]-2][2]:
                fingers.append(True)
            else:
                fingers.append(False)

        print(fingers)
        # Counting the number of fingers are open
        totalFingers = fingers.count(True)
        print(totalFingers)
        # showing the photo
        h, w, c = overlayList[totalFingers-1].shape
        frame[0:h, 0:w] = overlayList[totalFingers-1]



    # Show FPS
    frame = detector.showFPS(frame)
    cv.imshow('Hand Volume Control', frame)

    # Exit on ESC key
    if cv.waitKey(1) & 0xFF == 27:
        break

webcam.release()
cv.destroyAllWindows()