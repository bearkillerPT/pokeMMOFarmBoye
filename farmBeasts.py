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

def isBeast(text):
    return 'raikou' in text.lower() or 'entei' in text.lower() or 'suicune' in text.lower()

def runAway():
    pydirectinput.press('right')
    time.sleep(.1)
    pydirectinput.press('down')
    time.sleep(.1)
    pydirectinput.press('z')

nightSlashPP = 15
paydayPP = 20

def useNightSlash():
    global nightSlashPP
    nightSlashPP -= 1
    pydirectinput.press('z')
    time.sleep(.1)
    pydirectinput.press('down')
    time.sleep(.1)
    pydirectinput.press('right')
    time.sleep(.1)
    pydirectinput.press('z')

def usePayday():
    global paydayPP
    paydayPP -= 1
    pydirectinput.press('z')
    time.sleep(.1)
    pydirectinput.press('right')
    time.sleep(.1)
    pydirectinput.press('z')

def farmBeast(): 
    global debug
    global encountersCount
    global gotify_url
    global app_token

    while True:
        if nightSlashPP == 0 or paydayPP == 0:
            print('Out of PP! Exiting...')
            exit(0)
        text = getScreenShotText()
        isTextPokemon = isPokemon(text)
        if debug:
            print(text, end='\r')
        if not text or not isTextPokemon:
            steps = random.random()*2 + 3
            pydirectinput.keyDown('x')
            walkAround(steps)
            pydirectinput.keyUp('x')
        else:
            print("Found Pokemon (try " + str(encountersCount) + "): " + text)
            while (fight_ui := pyautogui.locateOnScreen(fight_ui_image, confidence=.7)) == None:
                time.sleep(.5)
            if isShiny(text) or isBeast(text):
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
                
                print('Found a shiny or beast! Exiting...')
                exit(0)
            else:
                with open('encountersCount.txt', 'w') as f:
                    f.write(str(encountersCount + 1))
                    encountersCount += 1
                if 'diglett' in text.lower():
                    usePayday()
                    time.sleep(3)
                    # check if the pokemon is still there
                    # wait until the fight ui is there
                    while (fight_ui := pyautogui.locateOnScreen(fight_ui_image, confidence=.7)) == None:
                        time.sleep(.5)
                        if not isPokemon(getScreenShotText()):
                            break
                    # use night slash to finish the fight
                    if fight_ui != None:
                        useNightSlash()
                else:
                    runAway()
                
                

                while isPokemon(getScreenShotText()):
                    time.sleep(.1)

def goToPCAndHeal():
    global debug

    pydirectinput.press(teleportKey)
    time.sleep(5)
    if debug:
        print('In front of the PC! Starting healing...')
    pydirectinput.keyDown('z')
    time.sleep(6)
    pydirectinput.keyUp('z')
    pydirectinput.keyDown('x')
    pydirectinput.keyDown('z')
    time.sleep(7)
    pydirectinput.keyUp('z')
    pydirectinput.keyUp('x')
    if debug:
        print('Exiting...')
    pydirectinput.keyDown('down')
    time.sleep(1.75)
    pydirectinput.keyUp('down')
    time.sleep(2)
    print('Healed! Exiting...')

def runJohtoFromPCToDragonDen():
    # you need repel 
    repel_key = '8'
    pydirectinput.keyDown('x')
    pydirectinput.keyDown('left')
    time.sleep(.5)
    pydirectinput.keyUp('left')
    pydirectinput.keyDown('up')
    time.sleep(1)
    pydirectinput.keyUp('up')
    pydirectinput.keyDown('left')
    time.sleep(1.5)
    pydirectinput.keyUp('left')
    pydirectinput.keyDown('up')
    time.sleep(.6)
    pydirectinput.keyUp('up')
    pydirectinput.keyDown('left')
    time.sleep(.75)
    pydirectinput.keyUp('left')
    pydirectinput.keyDown('up')
    time.sleep(1)
    pydirectinput.keyUp('up')
    pydirectinput.keyDown('right')
    time.sleep(.85)
    pydirectinput.keyUp('right')
    pydirectinput.keyDown('up')
    time.sleep(.75)
    pydirectinput.keyUp('up')
    pydirectinput.keyDown('right')
    time.sleep(1.5)
    pydirectinput.keyUp('right')
    pydirectinput.keyDown('up')
    time.sleep(.5)
    pydirectinput.keyUp('up')
    # 59 steps (can be changed)
    # use repel
    pydirectinput.press(repel_key)
    time.sleep(.5)
    # swim 41 steps
    pydirectinput.press('z')
    time.sleep(.75)
    pydirectinput.press('z')
    time.sleep(.5)
    pydirectinput.press('z')
    time.sleep(.5)
    pydirectinput.keyDown('up')
    time.sleep(.75)
    pydirectinput.keyUp('up')
    pydirectinput.keyDown('left')
    time.sleep(.25)
    pydirectinput.keyUp('left')
    pydirectinput.keyDown('up')
    time.sleep(.75)
    pydirectinput.keyUp('up')
    pydirectinput.keyDown('right')
    time.sleep(.5)	
    pydirectinput.keyUp('right')
    pydirectinput.keyDown('up')
    time.sleep(.75)
    pydirectinput.keyUp('up')
    time.sleep(3)
    pydirectinput.keyDown('up')
    time.sleep(1)
    pydirectinput.keyUp('up')
    pydirectinput.keyDown('down')
    time.sleep(3)
    pydirectinput.keyUp('down')
    # min 18 steps to go back
    pydirectinput.press('z')
    time.sleep(.5)
    pydirectinput.press('z')
    time.sleep(.5)

    
def runJohtoFromPCToRoute42():
    # 100% encounter rate with hordes of mareep
    pydirectinput.keyDown('x')
    pydirectinput.keyDown('left')
    time.sleep(.9)
    pydirectinput.keyUp('left')
    pydirectinput.keyDown('up')
    time.sleep(1.2)
    pydirectinput.keyUp('up')
    pydirectinput.keyDown('left')
    time.sleep(2)
    pydirectinput.keyUp('left')
    pydirectinput.keyDown('up')
    time.sleep(.2)
    pydirectinput.keyUp('up')
    pydirectinput.keyDown('left')
    randomTime = random.random() * .4 + 2
    time.sleep(randomTime)
    pydirectinput.keyUp('left')
    pydirectinput.keyDown('down')
    randomTime = random.random() * .1 + .6
    time.sleep(randomTime)
    pydirectinput.keyUp('down')

def runJohtoFromPCToBellowSafari():
    # cool place with hordes of tauros, gloom and fearow
    pydirectinput.keyDown('x')
    pydirectinput.keyDown('down')
    time.sleep(.2)
    pydirectinput.keyUp('down')
    pydirectinput.keyDown('right')
    time.sleep(1.2)
    pydirectinput.keyUp('right')
    pydirectinput.keyDown('down')
    time.sleep(4.9)
    pydirectinput.keyUp('down')
    pydirectinput.keyUp('x')

def runJohtoFromPCToRoute45():
    pydirectinput.keyDown('x')
    pydirectinput.keyDown('down')
    time.sleep(.1)
    pydirectinput.keyUp('down')
    pydirectinput.keyDown('left')
    random_time = 1.75 + .25 * random.random()
    time.sleep(random_time)
    pydirectinput.keyUp('left')
    pydirectinput.keyDown('down')
    time.sleep(5.75)
    pydirectinput.keyUp('down')
    pydirectinput.keyUp('x')

def runHoennFromPCToDittoCave():
    pydirectinput.keyDown('x')
    pydirectinput.keyDown('left')
    time.sleep(1.1)
    pydirectinput.keyUp('left')
    pydirectinput.keyDown('down')
    time.sleep(.01)
    pydirectinput.keyUp('down')
    pydirectinput.keyDown('left')
    time.sleep(3)
    pydirectinput.keyUp('left')
    pydirectinput.keyDown('up')
    time.sleep(7)
    pydirectinput.keyUp('up')
    pydirectinput.keyDown('left')
    time.sleep(.01)
    pydirectinput.keyUp('left')
    pydirectinput.keyDown('up')
    time.sleep(.5)
    pydirectinput.keyUp('up')
    pydirectinput.keyDown('right')
    time.sleep(.01)
    pydirectinput.keyUp('right')
    pydirectinput.keyDown('up')
    time.sleep(1.4)
    pydirectinput.keyUp('up')
    pydirectinput.keyUp('x')

def farmHordes():
    global gotify_url
    global app_token
    global debug
    global sweetScentPP
    global encountersCount

    print('Going to the horde location...')
     runJohtoFromPCToBellowSafari()
    #runJohtoFromPCToRoute42()
    #runJohtoFromPCToRoute45()
    print('Arrived! Starting to farm...')
    for i in range(sweetScentPP): 
        time.sleep(1)
        time_init_trying_to_sweet_scent = time.time()
        while True:
            text = getScreenShotText()
            isTextPokemon = isPokemon(text)
            if debug:
                print(text, end='\r')
            if not text or not isTextPokemon:
                print('Using sweet scent... ' + str(i) + '/' + str(sweetScentPP), end='\r')
                pydirectinput.press(sweetScentKey)
                time.sleep(.5)
                if time.time() - time_init_trying_to_sweet_scent > 15:
                    print('Failed to use sweet scent. Teleporting...')
                    first_screenshot = pyautogui.screenshot()
                    pydirectinput.press(teleportKey)
                    time.sleep(5)
                    second_screenshot = pyautogui.screenshot()
                    # if the difference between the two screenshots is 10% or lower, it means that the teleport didn't work
                    if np.sum(np.abs(np.array(first_screenshot) - np.array(second_screenshot))) / np.sum(np.array(first_screenshot)) < .1:
                        print('Teleport failed. Sending notification...')
                        message = {
                            'title': 'Teleport failed!',
                            'message': 'Teleport failed. I\'m stuck! Come help me!',
                            'priority': 7,
                        }

                        response = requests.post(f'{gotify_url}/message?token={app_token}', json=message)
                        exit(0)
                    else:
                        goToPCAndHeal()
                    return
            else:
                print("Found Pokemon (try " + str(encountersCount) + " of Sweet Scent " + str(i) + "): " + text)
                print(text)
                while (fight_ui := pyautogui.locateOnScreen(fight_ui_image, confidence=.7)) == None:
                    time.sleep(.5)
                time.sleep(.5)
                
                if isShiny(text) or isBeast(text):

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
                elif 'diglett' in text.lower():
                    usePayday()
                    time.sleep(3)
                    # check if the pokemon is still there
                    # wait until the fight ui is there
                    while (fight_ui := pyautogui.locateOnScreen(fight_ui_image, confidence=.7)) == None:
                        time.sleep(.5)
                        if not isPokemon(getScreenShotText()):
                            break
                    # use night slash to finish the fight
                    if fight_ui != None:
                        useNightSlash()
                elif len(text.split(' ')) < 10: # it's not an horde
                    runAway()
                    i -= 1
                else:
                    with open('encountersCount.txt', 'w') as f:
                        f.write(str(encountersCount + 1))
                        encountersCount += 1
                        runAway()
                newText = getScreenShotText()
                start_time = time.time()
                while isPokemon((newText)):
                    if debug:
                        print("stuck", newText, isPokemon((newText)))
                    time.sleep(.1)
                    newText = getScreenShotText()
                    if time.time() - start_time > 10:
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
                break

    goToPCAndHeal()

def farmDittoCave():
    # hoenn
    while True:
        runHoennFromPCToDittoCave()
        text = getScreenShotText()
        if not text or not isPokemon(text):
                    walkAround(2)
        else:
            print("Found Pokemon (try " + str(encountersCount) + "): " + text)
            if 'ditto' in text.lower():
                print('Found a ditto! Exiting...')
            else:
                runAway()
        goToPCAndHeal()

# if a file with the encounters count exists, read it~
encountersCount = 0
if os.path.isfile('encountersCount.txt'):
    with open('encountersCount.txt', 'r') as f:
        encountersCount = int(f.readline())        

#runJohtoFromPCToDragonDen()
farmBeast()
#while True:
    #farmHordes()

