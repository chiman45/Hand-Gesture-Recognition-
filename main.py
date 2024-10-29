import cv2
import time
import numpy as np
import HandTrackingModule as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import autopy
import pygetwindow as gw
import pyautogui

# Constants for the first part of the code
wCam, hCam = 640, 480

# Constants for the second part of the code
wCam, hCam = 640, 480
frameR = 100
desired_fps = 50
smoothening = 7

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
cap.set(cv2.CAP_PROP_FPS, desired_fps)
pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

def hand_gesture_volume_control():
    # Constants from the first part of the code
    volRange = volume.GetVolumeRange()
    
    minVol = volRange[0]
    maxVol = volRange[1]
    vol = 0
    volBar = 400
    volPer = 0
    area = 0
    colorVol = (255, 0, 0)

    while True:
        success, img = cap.read()

        # Find Hand
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img, draw=True)
        if len(lmList) != 0:

            # Filter based on size
            area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1]) // 100
            # print(area)+
            if 250 < area < 1000:

                # Find Distance between index and Thumb
                length, img, lineInfo = detector.findDistance(4, 8, img)
                # print(length)

                # Convert Volume
                volBar = np.interp(length, [50, 200], [400, 150])
                volPer = np.interp(length, [50, 200], [0, 100])

                # Reduce Resolution to make it smoother
                smoothness = 10
                volPer = smoothness * round(volPer / smoothness)

                # Check fingers up
                fingers = detector.fingersUp()
                # print(fingers)

                # If pinky is down set volume
                if not fingers[4]:
                    volume.SetMasterVolumeLevelScalar(volPer / 100, None)
                    cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                    colorVol = (0, 255, 0)
                else:
                    colorVol = (255, 0, 0)

        # Drawings
        cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
        cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX,
                    1, (255, 0, 0), 3)
        cVol = int(volume.GetMasterVolumeLevelScalar() * 100)
        cv2.putText(img, f'Vol 0Set: {int(cVol)}', (400, 50), cv2.FONT_HERSHEY_COMPLEX,
                    1, colorVol, 3)

        # Frame rate
        cTime = time.time()
        pTime = 0
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                    1, (255, 0, 0), 3)

        cv2.imshow("Img", img)
        cv2.waitKey(1)

import autopy

def scroll_down(num_times=1):
    """
    Simulate scrolling down by pressing the "Down Arrow" key.

    Args:
        num_times (int): The number of times to press the "Down Arrow" key. Default is 1.
    """
    for _ in range(num_times):
        autopy.key.tap(autopy.key.Code.DOWN_ARROW)

# Example usage:
scroll_down(3) 

def minimize_active_window():
    # Get the current active window
    active_window = gw.getActiveWindow()

    if active_window is not None:
        # Minimize the active window
        active_window.minimize()
    else:
        print("No active window found.")

def keyboard():

    # Press and hold the Windows (Win) and Control (Ctrl) keys
    pyautogui.keyDown('win')
    pyautogui.keyDown('ctrl')
    pyautogui.keyDown('o')
    # Press the 'O' key


    # Release the Windows (Win) and Control (Ctrl) keys
    pyautogui.keyUp('win')
    pyautogui.keyUp('ctrl')
    pyautogui.keyUp('o')

def increase_volume():
    # Send a key press event for the "Volume Up" key (media key)
    pyautogui.press('volumeup')
    # Optionally, you can add a delay to control the speed of the keypress



def decrease_volume():
    # Send a key press event for 
    # the "Volume Up" key (media key)
    pyautogui.press('volumedown')
    # Optionally, you can add a delay to control the speed of the keypress    

def scroll_up(num_times=1):
    """
    Simulate scrolling up by pressing the "Up Arrow" key.

    
    Args:
        num_times (int): The number of times to press the "Up Arrow" key. Default is 1.
    """
    for _ in range(num_times):
        autopy.key.tap(autopy.key.Code.UP_ARROW)     

def close_active_window():
    # Get the active window
    active_window = gw.getActiveWindow()

    if active_window is not None:
        # Close the active window
        active_window.close()
        return True  # Return True if a window was closed
    else:
        return False  # Return False if no active window was found

def maximize_window():
    # To maximize
    pyautogui.FAILSAFE = False

    pyautogui.hotkey('win', 'tab')
    pyautogui.FAILSAFE = True

while True:
    success, img = cap.read()
       
    
        

    img = detector.findHands(img)
    lmList,bbox = detector.findPosition(img)
    # 2 Get the tip of the index and middle fingure
    if len(lmList)!=0:
        x1,y1 = lmList[8][1:]
        x2,y2 = lmList[12][1:]

        #print(x1,y1,x2, y2)

        # 3 Check which fingures are up 

        fingers = detector.fingersUp()
        #print(fingers)
        cv2.rectangle(img, (frameR, frameR),(wCam-frameR,hCam-frameR), (255,0,255),2)
        # 4 Only index fingures : moving mode
        if fingers[1]==1 and fingers[2]==0:
    
            # 5 Convert coordinates
           
            x3 = np.interp(x1,(frameR, wCam-frameR),(0, wScr))

            y3 = np.interp(y1,(frameR, hCam-frameR),(0, hScr))
            # 6 Smoothen values
            clocX = plocX + (x3 - plocX)/smoothening
            clocY = plocY + (y3 - plocY)/smoothening

            # 7 Move Mouse
            autopy.mouse.move(wScr-x3,y3)
            cv2.circle(img, (x1,y1), 15, (255,0 , 255),cv2.FILLED)
            plocX, plocY = clocX, clocY
        # 8 Both and index and middle finger are up: clicking mode
        if fingers[1]==1 and fingers[2]==1:
            # 9 Find distance between fingres
            length, img , lineInfo = detector.findDistance(8,12,img)
            print(length)
             # 10 Click mouse if distance short
            if length<40:
                cv2.circle(img,(lineInfo[4],lineInfo[5]),15,(0,255,0),cv2.FILLED)
                autopy.mouse.click() 

                
    
        # 10.1 for minimising
        if fingers[0]==0 and fingers[1]==0 and fingers[2]==0 and fingers[3]==0 and fingers[4]==0:
            # Call the function to minimize the active window
            minimize_active_window()

        # 10.2 for mazimizing
        if fingers[0]==0 and fingers[1]==1 and fingers[2]==1 and fingers[3]==1 and fingers[4]==0:    
            # Call the function to maximize the window
            maximize_window()    
            time.sleep(0.5)
        
        # 10.3 for keyboard 
        if fingers[0]==0 and fingers[1]==1 and fingers[2]==1 and fingers[3]==1 and fingers[4]==1 :
            keyboard()
            time.sleep(0.5)

        # 10.4 for scroll up
        if fingers[0]==1 and fingers[1]==1 and fingers[2]==1 and fingers[3]==1 and fingers[4]==1:
            scroll_up(1)    
        
        # 10.4 for decrease volume
        if fingers[0]==0 and fingers[1]==0 and fingers[2]==1 and fingers[3]==1 and fingers[4]==1:
            decrease_volume()

        # 10.5 for increase volume
        if fingers[0]==1 and fingers[1]==0 and fingers[2]==0 and fingers[3]==0 and fingers[4]==0:
            increase_volume()
        # 10.5 for close 
        if fingers[0]==0 and fingers[1]==1 and fingers[2]==0 and fingers[3]==0 and fingers[4]==1:
            # Call the function to close the current window
            scroll_down()
 
    # 11 Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,(255, 0, 0), 3)

    # 12 Display
    cv2.imshow("Image",img)
    cv2.waitKey(1)