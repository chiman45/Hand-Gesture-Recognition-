# gesture_recognition.py

import cv2
import time
import numpy as np
import utils  # Importing our custom utilities file
import HandTrackingModule as htm

# Camera and window parameters
wCam, hCam = 640, 480
frameR = 100  # Frame Reduction
smoothening = 7  # Smoothening factor for cursor movement

# Set up video capture
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# Initialize hand detector
detector = htm.handDetector(maxHands=1)

# Get screen width and height for cursor control
wScr, hScr = utils.autopy.screen.size()

# Previous location and current location (used for smoothening the mouse movement)
plocX, plocY = 0, 0
clocX, clocY = 0, 0

# Volume control variables
pTime = 0

def main():
    global pTime, plocX, plocY

    while True:
        # 1. Read the webcam image
        success, img = cap.read()

        # 2. Detect hand and find landmarks
        img, lmList, bbox = utils.draw_hand_tracking(img, detector)

        # 3. Check if any landmarks are detected
        if lmList:
            # Get coordinates of index and middle fingers
            x1, y1 = lmList[8][1:]  # Index finger tip
            x2, y2 = lmList[12][1:]  # Middle finger tip

            # 4. Check which fingers are up
            fingers = detector.fingersUp()

            # 5. Moving Mode: Only index finger is up
            if fingers[1] == 1 and fingers[2] == 0:
                clocX, clocY = utils.move_mouse(x1, y1, frameR, wScr, hScr, smoothening, plocX, plocY)
                plocX, plocY = clocX, clocY

            # 6. Clicking Mode: Both index and middle fingers are up
            if fingers[1] == 1 and fingers[2] == 1:
                length, img, _ = detector.findDistance(8, 12, img)
                if length < 40:
                    utils.click_mouse()

            # 7. Gesture-based commands
            # Minimize window: All fingers closed
            if all(f == 0 for f in fingers):
                utils.minimize_active_window()

            # Maximize window: Three fingers up
            if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 0:
                utils.maximize_window()
                time.sleep(0.5)

            # Toggle keyboard: Four fingers up
            if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
                utils.keyboard_toggle()
                time.sleep(0.5)

            # Volume controls
            # Decrease volume: "Okay" gesture (thumb and index finger form a circle)
            if fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1 and fingers[0] == 0:
                utils.decrease_volume()

            # Increase volume: Thumbs up
            if fingers[0] == 1 and all(f == 0 for f in fingers[1:]):
                utils.increase_volume()

            # Scrolling
            # Scroll up: All five fingers up
            if all(f == 1 for f in fingers):
                utils.scroll_up()

            # Scroll down: "U" gesture (index and ring fingers up)
            if fingers[1] == 1 and fingers[3] == 1 and all(f == 0 for f in (fingers[0], fingers[2], fingers[4])):
                utils.scroll_down()

        # 8. Frame rate calculation
        fps, pTime = utils.calculate_fps(pTime)
        utils.draw_fps(img, fps)

        # 9. Display the image
        cv2.imshow("Hand Gesture Recognition", img)

        # 10. Break loop on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
