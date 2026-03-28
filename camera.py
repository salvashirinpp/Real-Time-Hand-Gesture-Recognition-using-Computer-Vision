import cv2
import mediapipe as mp
from mediapipe.python.solutions import hands as mp_hands
from mediapipe.python.solutions import drawing_utils as mp_draw
import time

class VideoCamera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

        # MediaPipe
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.7)
        self.mp_draw = mp.solutions.drawing_utils

        # Counters
        self.gesture_count = {
            "FIST": 0,
            "THUMBS UP": 0,
            "PEACE": 0,
            "PALM": 0
        }

        self.prev_gesture = "NO HAND"
        self.last_time = 0   # delay control

    def __del__(self):
        self.cap.release()

    # ---------------- Gesture Logic ----------------
    def detect_gesture(self, lm):
        fingers = []

        # Index, middle, ring, pinky
        tips = [8, 12, 16, 20]
        for tip in tips:
            fingers.append(lm[tip].y < lm[tip - 2].y)

        # Thumb (simple)
        thumb = lm[4].x > lm[3].x

        if thumb and not any(fingers):
            return "THUMBS UP"
        elif fingers[0] and fingers[1] and not fingers[2] and not fingers[3]:
            return "PEACE"
        elif all(fingers):
            return "PALM"
        elif not any(fingers):
            return "FIST"

        return "UNKNOWN"

    # ---------------- Frame ----------------
    def get_frame(self):
        success, frame = self.cap.read()
        if not success:
            return None

        frame = cv2.flip(frame, 1)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb)

        gesture = "NO HAND"

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )

                gesture = self.detect_gesture(hand_landmarks.landmark)

        # ✅ FIX: Count only stable gesture (1 sec delay)
        if gesture != self.prev_gesture and gesture != "NO HAND":
            if time.time() - self.last_time > 1:
                if gesture in self.gesture_count:
                    self.gesture_count[gesture] += 1
                    self.prev_gesture = gesture
                    self.last_time = time.time()

        # ---------------- UI ----------------
        cv2.putText(frame, f"Gesture: {gesture}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        y = 80
        for g, c in self.gesture_count.items():
            cv2.putText(frame, f"{g}: {c}", (20, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            y += 30

        _, jpeg = cv2.imencode(".jpg", frame)
        return jpeg.tobytes()