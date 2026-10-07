import cv2
from hand_detector import HandDetector
from gesture_classifier import GestureClassifier
from actions import Actions

cap = cv2.VideoCapture(0)
detector = HandDetector()
classifier = GestureClassifier()
actions = Actions()

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read frame.")
        break

    frame, results = detector.detect(frame)

    gesture, hand_position, pinch_distance = classifier.classify(results)

    if hand_position is not None:
        actions.perform(
            gesture,
            hand_position,
            pinch_distance
        )

    cv2.putText(
        frame,
        gesture,
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    if gesture == "PINCH":
        current_brightness = actions.get_brightness()

        cv2.putText(
            frame,
            f"Brightness: {current_brightness}%",
            (20, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

    cv2.imshow("Hand Gesture Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()