from time import time
import sys
from tokenize import String
from turtle import right
from cv2 import log
import pyautogui
from math import floor
import numpy as np
import cv2 as cv
from pokeGame import pokeGame
import pydirectinput
from random import random
import requests

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
ready_to_farm = 'images\\ready_to_farm_pl.png'
ready_to_farm_cinnabar = 'images\\ready_to_farm_cinnabar.png'   
shiny_tentacool_head = 'images\\shiny_tentacool_head.png'
shiny_text = 'images\\shiny_text.png'
logout_text = 'images\\logout.png'
yes_text = 'images\\yes.png'


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
                self.game.moveMouseAndClick(floor(new_pokemon_box.left + new_pokemon_box.width) - 15, floor(new_pokemon_box.top + 1/2*new_pokemon_box.height))

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
            self.game.moveMouseAndClick(floor(fight_ui.left + 20), floor(fight_ui.top + 1/4*fight_ui.height))
            sleep_powder_box = None
            while (sleep_powder_box := self.game.detectFirstOccImage(sleep_powder)) == None:
                continue
            self.game.moveMouseAndClick(floor(sleep_powder_box.left + 1/2*sleep_powder_box.width), floor(sleep_powder_box.top + 1/2*sleep_powder_box.height))

            while True:
                if (fight_ui := self.game.detectFirstOccImage(fight_ui_image)) == None:
                    if self.game.detectFirstOccImage(new_pokemon_text) != None:
                        return
                    continue
                self.game.moveMouseAndClick(floor(fight_ui.left + 3/4*fight_ui.width), floor(fight_ui.top + 1/4*fight_ui.height))
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
            self.game.moveMouseAndClick(floor(fight_ui.left + 3/4*fight_ui.width), floor(fight_ui.top + 3/4*fight_ui.height))
            


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

    def farmEXP(self):
        print("sweet scent")
        pyautogui.sleep(.5)
        pydirectinput.press('5')
        # wait until the battle ui is shown
        while (fight_ui := self.game.detectFirstOccImage(fight_ui_image)) == None:
            pyautogui.sleep(.5)
            pydirectinput.press('5')
        pyautogui.sleep(.5)
        if self.game.check_for_shiny() or self.game.detectFirstOccImage(shiny_text, confidence=0.8):
            print("HOLY SHIT FUCK")
            requests.post('https://api.mynotifier.app', {
                "apiKey": '011266e7-bd88-4109-b4f0-2cf1ef195b2c',
                "message": "Found a shiny hehe!",
                "description": "Bitch ruuuuuuuuuuuun you gotta catch the pokemans I can't do everything for you...",
                "type": "info", # info, error, warning or success
            })
            self.handleLogout()
            while True:
                pyautogui.sleep(10000)

        #pydirectinput.press("down")
        #pydirectinput.press("right")
        #pydirectinput.press("z")


        #pydirectinput.press("z")
        #pyautogui.sleep(.2)
        pydirectinput.press("down")
        pyautogui.sleep(.1)
        pydirectinput.press("right")
        pyautogui.sleep(.1)
        pydirectinput.press("z")
        pyautogui.sleep(.2)
        pydirectinput.press("z")
        while self.game.detectFirstOccImage(ready_to_farm) == None:
            pyautogui.sleep(1)
        self.total_encounters += 1
        open('encounters.count', 'w').write(str(self.total_encounters))
        print("I'm ready to farm again!")
        pyautogui.sleep(.5)

    def healPokemon(self):
        print("Gotta go JUICE UP!")
        
        #go to pokemon summary and favorite the teleport to key 6 or some other 
        pydirectinput.press("6")
        pyautogui.sleep(5)
        #Or fly and go inside
        #pydirectinput.press("1")
        #pyautogui.sleep(.5)
        #pydirectinput.press("z")
        #pyautogui.sleep(3)
        pydirectinput.keyDown('z')
        pyautogui.sleep(3.5)
        pydirectinput.keyUp('z')

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
            self.farmEXP()
        self.healPokemon() 


    def farmShiniesPokemonLeague(self):
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
            self.farmEXP()
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
        self.game.holdKey(['x','right'], 1.25)
        self.game.holdKey(['x','up'], .5)
        self.game.holdKey(['x','right'], 1.4)
        self.game.holdKey(['x','up'], 2)

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
            self.farmEXP()
        self.healPokemon() 
        pyautogui.sleep(1)
        self.game.holdKey(['x','down'], 1)
        pyautogui.sleep(1)

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



    


def run_bot():
    poke_game = pokeGame()
    farm_boye = pokeFarmBoye(poke_game)
    init_game_time = time()
    farm_boye.focusWindow()
    pyautogui.sleep(.5)
    farm_duration = 60 * 90 #1 + 1/2 hours
    if(len(sys.argv) == 2):
        farm_duration = 60 * int(sys.argv[1]) #First argument is time in min    

    while True:
        #if shit := poke_game.detectFirstOccImage(shiny_text, confidence=0.6):
        #    poke_game.moveMouseAndClick(floor(shit.left + shit.width/2), floor(shit.top + shit.height/2))
        #    print("HOLY SHIT FUCK")
        if(time() > init_game_time + farm_duration):
            print("I'm done! In:" + str((time() - init_game_time)/60) + " minutes and was supposed to have lasted for " + str(farm_duration/60) + " but I had to kill'em all...")
            farm_boye.handleLogout()
            pyautogui.sleep(4*farm_duration)

        if login_box := poke_game.detectFirstOccImage(image_login_1, 0.7):
            farm_boye.handleLogin(login_box)

        farm_boye.farmShiniesPokemonLeague()
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
