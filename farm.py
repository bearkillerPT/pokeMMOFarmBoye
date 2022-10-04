from time import time
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
shiny_tentacool_head = 'images\\shiny_tentacool_head.png'


class pokeFarmBoye:
    def __init__(self, game: pokeGame) -> None:
        self.game = game

    def focusWindow(self):
        self.game.moveMouseAndClick(100, 10)

    #This function supposes you're already in the farming spot!
    def farmAbras(self):
        self.focusWindow()
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
        self.focusWindow()
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
    def farmEXPCinnabar(self):
        self.focusWindow()
        
        #Start in front of the nurse in the PC

        #Walk out of the PC and into the water (i use an Ampharos to discharge them all and exp share)
        self.game.holdKey(['x','down'], 1)
        self.game.holdKey(['x','right'], 2)
        pydirectinput.press('z')
        pyautogui.sleep(.5)
        pydirectinput.press('z')
        pyautogui.sleep(.5)
        pydirectinput.press('z')
        pyautogui.sleep(.5)
        pydirectinput.press('z')
        pyautogui.sleep(1)
        #go to pokemon summary and favorite the sweet scent to key 5 or some other (20pp 5 per use)
        for i in range(4): 
            print("sweet scent")
            pydirectinput.press('5')
            # wait until the battle ui is shown
            pyautogui.sleep(13)
            if self.game.detectFirstOccImage(shiny_tentacool_head, grayscale=False):
                while True:
                    pyautogui.sleep(10000)
            pydirectinput.press("z")
            pyautogui.sleep(.2)
            pydirectinput.press("down")
            pyautogui.sleep(.1)
            pydirectinput.press("left")
            pyautogui.sleep(.1)
            pydirectinput.press("z")
            pyautogui.sleep(.2)
            pydirectinput.press("z")
            while self.game.detectFirstOccImage(ready_to_farm) == None:
                pyautogui.sleep(1)
            print("I'm ready to farm again!")
            pyautogui.sleep(.5)

        
        print("Gotta go JUICE UP!")
        
        #go to pokemon summary and favorite the teleport to key 6 or some other 
        pydirectinput.press("6")
        pyautogui.sleep(3)
        #Or fly and go inside
        #pydirectinput.press("1")
        #pyautogui.sleep(.5)
        #pydirectinput.press("z")
        #pyautogui.sleep(3)
        pydirectinput.press('z')
        pyautogui.sleep(1)
        pydirectinput.press('z')
        pyautogui.sleep(1)
        pydirectinput.press('z')
        pyautogui.sleep(2)
        pydirectinput.press('z')
        pyautogui.sleep(.5)
        pydirectinput.press('z')
        pyautogui.sleep(.5)
        pydirectinput.press('z')
        pyautogui.sleep(.5)
        pydirectinput.press('z')





def run_bot():
    poke_game = pokeGame()
    farm_boye = pokeFarmBoye(poke_game)
    init_game_time = time()
    farm_duration = 60 * 15
    while True:
        if login_box := poke_game.detectFirstOccImage(image_login_1, 0.8):
            farm_boye.handleLogin(login_box)

        if(time() > init_game_time + farm_duration):
            print("I'm done! In:" + str(time() - init_game_time) + "and was supposed to have lasted for " + str(farm_duration) + " but I had to kill'em all...")
            return
        

        farm_boye.farmEXPCinnabar()
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
