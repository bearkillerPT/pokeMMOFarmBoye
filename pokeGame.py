import cv2 as cv
import numpy as np
import pyautogui
import autoit
import pydirectinput
import pytesseract
import pyscreenshot as sc

class pokeGame:
    def __init__(self) -> None:
        pass

    def check_for_shiny(self):
        im = sc.grab(bbox=(500, 50, 1400, 210))
        im.save('im.png')
        img_cv = cv.imread('im.png')
        img_rgb = cv.cvtColor(img_cv, cv.COLOR_BGR2GRAY)
        hsv = cv.cvtColor(img_cv, cv.COLOR_BGR2HSV)

        hsv_channels = cv.split(hsv)

        rows = img_cv.shape[0]
        cols = img_cv.shape[1]

        for i in range(0, rows):
            for j in range(0, cols):
                h = hsv_channels[0][i][j]


        txt = pytesseract.image_to_string( hsv_channels[0])
        print(txt)
        if 'Shiny' in txt or 'shiny' in txt or 'SHINY' in txt:
            print('SHINY DETECTED')
            return True
        print('####\nNO SHINY DETECTED\n######')
        return False

    def log_screenshot(self, ):
        screenshot = np.array(pyautogui.screenshot())
        cv.imwrite('print.png', screenshot)


    def detectFirstOccImage(self, image, confidence=0.6, grayscale=True):
        image_loc = pyautogui.locateAllOnScreen(
            image, confidence=confidence, grayscale=grayscale)
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


    def detectImage(self, image, confidence=0.6, grayscale=True):
        image_loc = pyautogui.locateAllOnScreen(
            image, confidence=confidence, grayscale=grayscale)
        res = []
        if image_loc:
            for image_occ in image_loc:
                res.append(image_occ)
        return res


    def moveMouseAndClick(self, x, y):
        autoit.mouse_move(x, y)
        autoit.mouse_click("left", x, y)
