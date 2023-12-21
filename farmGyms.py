import pydirectinput
import pyautogui
import time
import pokeGame

battle_ui_image = 'images\\fight_ui.png'
typhlosion_icon = 'images\\typhlosion.png'

def goFromPewterCityPCToGym(game):
        game.holdKey(['x', 'right'], .75)
        game.holdKey(['x', 'up'], 2.25)
        game.holdKey(['x', 'left'], 2.2)
        game.holdKey(['x', 'down'], .75)
        game.holdKey(['x', 'right'], 1)
        game.holdKey(['x', 'up'], 2.5)
        pydirectinput.press('z')

def confrontGymLeader(game): 
    pydirectinput.keyDown('x')
    while not game.detectImage(battle_ui_image, confidence=.7):
        pydirectinput.press('z')
        time.sleep(.5)
    pydirectinput.keyUp('x')


def battleGymLeader(game):
    # First use tailwind and Explosion
    #while not game.detectImage(battle_ui_image, confidence=.7):
    #    time.sleep(.5)
    #print('battle_ui detected')
    ## Use tailwind
    #pydirectinput.press('z')
    #time.sleep(.5)
    #pydirectinput.press('z')
    #time.sleep(.5)
    #pydirectinput.press('right')
    #time.sleep(.2)
    #pydirectinput.press('z')
    #time.sleep(.5)
    ## Now use explosion
    #pydirectinput.press('z')
    #time.sleep(.5)
    #pydirectinput.press('right')
    #time.sleep(.2)
    #pydirectinput.press('z')
    #time.sleep(.5)
    #pydirectinput.press('z')
    ##Now use the typhlosion
    ##Now let the typhlosions in
    #print("Wating for pokemon to die")
    #while not (all_typhlosions := game.detectImage(typhlosion_icon, confidence=.7)):
    #    time.sleep(.5)
    #for i, typhlosion in enumerate(all_typhlosions):
    #    if i > 1:
    #        break
    #    game.moveMouseAndClick(typhlosion.left + 10, typhlosion.top + 10)    
    #    
    while not game.detectImage(battle_ui_image, confidence=.7):
        time.sleep(.5)
    # 3 turns erupting 6 pokemmon
    for i in range(3):
        print('battle_ui detected')
        pydirectinput.press('z')
        time.sleep(.5)
        pydirectinput.press('left')
        time.sleep(.1)
        pydirectinput.press('up')
        time.sleep(.1)
        pydirectinput.press('z')
        time.sleep(.5)
        pydirectinput.press('z')
        time.sleep(.5)
        pydirectinput.press('z')
        time.sleep(.5)
        pydirectinput.press('left')
        time.sleep(.1)
        pydirectinput.press('up')
        time.sleep(.1)
        pydirectinput.press('z')
        time.sleep(.5)
        pydirectinput.press('z')
        time.sleep(1)
        if i < 2:
            while not game.detectImage(battle_ui_image, confidence=.7):
                time.sleep(.5)
    
    print("done!")

def goFromFuchsiaCityPCToGym(game):
    game.holdKey(['down'], .1)
    game.holdKey(['x','left'], 2.6)
    game.holdKey(['x','up'], .25)
    time.sleep(1)
    # Now we are in the gym
    game.holdKey(['x','right'], 1.5)
    game.holdKey(['x','up'], 3.25)
    game.holdKey(['x','left'], 2.5)
    game.holdKey(['x','down'], .2)
    game.holdKey(['x','right'], .3)
    game.holdKey(['x','down'], .3)
    game.holdKey(['x','left'], .2)
    game.holdKey(['x','down'], .7)
    game.holdKey(['x','right'], .5)
    game.holdKey(['x','down'], .2)
    game.holdKey(['x','right'], .15)
    game.holdKey(['x','up'], .2)

def goFromDewfordTownPCToGym(game):
    game.holdKey(['x','down'], 1)
    game.holdKey(['x','right'], .9)
    game.holdKey(['x','up'], .1)
    time.sleep(1)
    game.holdKey(['x','right'], .1)
    game.holdKey(['x','up'], .6)
    game.holdKey(['x','right'], .6)
    game.holdKey(['x','up'], 1)
    game.holdKey(['x','right'], .1)
    game.holdKey(['x','up'], 1.75)
    game.holdKey(['x','left'], 1.25)
    game.holdKey(['x','up'], .25)

def goFromPetalburgCityPCToGym(game):
    # This one is weird because it doesn't kill whimsecott
    game.holdKey(['x','left'], .7)
    game.holdKey(['x','up'], 1.4)
    time.sleep(1)
    print("gym to loaded")
    game.holdKey(['x','up'], .6)
    game.holdKey(['x','left'], .3)
    game.holdKey(['x','up'], .1)
    pydirectinput.press('z')
    time.sleep(1.25)
    pydirectinput.press('z')
    time.sleep(1.25)
    pydirectinput.press('z')
    time.sleep(1.25)
    pydirectinput.press('z')
    time.sleep(1.25)
    game.holdKey(['x','up'], .7)
    pydirectinput.press('z')
    time.sleep(1.25)
    pydirectinput.press('z')
    time.sleep(1.25)
    pydirectinput.press('z')
    time.sleep(1.25)
    pydirectinput.press('z')
    time.sleep(1.25)
    game.holdKey(['x','up'], .7)
    pydirectinput.press('z')
    time.sleep(1.25)
    pydirectinput.press('z')
    time.sleep(1.25)
    pydirectinput.press('z')
    time.sleep(1.25)
    pydirectinput.press('z')
    time.sleep(1.25)
    game.holdKey(['x','up'], .7)
    pydirectinput.press('z')
    time.sleep(1.25)
    pydirectinput.press('z')
    time.sleep(1.25)
    pydirectinput.press('z')
    time.sleep(1.25)
    pydirectinput.press('z')
    time.sleep(1.25)
    game.holdKey(['x','right'], .4)
    game.holdKey(['x','up'], .5)    

# HOENN petalbutg and rustboro city don't kill the whimsecott
# HOENN fortree easy needs to be done
game = pokeGame.pokeGame()
#goFromFuchsiaCityPCToGym(game)
#goFromPewterCityPCToGym(game)
#goFromDewfordTownPCToGym(game)
#goFromPetalburgCityPCToGym(game)
#confrontGymLeader(game)
#battleGymLeader(game)