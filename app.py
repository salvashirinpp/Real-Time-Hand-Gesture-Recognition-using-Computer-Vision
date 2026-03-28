import cv2
import mediapipe as mp
import numpy as np

# ------------------ MediaPipe Setup ------------------
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# ------------------ Gesture Counters ------------------
gesture_count = {
    "THUMBS_UP": 0,
    "PEACE": 0,
    "PALM": 0,
    "FIST": 0
}

prev_gesture = None

# ------------------ Gesture Classification ------------------
def classify_gesture(landmarks):
    """
    Classify hand gesture using landmark positions
    """
    tips = [8, 12, 16, 20]
    fingers = []

    # Fingers (except thumb)
    for tip in tips:
        fingers.append(landmarks[tip].y < landmarks[tip - 2].y)

    # Thumb (horizontal comparison)
    thumb_open = landmarks[4].x > landmarks[3].x

    if thumb_open and not any(fingers):
        return "THUMBS_UP"
    if fingers[0] and fingers[1] and not fingers[2] and not fingers[3]:
        return "PEACE"
    if all(fingers):
        return "PALM"
    if not any(fingers):
        return "FIST"

    return "UNKNOWN"

# ------------------ Webcam ------------------
cap = cv2.VideoCapture(0)

print("Press 'q' to quit")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    gesture = "NONE"

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            gesture = classify_gesture(hand_landmarks.landmark)

            # Count gesture only when it changes
            if gesture != prev_gesture and gesture in gesture_count:
                gesture_count[gesture] += 1
                prev_gesture = gesture

    # ------------------ Background Color Action ------------------
    if gesture == "THUMBS_UP":
        frame[:] = (200, 255, 200)  # Light green
    elif gesture == "PEACE":
        frame[:] = (255, 255, 200)  # Light yellow
    elif gesture == "PALM":
        frame[:] = (200, 255, 255)  # Light cyan
    elif gesture == "FIST":
        frame[:] = (255, 200, 200)  # Light red

    # ------------------ UI Overlay ------------------
    cv2.rectangle(frame, (0, 0), (360, 170), (0, 0, 0), -1)

    cv2.putText(frame, f"Gesture: {gesture}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    y = 60
    for g, c in gesture_count.items():
        cv2.putText(frame, f"{g}: {c}", (10, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        y += 25

    cv2.imshow("Gesture Recognition (CV Task)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
