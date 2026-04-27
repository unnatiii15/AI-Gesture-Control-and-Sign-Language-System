import cv2
import mediapipe as mp
import time
from gesture_logic import GestureLogic
from system_control import SystemControl

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

pTime = 0
gesture = GestureLogic()
control = SystemControl()

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

            lm_list = []
            h, w, c = img.shape

            for id, lm in enumerate(handLms.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((id, cx, cy))

            fingers = gesture.get_fingers(lm_list)
            stable_gesture = gesture.stabilize_gesture(fingers)
            pinch = gesture.detect_pinch(lm_list)

            cv2.putText(img, f'Fingers: {fingers}', (20, 140),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            if pinch:
                cv2.putText(img, 'PINCH', (20, 180),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            control.handle_pinch(pinch)

            x, y = lm_list[8][1], lm_list[8][2]

            # ===== SCROLL FIRST =====
            if fingers[1] == 1 and fingers[2] == 1:

                y = lm_list[8][2]

                if y < h//2 - 60:
                    control.scroll("up")
                    cv2.putText(img, "SCROLL UP", (20, 200),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)

                elif y > h//2 + 60:
                    control.scroll("down")
                    cv2.putText(img, "SCROLL DOWN", (20, 200),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)

                # ===== MOUSE =====
            elif fingers[1] == 1:
                control.move_mouse(x, y, w, h)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (120, 150),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Gesture Control - Phase 1", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()