from PIL.ImageOps import grayscale
import pyautogui
import pydirectinput
import time
import autoit
import math
import cv2 as cv
import numpy as np
import copy
METINTEXTDISTANCE = 60
deliver_button_size = 10
market_button_size = 10
orc_tooth_button_size = 10
submit_button_size = 10
trash_size = 30
metin_health_bar_image = 'C:\\Users\\gil-t\\Downloads\\MetinBot-main\\images\\metin_hp.png'
logged_out_image = 'C:\\Users\\gil-t\\Downloads\\MetinBot-main\\images\\logged_out_right.png'
biologist_deliver = 'C:\\Users\\gil-t\\Downloads\\MetinBot-main\\images\\biologist\\deliver.png'
biologist_market = 'C:\\Users\\gil-t\\Downloads\\MetinBot-main\\images\\biologist\\market.png'
biologist_orc_tooth = 'C:\\Users\\gil-t\\Downloads\\MetinBot-main\\images\\biologist\\orc_tooth.png'
biologist_submit = 'C:\\Users\\gil-t\\Downloads\\MetinBot-main\\images\\biologist\\submit_text.png'
trash_1 = 'C:\\Users\\gil-t\\Downloads\\MetinBot-main\\images\\items_to_delete\\pulseira_ebano.png'
trash_2 = 'C:\\Users\\gil-t\\Downloads\\MetinBot-main\\images\\items_to_delete\\leque_fenix.png'
trash_3 = 'C:\\Users\\gil-t\\Downloads\\MetinBot-main\\images\\items_to_delete\\dagger.png'
destroy_item = 'C:\\Users\\gil-t\\Downloads\\MetinBot-main\\images\\items_to_delete\\confirm_destroy.png'
settings = 'C:\\Users\\gil-t\\Downloads\\MetinBot-main\\images\\settings.png'
lvl = 'C:\\Users\\gil-t\\Downloads\\MetinBot-main\\images\\lvl.png'
healthbarnotempty = False
pickupkeypressed = False
healthbar_located = False
clients = []
pixelcolor = (0, 0, 0)
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

    def handleLogout(clients, client):
        pyautogui.moveTo(client["window_top"][0] , client["window_top"][1] , 0.2)
        autoit.mouse_click("left",client["window_top"][0], client["window_top"][1], 2)
        pyautogui.moveTo(client["window_top"][0] , client["window_top"][1] +200, 0.2)
        autoit.mouse_click("left",client["window_top"][0], client["window_top"][1]+200, 2)
        pydirectinput.press('f' + str(clients.index(client) + 2))
        time.sleep(3)
        pyautogui.moveTo(client["window_top"][0] , client["window_top"][1] , 0.2)
        autoit.mouse_click("left",client["window_top"][0], client["window_top"][1], 2)
        pyautogui.press('enter')
        pyautogui.press('enter')
        pyautogui.keyDown('f')
        pyautogui.sleep(2)
        pyautogui.keyUp('f')

    def locateAllAndFilterProp(client, prop_image):
        res = []
        prop_locations = pyautogui.locateAllOnScreen(prop_image, confidence=0.8, grayscale=True)
        for prop_location in prop_locations:
            if prop_location[0] > client["healthbar"][0] and prop_location[0] < client["healthbar"][0] + 800 and prop_location[1] < client["healthbar"][1] and prop_location[1] > client["healthbar"][1] - 900:
                    res.append(prop_location)
        return res

    def locateAndFilterProp(client, prop_image):
        prop_locations = pyautogui.locateAllOnScreen(prop_image, confidence=0.8, grayscale=True)
        for prop_location in prop_locations:
            if prop_location[0] > client["healthbar"][0] and prop_location[0] < client["healthbar"][0] + 800 and prop_location[1] < client["healthbar"][1] and prop_location[1] > client["healthbar"][1] - 900:
                    return prop_location
                

    def checkIfMetinStillAlive(client):
        metinhealthbarlocation = 0
        template = cv.imread('C:\\Users\\gil-t\\Downloads\\MetinBot-main\\images\\metin_writing.png',0)
        w, h = template.shape[::-1]
        while not metinhealthbarlocation:
            metinhealthbarlocation = Metin.locateAndFilterProp(client, metin_health_bar_image)
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

    def collectLoot(client):
        print('collecting loot')
        pyautogui.moveTo(client["window_top"][0] , client["window_top"][1] , 0.2)
        autoit.mouse_click("left",client["window_top"][0], client["window_top"][1], 2)
        pydirectinput.press('z') #cause of us layout


    def findMetinOpenCV(client):
        metinhealthbarlocation = Metin.locateAndFilterProp(client, metin_health_bar_image)
        if metinhealthbarlocation:
            Metin.collectLoot(client)
            print("Bugged! Trying again!")
            pyautogui.keyDown('esc')
            pyautogui.keyUp('esc')
            pyautogui.keyDown('a')
            pyautogui.keyDown('s')
            pyautogui.sleep(2)
            pyautogui.keyUp('a')
            pyautogui.keyUp('s')
            pyautogui.press('q')
            pyautogui.press('q')
            return False
        screenshot = np.array(pyautogui.screenshot())[ client["healthbar"][1] - 730 : client["healthbar"][1] - 140, client["healthbar"][0] - 10 :client["healthbar"][0] + 900]
        img_gray = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
        template = cv.imread('C:\\Users\\gil-t\\Downloads\\MetinBot-main\\images\\metin_writing.png',0)
        w, h = template.shape[::-1]
        res = cv.matchTemplate(img_gray,template,cv.TM_CCORR_NORMED)
        threshold = 0.9
        loc = np.where( res >= threshold)
        target_dist = 1000
        target = 0
        yellow_pixels = 0
        for pt in zip(*loc[::-1]):
            red_pixels = 0

            for i in range(pt[0], pt[0] + w):
                for j in range(pt[1] + 55, pt[1] + h+ 70):
                    if i < len(screenshot) and j < len(screenshot[0]):
                        pixel = screenshot[i, j]
                        if pixel[0] > 200 and pixel[1] < 50 and pixel[2] < 50:
                            red_pixels += 1  
            if red_pixels < 10 and (math.sqrt(pow(abs(440 - pt[0] + int(w/2)),2) +pow(abs(310- pt[1] + int(h/2) + METINTEXTDISTANCE), 2)) < target_dist and pt[0] + w < 750 and pt[1] + h + METINTEXTDISTANCE < 700):
                target = pt
        if not target:
            return False
        print(f'Metin found at {target[0] + int(w/2)} and {target[1] + h + METINTEXTDISTANCE}')

        #for pt in zip(*loc[::-1]):
        pyautogui.moveTo(target[0] + int(w/2) + client["healthbar"][0]+ 10, target[1] + h + METINTEXTDISTANCE + client["healthbar"][1] - 730, 0.2)
            #pyautogui.click(clicks=2, interval=0.1)
        autoit.mouse_click("left",target[0] + int(w/2) + client["healthbar"][0] + 10, target[1] + h + METINTEXTDISTANCE + client["healthbar"][1] - 730,2)
            #cv.rectangle(img_gray, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
            #cv.imwrite('res.png',img_gray)
        return True

        print('No Metin found')
        
    def lookaround():
        print('looking around')
        pydirectinput.press('q')
        pydirectinput.press('q')
        pydirectinput.press('q')
        pydirectinput.press('q')

        #pydirectinput.D('left')
        #pydirectinput.keyUp('left')

    def useSkills(client):
        pyautogui.moveTo(client["window_top"][0] , client["window_top"][1] , 0.2)
        autoit.mouse_click("left",client["window_top"][0], client["window_top"][1], 2)
        print('Using skills!')
        pydirectinput.keyDown('ctrl')
        pyautogui.sleep(0.2)
        pydirectinput.press('h')
        pydirectinput.keyUp('ctrl')
        time.sleep(1)
        pydirectinput.press('3')
        time.sleep(2)
        pydirectinput.press('4')
        time.sleep(2)
        pydirectinput.keyDown('ctrl')
        pyautogui.sleep(0.2)
        pydirectinput.press('h')
        pydirectinput.keyUp('ctrl')

    def biologist(client):
        print("biologist!")
        pyautogui.moveTo(client["window_top"][0] , client["window_top"][1] , 0.2)
        autoit.mouse_click("left",client["window_top"][0], client["window_top"][1], 2)
        biologist_deliver_location = Metin.locateAndFilterProp(client, biologist_deliver)
        if(biologist_deliver_location):
            pyautogui.moveTo(int((biologist_deliver_location[0] + biologist_deliver_location[0] + deliver_button_size)/2) , int((biologist_deliver_location[1] + biologist_deliver_location[1] + deliver_button_size)/2) , 0.2)
            autoit.mouse_click("left",int((biologist_deliver_location[0] + biologist_deliver_location[0] + deliver_button_size)/2), int((biologist_deliver_location[1] + biologist_deliver_location[1] + deliver_button_size)/2), 2)
            biologist_market_location = [0,0,10,10]
            pyautogui.sleep(1)
            biologist_submit_location = Metin.locateAndFilterProp(client, biologist_submit)
            if biologist_submit_location:
                biologist_market_location[0] = biologist_submit_location[0] + biologist_submit_location[2] + 42 
                biologist_market_location[1] = biologist_submit_location[1] + 47
                pyautogui.sleep(1)
                pyautogui.moveTo(int((biologist_market_location[0] + biologist_market_location[0] + market_button_size)/2) , int((biologist_market_location[1] + biologist_market_location[1] + market_button_size)/2) , 0.2)
                autoit.mouse_click("left",int((biologist_market_location[0] + biologist_market_location[0] + market_button_size)/2), int((biologist_market_location[1] + biologist_market_location[1] + market_button_size)/2), 2)
                pydirectinput.press('i')
                pyautogui.sleep(1)
                biologist_orc_tooth_location = Metin.locateAndFilterProp(client, biologist_orc_tooth)
                if biologist_orc_tooth_location:
                    pyautogui.moveTo(int((biologist_orc_tooth_location[0] + biologist_orc_tooth_location[0] + orc_tooth_button_size)/2) , int((biologist_orc_tooth_location[1] + biologist_orc_tooth_location[1] + orc_tooth_button_size)/2) , 0.2)
                    autoit.mouse_click("right",int((biologist_orc_tooth_location[0] + biologist_orc_tooth_location[0] + orc_tooth_button_size)/2), int((biologist_orc_tooth_location[1] + biologist_orc_tooth_location[1] + orc_tooth_button_size)/2), 2)
                    pydirectinput.press('escape')
                    pyautogui.sleep(2)
                    if biologist_submit_location:
                        pyautogui.moveTo(int((biologist_submit_location[0] + biologist_submit_location[0] + submit_button_size)/2) , int((biologist_submit_location[1] + biologist_submit_location[1] + submit_button_size)/2) , 0.2)
                        autoit.mouse_click("left",int((biologist_submit_location[0] + biologist_submit_location[0] + submit_button_size)/2), int((biologist_submit_location[1] + biologist_submit_location[1] + submit_button_size)/2), 2)
                        client["biologist_timer"] = time.time()
                else:
                    pyautogui.sleep(1)
                    pyautogui.moveTo(client["window_top"][0], client["window_top"][1], 0.2)
                    autoit.mouse_click("left",client["window_top"][0], client["window_top"][1],2)
                    pydirectinput.press('escape')
            pyautogui.sleep(1)
            pyautogui.moveTo(int((biologist_orc_tooth_location[0] + biologist_orc_tooth_location[0] + orc_tooth_button_size)/2) , int((biologist_orc_tooth_location[1] + biologist_orc_tooth_location[1] + orc_tooth_button_size)/2) , 0.2)
            autoit.mouse_click("right",int((biologist_orc_tooth_location[0] + biologist_orc_tooth_location[0] + orc_tooth_button_size)/2), int((biologist_orc_tooth_location[1] + biologist_orc_tooth_location[1] + orc_tooth_button_size)/2), 2)
            pydirectinput.press('escape')
        

    def clearInventory(client):
        deleted = []
        print("Cleaning Inventory!")
        pydirectinput.press('i')
        trash_items = [trash_1, trash_2, trash_3]
        for trash_item in trash_items:
            trash = Metin.locateAndFilterProp(client, trash_item)
            while trash and not deleted.__contains__(trash) and time.time() - client["clear_inventory_bugged_timer"] < 50: 
                pyautogui.moveTo(int((trash[0] + trash[0] + trash_size)/2) , int((trash[1] + trash[1] + trash_size)/2) , 0.1)
                autoit.mouse_click("left",int((trash[0] + trash[0] + trash_size)/2), int((trash[1] + trash[1] + trash_size)/2), 1)
                pyautogui.moveTo(client["window_top"][0] + 150, client["window_top"][1] + 150, 0.1)
                autoit.mouse_click("left",client["window_top"][0] + 150, client["window_top"][1] + 150, 1)
                pyautogui.sleep(0.1)
                submit = Metin.locateAndFilterProp(client, destroy_item)
                if submit:
                    print("Item Deleted!")
                    destroy_button = int(submit[0] + 3* submit[2]/4 + 20), int(submit[1] + submit[3]/2)
                    pyautogui.moveTo(destroy_button[0], destroy_button[1] , 0.2)
                    autoit.mouse_click("left", destroy_button[0], destroy_button[1], 1)
                    pyautogui.sleep(0.4)
                    deleted.append(trash)
                    trash = Metin.locateAndFilterProp(client, trash_item)
        pydirectinput.press('i')
        
    def farm():
        while True:
            pydirectinput.keyDown("space")
            pyautogui.sleep(4)
            pydirectinput.keyUp("space")
            autoit.mouse_click('right')

            
            
    
def run_bot():
    bilogist = False
    # Locate the Healthbar for init
    healthbarlocations = 0
    while not healthbarlocations:
        healthbarlocations = Metin.locateHealthBar()
    client_id = 0
    for location in healthbarlocations:
        append_dict = {"client_id" : client_id,
                      "healthbar": location,
                      "skills_timer" : 0,
                      "bugged_timer": 0,
                      "biologist_timer": 0,
                      "clear_inventory_timer" : 0,
                      "clear_inventory_bugged_timer" : 0,
                      "not_farming_loop_counter": 0,
                      "farming": False,
                      "window_top": (location[0] + 10, location[1] - 740)
                     }
        clients.append(copy.deepcopy(append_dict))
        client_id += 1
    while True:
        for client in clients:
            Metin.collectLoot(client)
            #noticed that sometimes it doesn't loot
            if client["not_farming_loop_counter"] > 5:
                Metin.collectLoot(client)
                pydirectinput.keyDown('a')
                pydirectinput.keyDown('s')
                pyautogui.sleep(3)
                pydirectinput.keyUp('a')
                pydirectinput.keyUp('s')
                pydirectinput.press('q')
                pydirectinput.press('q')
                client["not_farming_loop_counter"] = 0
            if bilogist and (time.time() - client["biologist_timer"] > 650):
                Metin.biologist(client)
            loggout_location = Metin.locateAndFilterProp(client, logged_out_image)
            if loggout_location:
                Metin.handleLogout(clients, client) 
            pyautogui.moveTo(client["window_top"][0], client["window_top"][1], 0.2)
            autoit.mouse_click("left",client["window_top"][0], client["window_top"][1],2)
            if Metin.locateAndFilterProp(client, settings):
                print("Closing Settings!")
                pydirectinput.press('escape')
            if(time.time() - client["clear_inventory_timer"] > 500):
                client["clear_inventory_bugged_timer"] = time.time()
                Metin.clearInventory(client)
                client["clear_inventory_timer"] = time.time()
            if( time.time() - client["skills_timer"] > 300):
                client["skills_timer"] = time.time()
                Metin.useSkills(client)
            #try to find a metin:
            if len(Metin.locateAllAndFilterProp(client, lvl)) > 1:
                pydirectinput.keyDown('a')
                pydirectinput.keyDown('s')
                pyautogui.sleep(2)
                pydirectinput.keyUp('a')
                pydirectinput.keyUp('s')
                break
            if not client["farming"]:
                client["not_farming_loop_counter"] += 1
                if(Metin.locateAndFilterProp(client, metin_health_bar_image)):
                    Metin.collectLoot(client)
                    pydirectinput.keyDown('space')
                    pyautogui.sleep(1)
                    pydirectinput.keyUp('space')
                    pydirectinput.keyDown('a')
                    pydirectinput.keyDown('s')
                    pyautogui.sleep(1)
                    pydirectinput.keyUp('a')
                    pydirectinput.keyUp('s')
                    pydirectinput.press('escape')
                    client["bugged_timer"] = time.time()
                    break
                if Metin.findMetinOpenCV(client):
                    client["bugged_timer"] = time.time()
                    client["farming"] = True
                    break
                else:
                    Metin.lookaround()
                    Metin.lookaround()
                    break
                #check if the metin is still alive
            if Metin.checkIfMetinStillAlive(client):
                if(time.time() - client["bugged_timer"] > 20):
                    Metin.collectLoot(client)
                    pydirectinput.press('escape')
                    pydirectinput.keyDown('a')
                    pydirectinput.keyDown('s')
                    pydirectinput.keyDown('q')
                    pyautogui.sleep(1)
                    pydirectinput.keyUp('a')
                    pydirectinput.keyUp('s')
                    pydirectinput.keyUp('q')
                    pydirectinput.keyDown('space')
                    time.sleep(1)
                    pydirectinput.keyUp('space')
                    client["bugged_timer"] = time.time()
                    client["farming"] = True
                    print("UnBugging client " + str(client["client_id"]) + "!")
                    break
            else:
                client["farming"] = False
                Metin.collectLoot(client)
                if Metin.findMetinOpenCV(client):
                    client["bugged_timer"] = time.time()
                    client["farming"] = True
                    client["not_farming_loop_counter"] = 0

                    



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

