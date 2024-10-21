from cvzone.HandTrackingModule import HandDetector
import cv2
import numpy as np
import pyautogui
from random import *

cap = cv2.VideoCapture(0)

detector = HandDetector(detectionCon=0.8, maxHands=2)

size = [640, 480]
image = np.zeros((size[1], size[0], 3), np.uint8)

counter = np.ones((150, 300, 3), np.uint8)
counter[:, :, :] = 255

ball = [[], []]

record = 0
maxrecord = 0

snake = []
scr = 0
b = 51
g = 164
r = 105

b1 = 3
g1 = 212
r1 = 182

r2 = 230
b2 = 0
g2 = 0

k = 0
d = 0

def play():
    global image, i, ball, x1, y1, snake, scr, k, counter, n, record

    while True:
        counter[:, :, :] = 255
        image = np.zeros((pyautogui.size()[1] // 2 + pyautogui.size()[1] // 4, pyautogui.size()[0] // 2, 3), np.uint8)
        image[:, :, :] = (b, g, r)

        _, img = cap.read()
        img = cv2.flip(img, 90)
        img = cv2.resize(img, (pyautogui.size()[0]//2, pyautogui.size()[1] // 2 + pyautogui.size()[1] // 4))
        cv2.rectangle(image, (50, 50), (pyautogui.size()[0] // 2 - 50, pyautogui.size()[1] // 2 + pyautogui.size()[1] // 4 -50), (b + 50, g + 50, r + 50), 10)
        hands = detector.findHands(img, draw=False)

        if len(ball[0]) == 0:
            x1 = randint(100, pyautogui.size()[0] // 2 - 100)
            y1 = randint(100, pyautogui.size()[1] // 2 + pyautogui.size()[1] // 4 - 100)
            ball[0].append(x1)
            ball[1].append(y1)
        cv2.circle(image, (ball[0][0], ball[1][0]), 10, (b2, g2, r2), -1)

        if hands:
            hand1 = hands[0]
            lmlist1 = hand1["lmList"]
            bbox1 = hand1["bbox"]
            centerPoint1 = hand1['center']
            handType1 = hand1["type"]

            if len(snake)==0:
                snake.append(lmlist1[8])
            snake[0][0]=lmlist1[8][0]
            snake[0][1]=lmlist1[8][1]

            if scr == 1:
                for i in range(len(snake) - 1, 0, -1):
                    snake[i][0]=snake[i - 1][0]
                    snake[i][1] = snake[i - 1][1]
                scr=0
            scr += 1

            if (snake[0][0] + 15 > pyautogui.size()[0] // 2 - 50) or (snake[0][0] - 15 < 50) or\
                    (snake[0][1] - 15 < 50) or (snake[0][1] + 15 > pyautogui.size()[1] // 2 + pyautogui.size()[1] // 4 - 50):
                cv2.putText(image, 'You lose', (pyautogui.size()[0] // 4 - 100, pyautogui.size()[1] // 4),  cv2.FONT_HERSHEY_COMPLEX, 1.3, (147, 213, 178), 3)
                cv2.imshow('Snake', image)
                cv2.waitKey(10000)
                cv2.destroyAllWindows()
                image = cv2.resize(image, size)
                snake.clear()
                record = k
                k = 0
                return 0

            for i in range(1,len(snake)):
                cv2.circle(image, (snake[i][0], snake[i][1]), 15, (b1,g1,r1), -1)
            cv2.circle(image, (snake[0][0], snake[0][1]), 15, (b1 + 20, g + 20, r + 20), -1)


            if (lmlist1[8][0] < ball[0][0] + 10) and (lmlist1[8][0] > ball[0][0] - 10) and (lmlist1[8][1] < ball[1][0] + 10) and (lmlist1[8][1] > ball[1][0] - 10):
                ball[0].clear()
                ball[1].clear()
                snake.append(lmlist1[8])
                k += 1

        cv2.putText(counter, 'Counter: ' + str(k), (55, 75), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (60, 78, 58), 3)
        cv2.imshow('Counter', counter)
        cv2.imshow('Snake', image)

        if detector.findDistance((lmlist1[4][0], lmlist1[4][1]), (lmlist1[20][0], lmlist1[20][1]))[0] < 70:
            cv2.destroyAllWindows()
            image = cv2.resize(image, size)
            snake.clear()
            record = k
            k = 0
            return 0

        if cv2.waitKey(5) & 0xFF == 27:
            cv2.destroyAllWindows()
            image = cv2.resize(image, size)
            snake.clear()
            record = k
            k = 0
            return 0

def color():
    global r, g, b, image, r1, g1, b1, r2, b2, g2

    cv2.namedWindow('SnakeColor')
    cv2.resizeWindow('SnakeColor',400,390)

    def non(none):
        pass

    cv2.createTrackbar('Red', 'SnakeColor', 0, 255 , non)
    cv2.createTrackbar('Green', 'SnakeColor', 0, 255, non)
    cv2.createTrackbar('Blue', 'SnakeColor', 0, 255, non)
    cv2.createTrackbar('RedSnake', 'SnakeColor', 0, 255, non)
    cv2.createTrackbar('GreenSnake', 'SnakeColor', 0, 255, non)
    cv2.createTrackbar('BlueSnake', 'SnakeColor', 0, 255, non)
    cv2.createTrackbar('RedBalls', 'SnakeColor', 0, 255, non)
    cv2.createTrackbar('GreenBalls', 'SnakeColor', 0, 255, non)
    cv2.createTrackbar('BlueBalls', 'SnakeColor', 0, 255, non)

    while True:
        r = cv2.getTrackbarPos('Red', 'SnakeColor')
        g = cv2.getTrackbarPos('Green', 'SnakeColor')
        b = cv2.getTrackbarPos('Blue', 'SnakeColor')
        r1 = cv2.getTrackbarPos('RedSnake', 'SnakeColor')
        g1 = cv2.getTrackbarPos('GreenSnake', 'SnakeColor')
        b1 = cv2.getTrackbarPos('BlueSnake', 'SnakeColor')
        r2 = cv2.getTrackbarPos('RedBalls', 'SnakeColor')
        g2 = cv2.getTrackbarPos('GreenBalls', 'SnakeColor')
        b2 = cv2.getTrackbarPos('BlueBalls', 'SnakeColor')
        image[:, :, :] = (b, g, r)
        cv2.circle(image, (100, 100), 15, (b1, g1, r1), -1)
        cv2.circle(image, (200, 100), 10, (b2, g2, r2), -1)
        cv2.imshow('Snake', image)

        if detector.findDistance((lmlist1[4][0], lmlist1[4][1]), (lmlist1[20][0], lmlist1[20][1]))[0] < 70:
            cv2.destroyAllWindows()
            return 0

        if cv2.waitKey(5) & 0xFF == 27:
            cv2.destroyAllWindows()
            return 0

while True:
    f = open('record.txt', 'r')
    maxrecord = int(f.readline())
    f.close()
    image[:, :, :] = (b, g, r)

    cv2.rectangle(image, ((size[0] // 2) - 100, (size[1] // 2) - 150), ((size[0] // 2) + 100, (size[1] // 2) - 30),
                  (b - 31, g - 93, r - 61), 5)
    cv2.rectangle(image, ((size[0] // 2) - 95, (size[1] // 2) - 145), ((size[0] // 2) + 95, (size[1] // 2) - 35),
                  (b - 31, g - 93, r - 61), -1)
    cv2.putText(image, 'Play', ((size[0] // 2) - 40, (size[1] // 2) - 75), cv2.FONT_HERSHEY_SIMPLEX, 1.3,
                (147, 213, 178), 3)

    cv2.rectangle(image, ((size[0] // 2) - 100, (size[1] // 2) + 5), ((size[0] // 2) + 100, (size[1] // 2) + 125),
                  (b - 31, g - 93, r - 61), 5)
    cv2.rectangle(image, ((size[0] // 2) - 95, (size[1] // 2) + 10), ((size[0] // 2) + 95, (size[1] // 2) + 120),
                  (b - 31, g - 93, r - 61), -1)
    cv2.putText(image, 'Color', ((size[0] // 2) - 50, (size[1] // 2) + 75), cv2.FONT_HERSHEY_SIMPLEX, 1.3,
                (147, 213, 178), 3)

    succes, img = cap.read()
    img = cv2.flip(img, 90)

    hands = detector.findHands(img, draw=False)
    if hands:
        hand1 = hands[0]
        lmlist1 = hand1["lmList"]
        bbox1 = hand1["bbox"]
        centerPoint1 = hand1['center']
        handType1 = hand1["type"]
        cv2.circle(image, (lmlist1[8][0], lmlist1[8][1]), 10, (31, 191, 169), -1)

        if  ((lmlist1[8][0]) > ((size[0] // 2) - 100)) and ((lmlist1[8][0]) < ((size[0] // 2) + 100)) and \
            ((lmlist1[8][1]) > (size[1] // 2) + 5) and ((lmlist1[8][1]) < (size[1] // 2) + 125) \
            and detector.findDistance((lmlist1[8][0], lmlist1[8][1]), (lmlist1[4][0], lmlist1[4][1]))[0] < 20:
            color()

        if ((lmlist1[8][0]) > ((size[0] // 2) - 100)) and ((lmlist1[8][0]) < ((size[0] // 2) + 100)) and \
            ((lmlist1[8][1]) > (size[1] // 2) - 150) and ((lmlist1[8][1]) < (size[1] // 2) - 30) \
            and detector.findDistance((lmlist1[8][0], lmlist1[8][1]), (lmlist1[4][0], lmlist1[4][1]))[0] < 20:
            play()
        if detector.findDistance((lmlist1[4][0], lmlist1[4][1]), (lmlist1[16][0], lmlist1[16][1]))[0] < 50:
            maxrecord = maxrecord
            break

    if maxrecord < record:
        maxrecord = record

    f = open('record.txt', 'r')
    d = int(f.readline())
    f.close()
    if d < maxrecord:
        d = maxrecord
        f = open('record.txt', 'w')
        f.write(str(d))
        f.close()

    cv2.putText(image, 'Record: ' + str(maxrecord), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3,(147, 213, 178), 3)

    cv2.imshow('Snake', image)

    if cv2.waitKey(5) & 0xFF == 27:
        break
