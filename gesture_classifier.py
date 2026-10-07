import math


class GestureClassifier:
    def __init__(self):
        pass

    def distance(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2

        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def finger_extended(self, points, tip, pip, wrist):
        tip_distance = self.distance(points[tip], points[wrist])
        pip_distance = self.distance(points[pip], points[wrist])

        return tip_distance > pip_distance * 1.15

    def classify(self, results):
        if not results.hand_landmarks:
            return "UNKNOWN", None, None

        hand_landmarks = results.hand_landmarks[0]

        points = []

        for landmark in hand_landmarks:
            points.append((landmark.x, landmark.y))

        wrist = 0

        thumb_extended = self.finger_extended(
            points, 4, 3, wrist
        )

        index_extended = self.finger_extended(
            points, 8, 6, wrist
        )

        middle_extended = self.finger_extended(
            points, 12, 10, wrist
        )

        ring_extended = self.finger_extended(
            points, 16, 14, wrist
        )

        pinky_extended = self.finger_extended(
            points, 20, 18, wrist
        )

        other_fingers_closed = (
            not middle_extended
            and not ring_extended
            and not pinky_extended
        )

        if (
            thumb_extended
            and index_extended
            and middle_extended
            and ring_extended
            and pinky_extended
        ):
            gesture = "OPEN_PALM"

        elif (
            not thumb_extended
            and not index_extended
            and not middle_extended
            and not ring_extended
            and not pinky_extended
        ):
            gesture = "FIST"

        elif (
            index_extended
            and not thumb_extended
            and other_fingers_closed
        ):
            gesture = "INDEX"

        elif (
            thumb_extended
            and index_extended
            and other_fingers_closed
        ):
            gesture = "PINCH"

        else:
            gesture = "UNKNOWN"

        hand_position = points[0]

        pinch_distance = self.distance(
            points[4],
            points[8]
        )

        palm_size = self.distance(
            points[0],
            points[9]
        )

        if palm_size > 0:
            pinch_distance = pinch_distance / palm_size

        return gesture, hand_position, pinch_distance