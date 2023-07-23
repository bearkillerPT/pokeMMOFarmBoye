import cv2 as cv
import numpy as np
import pyautogui
import autoit
import pydirectinput
import pytesseract
from math import floor
import pyscreenshot as sc
import keyboard

stop = False

def onkeypress(event):
    global stop
    if event.name == '0':
        stop = not stop

class pokeGame:
    def __init__(self) -> None:
        keyboard.on_press(onkeypress)
        pass

    def is_horde(self):
        txt = self.readScreen()
        txt_split = txt.split(' ')
        print("isHorde OCR text recognized: " + txt.replace('\n', ' '))
        if len(txt_split) > 15:
            return True
        return False

        
    def readScreen(self, shinybox=(50, 50, 1800, 210)):
        global stop
        while stop:
            pyautogui.sleep(.4)
        im = sc.grab(bbox=shinybox)
        im.save('readScreen.png')
        img_cv = cv.imread('readScreen.png')
        hsv = cv.cvtColor(img_cv, cv.COLOR_BGR2HSV)

        hsv_channels = cv.split(hsv)
        return pytesseract.image_to_string( hsv_channels[0])

    def check_for_shiny(self, shinybox=(500, 50, 1400, 210)):
        global stop
        while stop:
            pyautogui.sleep(.4)
        im = sc.grab(bbox=shinybox)
        im.save('check_for_shiny.png')
        img_cv = cv.imread('check_for_shiny.png')
        hsv = cv.cvtColor(img_cv, cv.COLOR_BGR2HSV)

        hsv_channels = cv.split(hsv)

        txt = pytesseract.image_to_string( hsv_channels[0])
        print("OCR pokemon data (name, lvl, hp): \n\t" + txt.replace('\n', ' '))
        if 'Shiny' in txt or 'shiny' in txt or 'SHINY' in txt:
            print('Shiny Detected!')
            return True
        print('No Shiny Detected!')
        return False

    def log_screenshot(self, ):
        screenshot = np.array(pyautogui.screenshot())
        cv.imwrite('print.png', screenshot)


    def detectFirstOccImage(self, image, confidence=0.6, grayscale=True):
        global stop
        while stop:
            pyautogui.sleep(.4)
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
        global stop
        while stop:
            pyautogui.sleep(.4)
        image_loc = pyautogui.locateAllOnScreen(
            image, confidence=confidence, grayscale=grayscale)
        res = []
        if image_loc:
            for image_occ in image_loc:
                res.append(image_occ)
        return res


    def moveMouseAndClick(self, x, y):
        global stop
        while stop:
            pyautogui.sleep(.4)
        autoit.mouse_move(floor(x), floor(y))
        autoit.mouse_click("left", floor(x), floor(y))
