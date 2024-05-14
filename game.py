#importing packages
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
import random

def GamePlay(PlayerName):


    # capturing the video
    video_cap = cv2.VideoCapture(0)
    video_cap.set(3, 640) #width
    video_cap.set(4, 480) #height

    # defining the hand detection module
    detector = HandDetector(maxHands=1)

    #setting up game
    timer = 0
    stateResults = False
    startGame = False
    scores = [0,0]  #[AI, Player]


    while True:
        # importing images
        bg = cv2.imread("resources/bg.jpg")
        success, img = video_cap.read()

        # scaling the image down
        imgScaled = cv2.resize(img,(0,0), None, 0.640, 0.640 )
        imgScaled = imgScaled[:, 80:360]

        # finding hands
        hands, img = detector.findHands(imgScaled) 

        if startGame:

            if stateResults is False:
                timer = time.time() - initialTime
                cv2.putText(bg, str(int(timer)),(440,330), cv2.FONT_HERSHEY_PLAIN,6,(255,0,255),4 )

                if timer > 3:
                    stateResults = True 
                    timer = 0

                    if hands:
                        hand = hands[0]
                        fingers = detector.fingersUp(hand)

                        # players move
                        playerMove = 0
                        if fingers == [0,0,0,0,0]:
                            playerMove = 1
                        if fingers == [1,1,1,1,1]:
                            playerMove = 2
                        if fingers == [0,1,1,0,0]:
                            playerMove = 3

                        # AI move
                        randomNumber = random.randint(1,3) 
                        imgAI = cv2.imread(f"Resources/{randomNumber}.png", cv2.IMREAD_UNCHANGED)
                        bg  = cvzone.overlayPNG(bg, imgAI, (110,249))

                        # finding winner
                        # player wins
                        if(playerMove == 1 and randomNumber ==3) or (playerMove == 2 and randomNumber == 1) or (playerMove == 3 and randomNumber == 2):
                            scores[1] += 1

                        # AI wins
                        if(playerMove == 3 and randomNumber ==1) or (playerMove == 1 and randomNumber == 2) or (playerMove == 2 and randomNumber == 3):
                            scores[0] += 1

        # putting scores
        cv2.putText(bg, str(scores[0]),(310,160), cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),5 )
        cv2.putText(bg, str(scores[1]),(835,160), cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),5 )

        #putting player name
        cv2.putText(bg, PlayerName,(610,160), cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),5 )

        # putting scaled image on the background
        bg[178:485,602:882] = imgScaled

        # putting the AI move image
        if stateResults:
            bg  = cvzone.overlayPNG(bg, imgAI, (110,240))
    
    
        cv2.imshow('BG', bg)

        key = cv2.waitKey(1)  
        if key == ord('s'):
            startGame = True
            initialTime = time.time()
            stateResults = False
        if key == ord('q'):
            break

    video_cap.release()
    cv2.destroyAllWindows()

