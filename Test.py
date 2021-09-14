from PIL.ImageOps import grayscale
import pyautogui
import pydirectinput
import time
import autoit
import math
import cv2 as cv
import numpy as np

METINTEXTDISTANCE = 60

healthbarnotempty = False
pickupkeypressed = False
healthbar_located = False
pixelcolor = (0, 0, 0)
clients = []
class Metin:

    def locateHealthBar():
        res=[]
        toInsert = True
        healthbarlocation = pyautogui.locateAllOnScreen('C:\\Users\\gil-t\\Downloads\\MetinBot-main\\images\\bar_full.png', confidence=0.9, grayscale=True)            
        if healthbarlocation:
            for barlocation in healthbarlocation:
                if len(res) == 0:
                    res.append(barlocation)
                else:
                    for barlocation2 in res:   
                            if abs(barlocation.left - barlocation2.left) < 10:
                                toInsert = False
                    if toInsert:
                        res.append(barlocation)
                    else:
                        toInsert = True
            for barlocation in res:
                print("Healthbarposition located: " + str(barlocation))
            
            return res
    def locateAllandFilterMetinHealthBar(client):
        metinhealthbarlocations = pyautogui.locateAllOnScreen('C:\\Users\\gil-t\\Downloads\\MetinBot-main\\images\\metin_hp.png', confidence=0.9, grayscale=True)
        for healthbar in metinhealthbarlocations:
            print(healthbar)
            if healthbar[0] < client["healthbar"][0] + 700 and healthbar[0] + 800 > client["healthbar"][0] and healthbar[1] < client["healthbar"][1] and healthbar[1] > client["healthbar"][1] - 700:
                return healthbar



    def checkIfMetinStillAlive(client):
        pyautogui.sleep(1)
        metinhealthbarlocation = 0
        template = cv.imread('C:\\Users\\gil-t\\Downloads\\MetinBot-main\\images\\metin_writing.png',0)
        w, h = template.shape[::-1]
        while not metinhealthbarlocation:
            metinhealthbarlocation = Metin.locateAllandFilterMetinHealthBar(client)
            screenshot = np.array(pyautogui.screenshot()) 
            img_gray = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
            if metinhealthbarlocation:
                return True
                #cv.rectangle(img_gray, (healthbarlocation.left -120, healthbarlocation.top + h -10), (healthbarlocation.left -132, healthbarlocation.top + h), (0,0,255), 2)
                #cv.imwrite('res.png',img_gray)
            return False
        leftouterpixellocation_x = int(metinhealthbarlocation.left -132)
        leftouterpixellocation_y = int(metinhealthbarlocation.top + h -5)
        # Try to get the Pixel-Color
        checkedColor = False
        pixelcolor = (0, 0, 0)
        
        try:
            pixelcolor = pyautogui.pixel(leftouterpixellocation_x, leftouterpixellocation_y)
            checkedColor = True
            print(pixelcolor)
        except Exception:
            print(Exception)
            return True

        if pixelcolor == (249, 108, 109):
            return True

        elif checkedColor:
            print('Pixelcolor: ' + str(pixelcolor))
            return False

    def collectLoot():
        print('collecting loot')
        pydirectinput.press('z', 3, interval=0.1) #cause of us layout


    def findMetinOpenCV(client):
        metinhealthbarlocation = Metin.locateAllandFilterMetinHealthBar(client)
        if metinhealthbarlocation:
            print("Bugged! Trying again!")
            pyautogui.press('esc')
            return False
        screenshot = np.array(pyautogui.screenshot())[ client["healthbar"][1] - 730 : client["healthbar"][1], client["healthbar"][0] - 10 :client["healthbar"][0] + 900]
        img_gray = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
        template = cv.imread('C:\\Users\\gil-t\\Downloads\\MetinBot-main\\images\\metin_writing.png',0)
        w, h = template.shape[::-1]
        cv.imwrite('res.png',img_gray)
        res = cv.matchTemplate(img_gray,template,cv.TM_CCORR_NORMED)
        threshold = 0.85
        loc = np.where( res >= threshold)
        target_dist = 1000
        target = 0
        for pt in zip(*loc[::-1]):
            if(math.sqrt(abs(300 - pt[0]) + abs(400- pt[1] + h + METINTEXTDISTANCE)) < target_dist and pt[0] + w < 750 and pt[1] + h + METINTEXTDISTANCE < 700):
                target = pt
        if not target:
            return False
        #for pt in zip(*loc[::-1]):
        print(f'Metin found at {target[0] + int(w/2)} and {target[1] + h + METINTEXTDISTANCE}')
        pyautogui.moveTo(target[0] + int(w/2) + client["healthbar"][0] - 10, target[1] + h + METINTEXTDISTANCE + client["healthbar"][1] - 730, 0.2)
            #pyautogui.click(clicks=2, interval=0.1)
        autoit.mouse_click("left",target[0] + int(w/2) + client["healthbar"][0] - 10, target[1] + h + METINTEXTDISTANCE + client["healthbar"][1] - 730,2)
            #cv.rectangle(img_gray, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
            #cv.imwrite('res.png',img_gray)
        return True

        print('No Metin found')
        
    def lookaround():
        print('looking around')
        pydirectinput.keyDown('numpad4')
        pydirectinput.keyDown('left')
        pydirectinput.keyUp('numpad4')
        pydirectinput.keyUp('left')
    def useSkills():
        print('Using skills!')
        pydirectinput.keyDown('ctrl')
        pydirectinput.press('h')
        pydirectinput.keyUp('ctrl')
        time.sleep(1)
        pydirectinput.press('3')
        time.sleep(2)
        pydirectinput.press('4')
        time.sleep(2)
        pydirectinput.keyDown('ctrl')
        pydirectinput.press('h')
        pydirectinput.keyUp('ctrl')
    
def run_bot():
    # Locate the Healthbar for init
    healthbarlocations = 0
    while not healthbarlocations:
        healthbarlocations = Metin.locateHealthBar()
    for location in healthbarlocations:
        clients.append({"healthbar": location,
                      "skills_timer" : 0,
                      "bugged_timer": 0,
                      "farming": False,
                      "windowTop": (location[0], location[1] - 740)
                     })
    while True:
        for client in clients:
            pyautogui.moveTo(client["windowTop"][0], client["windowTop"][1], 0.2)
            autoit.mouse_click("left",client["windowTop"][0], client["windowTop"][1],2)
            
            if( time.time() - client["skills_timer"] > 300):
                client["skills_timer"] = time.time()
                Metin.useSkills()
            #try to find a metin:
            #metinhealthbarlocation = Metin.locateMetinHealthBar()
            #if(metinhealthbarlocation):
            #    pyautogui.press('esc')
            #    Metin.lookaround()
            if not client["farming"]:
                if Metin.findMetinOpenCV(client):
                    client["bugged_timer"] = time.time()
                    client["farming"] = True
                
                else:
                    Metin.lookaround()
                    Metin.lookaround()
                    break
                #check if the metin is still alive
            if Metin.checkIfMetinStillAlive(client):
                if(time.time() - client["bugged_timer"] > 20):
                    pyautogui.press('d')
                    pyautogui.press('d')
            else:
                client["farming"] = False
                pyautogui.moveTo(client["windowTop"][0], client["windowTop"][1], 0.2)
                autoit.mouse_click("left",client["windowTop"][0], client["windowTop"][1],2)
                Metin.collectLoot()



if __name__ == '__main__':
    run_bot()

# while True:
#     if not Metin.findMetinOpenCV():
#         time.sleep(3)
#     else:

#         healthbarlocation = pyautogui.locateOnScreen('C:\\Users\\gil-t\\Downloads\\MetinBot-main\\images\\bar_full.png', confidence=0.9, grayscale=True)

#         if healthbarlocation:
#             print("Healthbarposition located: " + str(healthbarlocation))
#             healthbar_located = True
#             leftouterpixellocation_x = int(healthbarlocation.left + 14)
#             leftouterpixellocation_y = int(healthbarlocation.top + 3)

#         while healthbar_located:
#             #pyautogui.screenshot("testshot.png", region=(healthbarlocation))

#             # Try to get the Pixel-Color
#             try:
#                 pixelcolor = pyautogui.pixel(leftouterpixellocation_x, leftouterpixellocation_y)
#             except:
#                 print("Error")

#             # If the Color is 99,39,39 the Healthbar isnt empty
#             if pixelcolor == (99, 39, 39):
#                 pickupkeypressed = False

#             else:
#                 if not pickupkeypressed :
#                     print("press y")
#                     time.sleep(0.5)
#                     pydirectinput.press('z') #cause of us layout
#                     pickupkeypressed = True

#             time.sleep(1)



        # time.sleep(1)

