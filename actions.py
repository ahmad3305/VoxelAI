import time
import pyautogui
import screen_brightness_control as sbc


class Actions:
    def __init__(self):
        self.last_media_gesture = "UNKNOWN"

        self.previous_y = None
        self.previous_pinch = None

        self.last_volume_action = 0
        self.last_brightness_action = 0
        
    def get_brightness(self):
        return sbc.get_brightness()[0]
        

    def perform(self, gesture, hand_position, pinch_distance):
        current_time = time.time()

        if gesture == "OPEN_PALM":
            if self.last_media_gesture == "FIST":
                pyautogui.press("space")

            self.last_media_gesture = "OPEN_PALM"

        elif gesture == "FIST":
            if self.last_media_gesture == "OPEN_PALM":
                pyautogui.press("space")

            self.last_media_gesture = "FIST"

        elif gesture == "INDEX":
            if self.previous_y is not None:
                movement = self.previous_y - hand_position[1]
                
                if current_time - self.last_volume_action > 0.15:

                    if movement > 0.003:
                        pyautogui.hotkey("ctrl", "up")
                        self.last_volume_action = current_time

                    elif movement < -0.003:
                        pyautogui.hotkey("ctrl", "down")
                        self.last_volume_action = current_time

            self.previous_y = hand_position[1]

        elif gesture == "PINCH":
            if self.previous_pinch is not None:
                movement = pinch_distance - self.previous_pinch

                if current_time - self.last_brightness_action > 0.35:

                    if movement > 0.03:
                        current_brightness = sbc.get_brightness()[0]

                        sbc.set_brightness(
                            min(current_brightness + 5, 100)
                        )

                        print("Brightness UP")
                        self.last_brightness_action = current_time

                    elif movement < -0.03:
                        current_brightness = sbc.get_brightness()[0]

                        sbc.set_brightness(
                            max(current_brightness - 5, 0)
                        )

                        print("Brightness DOWN")
                        self.last_brightness_action = current_time

            self.previous_pinch = pinch_distance

        else:
            self.previous_y = None
            self.previous_pinch = None

        if gesture != "INDEX":
            self.previous_y = None

        if gesture != "PINCH":
            self.previous_pinch = None

        self.last_gesture = gesture


