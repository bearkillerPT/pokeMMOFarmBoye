import cv2 as cv
import numpy as np
import pyautogui
import autoit
import pydirectinput

class pokeGame:
    def __init__(self) -> None:
        pass

    def log_screenshot(self, ):
        screenshot = np.array(pyautogui.screenshot())
        cv.imwrite('print.png', screenshot)


    def detectFirstOccImage(self, image, confidence=0.6):
        image_loc = pyautogui.locateAllOnScreen(
            image, confidence=confidence, grayscale=True)
        if image_loc:
            for image_occ in image_loc:
                return image_occ
        return None

    def holdKey(self, keys, duration):
        for key in keys:
            pydirectinput.keyDown(key)
        pyautogui.sleep(duration)
        for key in keys:
            pydirectinput.keyUp(key)

    def detectImage(self, image):
        image_loc = pyautogui.locateAllOnScreen(
            image, confidence=0.7, grayscale=True)
        res = []
        if image_loc:
            for image_occ in image_loc:
                res.append(image_occ)
        return res


    def moveMouseAndClick(self, x, y):
        autoit.mouse_move(x, y)
        autoit.mouse_click("left", x, y)
