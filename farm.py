from tokenize import String
from cv2 import log
import pyautogui
from math import floor
import numpy as np
import cv2 as cv
from pokeGame import pokeGame
import pydirectinput



map_top = 'images\\map_top.png'
image_login_1 = 'images\\login_1.png'
image_login_2 = 'images\\login_2.png'
image_login_3 = 'images\\login_3.png'
abra = 'images\\abra.png'
abra_text = 'images\\abra_text.png'
fight_ui_image = 'images\\fight_ui.png'
pokeball_text = 'images\\pokeball_text.png'



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
            self.game.holdKey({'down'}, 0.5)
            pyautogui.sleep(.2)
            self.game.holdKey({'right'}, 0.2)
            self.game.holdKey({'up'}, 0.5)
            pyautogui.sleep(.5)
            self.game.holdKey({'left'}, 0.5)
            continue
        abra_detected = self.game.detectFirstOccImage(abra_text, confidence=0.8)
        print(abra_detected)
        if abra_detected != None:
            self.game.moveMouseAndClick(floor(fight_ui.left + 3/4*fight_ui.width), floor(fight_ui.top + 1/4*fight_ui.height))
        else:
            self.game.moveMouseAndClick(floor(fight_ui.left + 3/4*fight_ui.width), floor(fight_ui.top + 3/4*fight_ui.height))
            while self.game.detectFirstOccImage(pokeball_text, confidence=0.9) == None:
                pydirectinput.press('right')
                pyautogui.sleep(1.5)
            pydirectinput.press('z')
            
    

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


def run_bot():
    poke_game = pokeGame()
    farm_boye = pokeFarmBoye(poke_game)
    while True:
        if login_box := poke_game.detectFirstOccImage(image_login_1):
            farm_boye.handleLogin(login_box)
        farm_boye.farmAbras()


if __name__ == '__main__':
    run_bot()
