import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)

print("Finger Counter läuft – drücke 'q' zum Beenden")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Konnte keinen Frame lesen.")
        break

    # Spiegeln (wie Selfie)
    frame = cv2.flip(frame, 1)

    # MediaPipe braucht RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    finger_count = 0

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            lm = hand_landmarks.landmark

            # Daumen: (bei gespiegelt = Selfie) funktioniert meist so:
            # Daumen ist "offen", wenn Spitze weiter links ist als das vorherige Gelenk
            if lm[4].x < lm[3].x:
                finger_count += 1

            # Andere Finger: Spitze höher (kleiner y) als das mittlere Gelenk
            tips = [8, 12, 16, 20]  # Index, Mittel, Ring, Pinky
            for tip in tips:
                if lm[tip].y < lm[tip - 2].y:
                    finger_count += 1

            # Nur eine Hand auswerten
            break

    cv2.putText(
        frame,
        f"Finger: {finger_count}",
        (30, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        2,
        (0, 255, 0),
        3
    )

    cv2.imshow("Finger Counter", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
