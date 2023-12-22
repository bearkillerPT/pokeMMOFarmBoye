from time import time
import sys
from tokenize import String
from turtle import right
from cv2 import log
import pyscreenshot as sc
import pyautogui
import numpy as np
import cv2 as cv
from regex import F
from pokeGame import pokeGame
import pydirectinput
from random import random
import pytesseract
import requests
import time

map_top = 'images\\map_top.png'
image_login_1 = 'images\\login_1.png'
image_login_2 = 'images\\login_2.png'
image_login_3 = 'images\\login_3.png'
abra = 'images\\abra.png'
abra_text = 'images\\abra_text.png'
fight_ui_image = 'images\\fight_ui.png'
fight_image = 'images\\fight.png'
pokeball_text = 'images\\pokeball_text.png'
new_pokemon_text = 'images\\new_pokemon_text.png'
sleep_powder = 'images\\sleep_powder.png'
ready_to_farm = 'images\\ready_to_farm.png'
ready_to_farm_pl = 'images\\ready_to_farm_pl.png'
ready_to_farm_cinnabar = 'images\\ready_to_farm_cinnabar.png'   
shiny_tentacool_head = 'images\\shiny_tentacool_head.png'
shiny_text = 'images\\shiny_text.png'
logout_text = 'images\\logout.png'
yes_text = 'images\\yes.png'
evolving = 'images\\evolving.png'
reference_position = 'images\\reference_position.png'
reference_hp = 'images\\reference_hp.png'
noPP = 'images\\noPP.png'
meowth_with_item = 'images\\meowth_with_item.png'
take_heart_scale = 'images\\take_heart_scale.png'
bills_strings = True
gotify_url = 'http://localhost:80'
app_token = 'APJQrj78re2CzhV'
def isPokemon(text):
    return text != '' and (
        'lv.' in text.lower() or 
        'lv,' in text.lower() or 
        'ly.' in text.lower() or
        'ly,' in text.lower()
        )

class pokeFarmBoye:
    def __init__(self, game: pokeGame) -> None:
        self.game = game
        self.total_encounters = int(open('encounters.count', 'r').read())

    def focusWindow(self):
        self.game.moveMouseAndClick(100, 10)

    #This function supposes you're already in the farming spot!
    def farmAbras(self):
        pyautogui.sleep(.5)
        while (fight_ui := self.game.detectFirstOccImage(fight_ui_image)) == None:
            if (new_pokemon_box := self.game.detectFirstOccImage(new_pokemon_text)) != None:
                self.game.moveMouseAndClick(new_pokemon_box.left + new_pokemon_box.width - 15, new_pokemon_box.top + 1/2*new_pokemon_box.height)

            moves = [('down', 'up'), ( 'right','left')]
            move_seq = round(random())
            selected_moves = moves[move_seq]
            move_time = random()
            if move_seq==0:
                move_time *= 3
            self.game.holdKey([selected_moves[1]], 2*move_time/3)
            pyautogui.sleep(.3)
            self.game.holdKey([selected_moves[0]], move_time)
            pyautogui.sleep(.3)
            continue
        abra_detected = self.game.detectFirstOccImage(abra_text, confidence=0.6)
        print(abra_detected)
        if abra_detected != None:
            self.game.moveMouseAndClick(fight_ui.left + 20, fight_ui.top + 1/4*fight_ui.height)
            sleep_powder_box = None
            while (sleep_powder_box := self.game.detectFirstOccImage(sleep_powder)) == None:
                continue
            self.game.moveMouseAndClick(sleep_powder_box.left + 1/2*sleep_powder_box.width, sleep_powder_box.top + 1/2*sleep_powder_box.height)

            while True:
                if (fight_ui := self.game.detectFirstOccImage(fight_ui_image)) == None:
                    if self.game.detectFirstOccImage(new_pokemon_text) != None:
                        return
                    continue
                self.game.moveMouseAndClick(fight_ui.left + 3/4*fight_ui.width, fight_ui.top + 1/4*fight_ui.height)
                menu_scroll_i = 0
                pyautogui.sleep(.5)
                while self.game.detectFirstOccImage(pokeball_text, confidence=0.9) == None:
                    menu_scroll_i += 1
                    if(menu_scroll_i < 6):
                        pydirectinput.press('right')
                    else:
                        pydirectinput.press('left')
                    pyautogui.sleep(.2)
                pydirectinput.press('z')
                pyautogui.sleep(8)
            
                if self.game.detectFirstOccImage(abra_text, confidence=0.6) == None or self.game.detectFirstOccImage(new_pokemon_text) != None:
                    return
            
        else:
            self.game.moveMouseAndClick(fight_ui.left + 3/4*fight_ui.width, fight_ui.top + 3/4*fight_ui.height)
            


    def handleLogin(self, login_box):
        self.game.moveMouseAndClick(login_box.left + login_box.width - 35,
                          login_box.top + login_box.height - 35)
        while (login_box := self.game.detectFirstOccImage(image_login_2)) == None:
            continue
        self.game.moveMouseAndClick(login_box.left + login_box.width - 80,
                          login_box.top + login_box.height + 5)
        while (login_box := self.game.detectFirstOccImage(image_login_3)) == None:
            continue
        self.game.moveMouseAndClick(login_box.left + login_box.width - 100,
                          login_box.top + 120)


    def farmEXP(self, ready_image, allow_evolve=True):
        print("sweet scent")
        pyautogui.sleep(.5)
        pydirectinput.press('5')
        # wait until the battle ui is shown
        while (fight_ui := self.game.detectFirstOccImage(fight_ui_image)) == None:
            pyautogui.sleep(.5)
            pydirectinput.press('7')
        pyautogui.sleep(.5)
        while (text := self.game.readScreen()) == "":
            pyautogui.sleep(.5)
        if self.game.check_for_shiny(text) or self.game.detectFirstOccImage(shiny_text, confidence=0.8):
            print("HOLY SHIT FUCK")
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
            self.handleLogout()
            while True:
                pyautogui.sleep(10000)

        #pydirectinput.press("down")
        #pydirectinput.press("right")
        #pydirectinput.press("z")


        pydirectinput.press("z")
        pyautogui.sleep(.2)
        pydirectinput.press("down")
        pyautogui.sleep(.1)
        #pydirectinput.press("right")
        #pyautogui.sleep(.1)
        pydirectinput.press("z")
        pyautogui.sleep(.2)
        pydirectinput.press("z")
        small_counter = 0
        while self.game.detectFirstOccImage(ready_image) == None:
            small_counter += 1
            if small_counter == 10:
                print("Help")
            if(self.game.detectFirstOccImage(evolving)):
                if not allow_evolve:
                    pyautogui.press('x')
                    pyautogui.sleep(.5)
                    yes_box = self.game.detectFirstOccImage(yes_text)
                    self.game.moveMouseAndClick(yes_box.left + yes_box.width/2, yes_box.top + yes_box.height/2)
                else: 
                    time.sleep(8)
            
            print("ignoring any kind of new moves")
            pydirectinput.press('x')
            pyautogui.sleep(.1)
            pydirectinput.press('z')
            
            pyautogui.sleep(4)
        self.total_encounters += 1
        open('encounters.count', 'w').write(str(self.total_encounters))
        print("I'm ready to farm again!")
        pyautogui.sleep(.5)

    def healPokemon(self):
        global bills_strings
        pydirectinput.press('6')
        time.sleep(5)
        print('In front of the PC! Starting healing...')
        if bills_strings:
            pydirectinput.press('z')
            time.sleep(1)
            pydirectinput.press('z')
            time.sleep(1)
            pydirectinput.press('z')
            time.sleep(1)
            pydirectinput.press('z')
            pydirectinput.keyDown('x')
            pydirectinput.keyDown('x')
            time.sleep(5)
            pydirectinput.keyUp('x')
            pydirectinput.keyUp('z')
        else:
            pydirectinput.keyDown('z')
            time.sleep(6)
            pydirectinput.keyUp('z')
            pydirectinput.keyDown('x')
            pydirectinput.keyDown('z')
            time.sleep(7)
            pydirectinput.keyUp('z')
            pydirectinput.keyUp('x')
        print('Healed! Exiting...')
        pydirectinput.keyDown('down')
        time.sleep(1.8)
        pydirectinput.keyUp('down')
        time.sleep(2)

    def farmEXPCinnabar(self):
        #Start in front of the nurse in the PC
        #Walk out of the PC and into the water (i use an Ampharos to discharge them all and exp share)
        self.game.holdKey(['x','down'], 1)
        pyautogui.sleep(.5)
        self.game.holdKey(['x','right'], 2)
        pyautogui.sleep(.5)
        pydirectinput.press('z')
        pyautogui.sleep(.75)
        pydirectinput.press('z')
        pyautogui.sleep(.75)
        pydirectinput.press('z')
        pyautogui.sleep(.5)
        pydirectinput.press('z')
        pyautogui.sleep(1)
        #go to pokemon summary and favorite the sweet scent to key 5 or some other (28pp 5 per use)
        for i in range(6): 
            self.farmEXP(ready_to_farm_cinnabar)
        self.healPokemon() 


    def farmEXPPokemonLeague(self):
        #Start in front of the nurse in the PC
        #Walk out of the PC and into the water (i use an Ampharos to discharge them all and exp share)
        self.game.holdKey(['x','down'], 2.5)
        pyautogui.sleep(.25)
        self.game.holdKey(['x','right'], .6)
        pyautogui.sleep(.25)
        self.game.holdKey(['x','down'], 1.5)
        pyautogui.sleep(.25)
        self.game.holdKey(['right'], .1)
        pyautogui.sleep(.25)
        self.game.holdKey(['x','down'], 1.5)
        pyautogui.sleep(.25)
        self.game.holdKey(['x','right'], .8)
        pyautogui.sleep(.25)
        self.game.holdKey(['x','down'], 1.7)
        pyautogui.sleep(.25)
        self.game.holdKey(['x','left'], .3)
        pyautogui.sleep(.25)
        self.game.holdKey(['x','up'], .3)
        #go to pokemon summary and favorite the sweet scent to key 5 or some other (28pp 5 per use)
        for i in range(6): 
            self.farmEXP(ready_to_farm_pl)
        self.game.holdKey(['x','down'], 1)
        pyautogui.sleep(1)
        self.healPokemon() 
        pyautogui.sleep(1)
        self.game.holdKey(['x','down'], .5)
        pyautogui.sleep(.1)
        self.game.holdKey(['left'], .3)
        pyautogui.sleep(.1)
        self.game.holdKey(['down'], .4)
        pyautogui.sleep(1)



    def farmEXPIsland2(self):
        #Start in front of the nurse in the PC
        #Walk out of the PC and into the water (i use an Ampharos to discharge them all and exp share)
        pyautogui.sleep(.5)
        self.game.holdKey(['x','right'], 1.1)
        self.game.holdKey(['x','up'], .3)
        self.game.holdKey(['x','right'], 1.25)
        self.game.holdKey(['x','up'], 1.75)

        pyautogui.sleep(1)
        pydirectinput.press('z')
        pyautogui.sleep(.5)
        pydirectinput.press('z')
        pyautogui.sleep(.5)
        pydirectinput.press('z')
        pyautogui.sleep(.5)
        pydirectinput.press('z')
        pyautogui.sleep(.5)
        pydirectinput.press('z')
        pyautogui.sleep(1)
        #go to pokemon summary and favorite the sweet scent to key 5 or some other (28pp 5 per use)
        for i in range(6): 
            self.farmEXP(ready_to_farm, allow_evolve=False)
        self.healPokemon() 

    def handleLogout(self):
        pydirectinput.press('esc')
        pyautogui.sleep(.5)
        while(logout_box := self.game.detectFirstOccImage(logout_text)) == None:
            pyautogui.sleep(.5)
            print(logout_box)
            pydirectinput.press('esc')
        pyautogui.click(logout_box.left + logout_box.width/2, logout_box.top + logout_box.height/2)
        while(yes_box := self.game.detectFirstOccImage(yes_text)) == None:
            pyautogui.sleep(.5)

        pyautogui.sleep(.5)
        pyautogui.click(yes_box.left + yes_box.width/2, yes_box.top + yes_box.height/2)
        pyautogui.sleep(.5)
        pyautogui.click(yes_box.left + yes_box.width/2, yes_box.top + yes_box.height/2)

    def farmPewterCityGym(self):
        pydirectinput.press('1')
        self.game.holdKey(['up'], 1)    
        self.game.holdKey(['left'], 1)    
        print(pydirectinput.PAUSE)
        pydirectinput.PAUSE = 0.05
        for i in range(4):
            pydirectinput.press('right')
            pydirectinput.press('down')
        pydirectinput.press('z')
        pydirectinput.PAUSE = 0.1
        pyautogui.sleep(5)

        self.game.holdKey(['right'], 1.5)
        self.game.holdKey(['up'], 3.75)
        self.game.holdKey(['left'], 3.75)
        self.game.holdKey(['down'], 1.5)
        self.game.holdKey(['right'], 1.75)
        self.game.holdKey(['up'], 2.2)
        pydirectinput.press('z')

    def dropMeowthHeartScale(self):
        hasItem = self.game.detectFirstOccImage(meowth_with_item, .9)
        if hasItem:
            pydirectinput.click(int(hasItem.left + hasItem.width / 2), int(hasItem.top + hasItem.height / 2))
            time.sleep(.5)
            take_item = self.game.detectFirstOccImage(take_heart_scale, .9)
            if take_item:
                pydirectinput.click(int(take_item.left + take_item.width / 2), int(take_item.top + take_item.height / 2))
                

    def farmPayday(self):
        place = "unova_undella_bay"
        if place == "kanto_island_5":
            self.game.holdKey(['x','left'], .7)
            self.game.holdKey(['x','down'], .65)
            self.game.holdKey(['x','right'], 2.25)
            self.game.holdKey(['x','up'], .3)
            self.game.holdKey(['right'], .2)
            self.game.holdKey(['x','up'], .4)
            self.game.holdKey(['x','right'], .4)
        elif place == "unova_undella_bay":
            self.game.holdKey(['x','left'], .7)
            chosen_path = int(random() * 3) % 2
            if chosen_path == 0:
                self.game.holdKey(['x','down'], .5)
                self.game.holdKey(['x','right'], 3.3)
            else:
                self.game.holdKey(['x','down'], 1.2)
        payDayPP = 32
        thiefPP = 25
        num_runs = 20 if place == "kanto_island_5" else payDayPP + thiefPP # it's fine to overstimate
        for i in range(num_runs):
            self.game.checkForCaptcha()
            min_x = 550
            max_x = 1000
            no_reference_position_count = 0
            if payDayPP == 0 or thiefPP == 0:
                break
            self.dropMeowthHeartScale()
            while not isPokemon((text := self.game.readScreen())):
                if place == "kanto_island_5":
                    if (x:=self.game.detectFirstOccImage(reference_position, confidence=0.8)):
                        if x.left > 1700:
                            self.healPokemon() 
                            return
                        if x.top < 85:
                            self.game.holdKey(['up'], .05)
                        walk_interval = random() * .75 + .5

                        if x.left < max_x:
                            self.game.holdKey(['x','left'], walk_interval)
                        else:
                            self.game.holdKey(['x','right'], walk_interval)
                    else: 
                        self.game.holdKey(['up'], .05)
                        no_reference_position_count += 1
                        pyautogui.sleep(1)
                else:
                    pydirectinput.press('4')
                    pydirectinput.press('z')
                    time.sleep(.1)
            while not self.game.detectFirstOccImage(fight_ui_image, .9):
                time.sleep(.1)
            if self.game.check_for_shiny(text) or self.game.detectFirstOccImage(shiny_text, confidence=0.8):
                print("HOLY SHIT FUCK")
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
                self.handleLogout()
                while True:
                    pyautogui.sleep(10000)
            hp_box=self.game.detectFirstOccImage(reference_hp, confidence=.90)
            pydirectinput.keyUp('x')
            if self.game.is_horde(text):
                pydirectinput.press("right")
                pyautogui.sleep(.25)
                pydirectinput.press("down")
                pyautogui.sleep(.25)
                pyautogui.press('z')
            elif place == "unova_undella_bay":
                hp_box=self.game.detectFirstOccImage(reference_hp, confidence=.90)
                pyautogui.press('z')
                pyautogui.sleep(.2)
                print("payDayPP", payDayPP,"thiefPP", thiefPP)
                if 'Luvdisc' in text or 'luvdisc' in text or 'Luvdise' in text or 'luvdise' in text:
                    thiefPP -= 1
                    pyautogui.press('z')
                    pydirectinput.keyDown('x')
                    pyautogui.sleep(12) # This is the worst case
                    # A reference image should be used instead.  
                else:
                    payDayPP -= 1
                    pydirectinput.press("down")
                    pyautogui.sleep(.1)
                    pyautogui.press('z')
                    pydirectinput.keyDown('x')
                    pyautogui.sleep(8)
                pydirectinput.keyUp('x')
            elif place == "kanto_island_5":
                while self.game.detectFirstOccImage(reference_position) == None:
                    if self.game.detectFirstOccImage(fight_ui_image):
                        hp_box=self.game.detectFirstOccImage(reference_hp, confidence=.90)
                        hp_text = sc.grab(bbox=(hp_box.left-hp_box.width, hp_box.top, hp_box.left, hp_box.top+hp_box.height))
                        hp_text.save('cocaine.png')
                        pyautogui.press('z')
                        pyautogui.sleep(.3)
                        pydirectinput.press("down")
                        pyautogui.sleep(.3)
                        pydirectinput.press("right")
                        pyautogui.sleep(.1)
                        pyautogui.press('z')
                        for i in range(4):
                            if self.game.detectFirstOccImage(noPP):
                                pyautogui.sleep(2)
                                pydirectinput.press("down")
                                pyautogui.sleep(.3)
                                pydirectinput.press("right")
                                pyautogui.sleep(.3)
                                pyautogui.press('z')
                                pyautogui.sleep(5)

                                self.healPokemon() 
                                return
                            pyautogui.sleep(.5)
            print("starting to farm again")   

        if hp_box:
            hp_text = sc.grab(bbox=(hp_box.left-hp_box.width, hp_box.top, hp_box.left, hp_box.top+hp_box.height))
            if  hp_text and hp_text != "":
                text = pytesseract.image_to_string( hp_text)
                print("parsed_hp",text)
                hp = 50
                try:
                    hp = int(text)
                    print("Current hp: " + str(hp))
                    if hp and hp < 100:
                        pyautogui.sleep(2)
                        pydirectinput.press("down")
                        pyautogui.sleep(.3)
                        pydirectinput.press("right")
                        pyautogui.sleep(.3)
                        pyautogui.press('z')
                        pyautogui.sleep(5)

                        self.healPokemon() 
                        return
                except:
                    print("Could not parse hp")
        
        start_time = time.time()
        while self.game.detectFirstOccImage(fight_ui_image) != None:
            pyautogui.sleep(.5)
            current_time = time.time()
            if current_time - start_time > 1*60:
                #self.healPokemon() 
                pydirectinput.press('right')
                pyautogui.sleep(.2)
                pydirectinput.press('down')
                pyautogui.sleep(.2)
                pydirectinput.press('z')
                start_time = time.time()

            elif place == "kanto_island_5" and current_time - start_time % 60*5 == 0:
                self.game.holdKey(['x','up'], .1)
            pyautogui.sleep(3)
        self.healPokemon() 

def run_bot():
    poke_game = pokeGame()
    farm_boye = pokeFarmBoye(poke_game)
    init_game_time = time.time()
    farm_boye.focusWindow()
    pyautogui.sleep(.5)
    farm_duration = 60 * 60 #1 hour
    if(len(sys.argv) == 2):
        farm_duration = 60 * int(sys.argv[1]) #First argument is time in min    

    while True:
        #if shit := poke_game.detectFirstOccImage(shiny_text, confidence=0.6):
        #    poke_game.moveMouseAndClick(floor(shit.left + shit.width/2), floor(shit.top + shit.height/2))
        #    print("HOLY SHIT FUCK")
        if(time.time() > init_game_time + farm_duration):
            print("I'm done! In:" + str((time.time() - init_game_time)/60) + " minutes and was supposed to have lasted for " + str(farm_duration/60) + " but I had to kill'em all...")
            farm_boye.handleLogout()
            pyautogui.sleep(60*60*3)

        if login_box := poke_game.detectFirstOccImage(image_login_1, 0.7):
            farm_boye.handleLogin(login_box)

        while True:     
            farm_boye.farmPayday()
            #print(poke_game.readScreen())
        

        #Pokemon slots farm
        #farm_boye.focusWindow()
        #poke_game.holdKey(['down'], 1)
        #pydirectinput.press('z')
        #pyautogui.sleep(0.01)
        #pydirectinput.press('z')
        #pyautogui.sleep(0.01)
        #pydirectinput.press('z')
        #pyautogui.sleep(0.01)
        #pydirectinput.press('z')


if __name__ == '__main__':
    run_bot()
