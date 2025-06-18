import cv2
import time
import mediapipe as mp
import numpy as np
from collections import deque
import pyautogui
from pynput.mouse import Button, Controller


DEBUG = True
NUM_HANDS = 2
DETECTION_CONFIDENCE = 0.9
TRACKING_CONFIDENCE = 0.7
PINCH_DIST = 40
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
MOUSE_FACTOR = 1.3

mouse = Controller()

class HandDetection():
    def __init__(self, num_hands=2, detection_confidence=0.9, tracking_confidence=0.7):
        self.detector = mp.solutions.hands.Hands(
            max_num_hands=num_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.cap = cv2.VideoCapture(0)
        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.running = False
        self.pinched = False       # Tracks whether the user is pinching their thumb and index finger tips close together
        self.smoothing_buffer = deque(maxlen=4)     # Used to prevent jittery mouse movement


    def run(self):
        self.running = True
        while self.running:
            # capture camera
            _, frame = self.cap.read()

            # preprocess
            frame = cv2.flip(frame, 1)

            # detection
            detection_success, data = self.detect(frame)
            # make detection visible
            if DEBUG and detection_success:
                for handedness, hand_data in data.items():
                    index = np.array(hand_data[0][8])
                    self.smoothing_buffer.append(index)
                    thumb = np.array(hand_data[0][4])

                    # Distance betweent the thumb and index finger tips (for pinch detection)
                    distance = np.linalg.norm(index - thumb)

                    smoothed = np.mean(self.smoothing_buffer, axis=0)
                    x, y = smoothed

                    # Calculate mouse pointer position
                    mouse_x = int(x / self.width * SCREEN_WIDTH * MOUSE_FACTOR)
                    mouse_y = int(y / self.height * SCREEN_HEIGHT * MOUSE_FACTOR)
                    mouse.position = (mouse_x, mouse_y)

                    # Check for pinching and press/release button accordingly
                    if distance < PINCH_DIST:
                        if not self.pinched:
                            self.pinched = True
                            mouse.press(Button.left)
                    elif distance > PINCH_DIST:
                        if self.pinched:
                            mouse.release(Button.left)
                            self.pinched = False
                    
                    self.draw_landmarks(frame, hand_data[1])

            # draw image
            cv2.imshow('MediaPipe Sample', frame)

            # allow quit
            time.sleep(0.05)
            if cv2.waitKey(1) == ord('q'):
                self.running = False
                self.cap.release()
                cv2.destroyAllWindows()


    def draw_landmarks(self, img, landmarks):
        # draws the landmarks, caution: overwrites the image data
        mp.solutions.drawing_utils.draw_landmarks(
            img, landmarks, mp.solutions.hands.HAND_CONNECTIONS
        )   


    def detect(self, img):
        hand_data = {}
        h, w, _ = img.shape
        detections = self.detector.process(img)

        # was detection successful?
        success = detections.multi_hand_landmarks and detections.multi_handedness
        if not success:
            return False, hand_data

        for hand_landmarks, handedness in zip(detections.multi_hand_landmarks, detections.multi_handedness):
            # left or right hand?
            handedness_label = handedness.classification[0].label

            # collect coordinates within image
            img_coords = []
            for lm in hand_landmarks.landmark:
                x_px = int(lm.x * w)
                y_px = int(lm.y * h)
                img_coords.append((x_px, y_px))

            # hand data, e.g.: {"Left" : (landmark coords within image, landmark data to draw them)}
            hand_data[handedness_label] = (img_coords, hand_landmarks)
     
        return True, hand_data



if __name__ == '__main__':
    detector = HandDetection(NUM_HANDS, DETECTION_CONFIDENCE, TRACKING_CONFIDENCE)   
    detector.run()