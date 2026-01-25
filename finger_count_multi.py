import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# Hände-Tracker: bis zu 2 Hände
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)

FINGER_TIPS = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky


def count_fingers(hand_landmarks, handedness_label):
    """
    Count raised fingers for one hand.
    handedness_label is 'Left' or 'Right' (from MediaPipe).
    Works with mirrored frame (selfie) because we use handedness.
    """
    lm = hand_landmarks.landmark
    count = 0

    # Thumb logic depends on Left/Right hand
    # If hand is Right: thumb is open when tip.x < ip.x
    # If hand is Left:  thumb is open when tip.x > ip.x
    if handedness_label == "Right":
        if lm[4].x < lm[3].x:
            count += 1
    else:  # "Left"
        if lm[4].x > lm[3].x:
            count += 1

    # Other fingers: tip higher than PIP joint (y smaller = higher in image)
    for tip in FINGER_TIPS:
        if lm[tip].y < lm[tip - 2].y:
            count += 1

    return count


print("Multi-Hand Finger Counter läuft – 'q' zum Beenden")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Konnte keinen Frame lesen.")
        break

    frame = cv2.flip(frame, 1)  # selfie
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb)

    left_count = 0
    right_count = 0

    if result.multi_hand_landmarks and result.multi_handedness:
        # paired by index
        for hand_lms, handed in zip(result.multi_hand_landmarks, result.multi_handedness):
            label = handed.classification[0].label  # "Left" / "Right"
            score = handed.classification[0].score

            # draw landmarks
            mp_draw.draw_landmarks(frame, hand_lms, mp_hands.HAND_CONNECTIONS)

            # count fingers
            c = count_fingers(hand_lms, label)

            if label == "Left":
                left_count = c
            else:
                right_count = c

            # label near wrist
            wrist = hand_lms.landmark[0]
            h, w = frame.shape[:2]
            x, y = int(wrist.x * w), int(wrist.y * h)
            cv2.putText(
                frame,
                f"{label}: {c} ({score:.2f})",
                (max(10, x - 30), max(30, y - 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

    total = left_count + right_count

    cv2.putText(
        frame,
        f"Left: {left_count}  Right: {right_count}  Total: {total}",
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (0, 255, 0),
        2
    )

    cv2.imshow("Multi-Hand Finger Counter", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
