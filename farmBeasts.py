# First go to a patch of grass 
# walk around until you find a beast or another pokemon
# Check if it contains a shiny
# if it does, stop
# if it doesn't, run away

import time
import pydirectinput
import pyautogui
import pytesseract
import cv2 as cv
import numpy as np

initialPos = 0
# The names of pokemon are always in the top corner
# SCREEN RESOLUTION: 2560 x 1440
namesROI = (125, 100, 2400, 200)

fight_ui_image = 'images\\fight_ui.png'

def walkAround(steps=1):
    global initialPos
    direction = 1
    if initialPos > 0:
        direction = -1
    initialPos += direction * steps	
    keyToPress = 'right' if direction == 1 else 'left'
    pydirectinput.keyDown(keyToPress)
    time.sleep(.125 * steps)
    pydirectinput.keyUp(keyToPress)

def getScreenShotText():
    screenshot = pyautogui.screenshot(region=namesROI)
    screenshot = cv.cvtColor( np.array(screenshot), cv.COLOR_RGB2GRAY)
    # keep only white pixels
    screenshot[screenshot < 250] = 0

    # If you want to see the cropped screenshot where the pokemon name is supposed to be
    #screenshot.save('pokeNamesRegionOfInterest.png')
    text = pytesseract.image_to_string( screenshot).strip()
    return text

def isPokemon(text):
    return text != '' and ('lv' in text.lower() or 'ly' in text.lower())

def isShiny(text):
    return 'shiny' in text.lower()    

def isBeast(text):
    return 'raikou' in text.lower() or 'entei' in text.lower() or 'suicune' in text.lower()


lastUICheck = time.time()
while True:
    text = getScreenShotText()
    isTextPokemon = isPokemon(text)
    if not text or not isTextPokemon:
        walkAround(3)
    else:
        while (fight_ui := pyautogui.locateOnScreen(fight_ui_image, confidence=.7)) == None:
            time.sleep(.5)
        print("Found Pokemon: " + text)
        if isShiny(text) or isBeast(text):
            print('Found a shiny or beast! Exiting...')
            exit(0)
        else:
            pydirectinput.press('right')
            time.sleep(.1)
            pydirectinput.press('down')
            time.sleep(.1)
            pydirectinput.press('z')
        while getScreenShotText() != '':
            time.sleep(.5)
        