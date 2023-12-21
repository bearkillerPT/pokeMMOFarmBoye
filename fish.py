import time
import pydirectinput
import pyautogui
import pytesseract
import cv2 as cv
import numpy as np
import os
import requests
import random
# Replace with your Gotify server URL and application token
gotify_url = 'http://localhost:80'
app_token = 'APJQrj78re2CzhV'
debug = False # if true, prints in useful functions
sweetScentPP = 32 // 5 # 32 pp / 5 pokemon per sweet scent
sweetScentKey = '7'
teleportKey = '6'

initialPos = 0
# The names of pokemon are always in the top corner
# SCREEN RESOLUTION: 2560 x 1440
namesROI = (125, 100, 2400, 200)

fight_ui_image = 'images\\fight_ui.png'

def runAway():
    pydirectinput.press('right')
    time.sleep(.1)
    pydirectinput.press('down')
    time.sleep(.1)
    pydirectinput.press('z')


def isTextOnScreen(text):
    screenshot = pyautogui.screenshot()
    screenshot = cv.cvtColor( np.array(screenshot), cv.COLOR_RGB2GRAY)
    # keep only white pixels
    screenshot[screenshot < 225] = 0
    screen_text = pytesseract.image_to_string(screenshot)
    return text in screen_text


def getScreenShotText():
    screenshot = pyautogui.screenshot(region=namesROI)
    screenshot = cv.cvtColor( np.array(screenshot), cv.COLOR_RGB2GRAY)
    # keep only white pixels
    screenshot[screenshot < 225] = 0

    # If you want to see the cropped screenshot where the pokemon name is supposed to be
    #screenshot.save('pokeNamesRegionOfInterest.png')
    text = pytesseract.image_to_string( screenshot).strip()
    # every multiple of 2 is a pokemon name
    #text = text.split('\n')
    #if len(text) > 0:
    #    text = ' '.join([text[i] for i in range(len(text)) if i % 2 == 0])  
    #else:
    #    text = ''
    # join text with \n
    return text

def isPokemon(text):
    return text != '' and (
        'lv.' in text.lower() or 
        'lv,' in text.lower() or 
        'ly.' in text.lower() or
        'ly,' in text.lower()
        )

def isShiny(text):
    return 'shiny' in text.lower()    

def fishForShinies():
    global gotify_url
    global app_token
    global debug
    # get in the water or in front of the water
    rod_key = '4'
    while True: 
        print("Using rod!")
        while (fight_ui := pyautogui.locateOnScreen(fight_ui_image, confidence=.7)) == None:
            pydirectinput.press(rod_key)
            time.sleep(.5)
            pydirectinput.press("z")
            time.sleep(1)        
        text = getScreenShotText()
        if debug:
            print(text, end='\r')
        
        if isShiny(text):
            # Create a notification message
            message = {
                'title': 'It\'s a miracle!',
                'message': 'Found a shiny or beast! You better run to chatch this one! Exiting...',
                'priority': 7,
            }

            # Send the notification
            response = requests.post(f'{gotify_url}/message?token={app_token}', json=message)

            if response.status_code == 200:
                print('Notification sent successfully.')
            else:
                print(f'Failed to send notification. Status code: {response.status_code}')
                print(response.text)
            
            time.sleep(500)
            print('Found a shiny or beast! Exiting...')
            exit(0)
        else:
            runAway()
            while pyautogui.locateOnScreen(fight_ui_image, confidence=.7) != None:
                time.sleep(.5)


fishForShinies()