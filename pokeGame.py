import cv2 as cv
import numpy as np
import pyautogui
import autoit
import pydirectinput
import pytesseract
from math import floor
import pyscreenshot as sc
import keyboard
import requests

captcha_ui_image = 'images\\captchas\\captchaTitle.png'
stop = False
gotify_url = 'http://localhost:80'
app_token = 'APJQrj78re2CzhV'

def onkeypress(event):
    global stop
    if event.name == '0':
        stop = not stop

class pokeGame:
    def __init__(self) -> None:
        keyboard.on_press(onkeypress)
        pass

    def is_horde(self, txt):
        txt_split = txt.split(' ')
        print("isHorde OCR text recognized: " + txt.replace('\n', ' '))
        if len(txt_split) > 15:
            return True
        return False

        
    def readScreen(self, shinybox=(190, 75, 1800, 200)):
        global stop
        while stop:
            pyautogui.sleep(.4)
        im = sc.grab(bbox=shinybox)
        im.save('readScreen.png')
        img_cv = cv.imread('readScreen.png')
        # turn all non white pixels to black

        hsv = cv.cvtColor(img_cv, cv.COLOR_BGR2HSV)
        # get white pixels
        lower_white = np.array([0,0,0], dtype=np.uint8)
        upper_white = np.array([0,0,255], dtype=np.uint8)
        mask = cv.inRange(hsv, lower_white, upper_white)
        # apply mask to image
        img_cv = cv.bitwise_and(img_cv, img_cv, mask=mask)
        # convert to grayscale
        img_cv = cv.cvtColor(img_cv, cv.COLOR_BGR2GRAY)
        # apply threshold
        ret, img_cv = cv.threshold(img_cv, 150, 255, cv.THRESH_BINARY)
        # invert image
        img_cv = img_cv
        
        cv.imwrite('readScreen1.png', img_cv)

        text = pytesseract.image_to_string( img_cv )
        # remove all non alphanumeric characters or . or space
        text = ''.join(e for e in text if e.isalnum() or e == '.' or e == ' ')
        return text.strip()
    
    def check_for_shiny(self, txt):
        global stop
        while stop:
            pyautogui.sleep(.4)
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
        if self.checkForCaptcha():
            print("Captcha detected, sleeping for 60 seconds")
            pyautogui.sleep(60)
            return None
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
        if self.checkForCaptcha():
            print("Captcha detected, sleeping for 60 seconds")
            pyautogui.sleep(60)
            return []
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

    def checkForCaptcha(self):
        global stop
        while stop:
            pyautogui.sleep(.4)
        image_loc = [loc for loc in pyautogui.locateAllOnScreen(captcha_ui_image, confidence=.6, grayscale=True)]
        if image_loc:
            print("HOLY SHIT FUCK")
            message = {
                'title': 'It\'s a captcha!',
                'message': 'Shit fucking captchas fuck come quick!',
                'priority': 7,
            }

            # Send the notification
            response = requests.post(f'{gotify_url}/message?token={app_token}', json=message)
            return True
        return False