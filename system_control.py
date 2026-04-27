import pyautogui
import time

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0


class SystemControl:

    def __init__(self):
        self.dragging = False
        self.pinch_start_time = None
        self.last_click_time = 0
        self.prev_x, self.prev_y = 0, 0

    def move_mouse(self, x, y, frame_w, frame_h):
        import pyautogui

        screen_w, screen_h = pyautogui.size()

        # reduce active area (important)
        frame_reduction = 120

        x = min(max(x, frame_reduction), frame_w - frame_reduction)
        y = min(max(y, frame_reduction), frame_h - frame_reduction)

        # map to screen
        screen_x = screen_w * (x - frame_reduction) / (frame_w - 2 * frame_reduction)
        screen_y = screen_h * (y - frame_reduction) / (frame_h - 2 * frame_reduction)

        # smoothing (key fix)
        curr_x = self.prev_x + (screen_x - self.prev_x) / 8
        curr_y = self.prev_y + (screen_y - self.prev_y) / 8

        pyautogui.moveTo(curr_x, curr_y)

        self.prev_x, self.prev_y = curr_x, curr_y
    def scroll(self, direction):
        import pyautogui
        if direction == "up":
            pyautogui.scroll(100)
        else:
            pyautogui.scroll(-100)    

    def handle_pinch(self, pinch):
        current_time = time.time()

        if pinch:
            if self.pinch_start_time is None:
                self.pinch_start_time = current_time

            elif (current_time - self.pinch_start_time > 0.5) and not self.dragging:
                pyautogui.mouseDown()
                self.dragging = True

        else:
            if self.pinch_start_time is not None:
                duration = current_time - self.pinch_start_time

                if self.dragging:
                    pyautogui.mouseUp()
                    self.dragging = False

                elif duration > 0.1:   # 👈 prevents accidental taps
                    if current_time - self.last_click_time < 0.8:
                        pyautogui.rightClick()
                    else:
                        pyautogui.click()

                    self.last_click_time = current_time

                self.pinch_start_time = None