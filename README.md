This is a tool for pokeMMO automated farm! Built with fun in mind :))

# PokeGame
This class has many utility functions for manipulating the game's input:
- isHorde
- readScreen 
    - Uses opencv and pytesseract to read the screen
- check_for_shiny 
    - Uses the pokemon text to check for shinies
- detectFirstOccImage
    - uses pyautogui to detect the first occurence of an image on the screen
- detectImage
    - uses pyautogui to detect all occurences of an image on the screen
- holdkey
    - holds an array of keys for a given amount of time
- moveMouseAndClick
    - moves the mouse to a given position and clicks (accepts floats as the x and y unlike autoit)
- checkForCaptcha
    - checks for a reference image of the top of the captcha window. It's best that you screenshot the top of the captcha window and use that as the reference image.  
- logScreemshot 
    - Used to save a screenshot at any point in the code
## Current State
There are 3 different scripts with different functions:
- farm.py
    - Farm EXP, they all start with walking to the spot and then calling a generic farmEXP function:
        - Kanto CinnaBar Island;
        - Kanto Island 2;
        - Kanto Pokemon League.
    - Farm Abras Kanto:
        - This is a rather old script wich is not very easy to setup.
    - Farm Payday:
        - Unova Undella Bay (my meowth can kill them in one shot so it's programmed with that in mind). It farms thief on luvdiscs and then payday on the rest. If the icon of the meowth with and Icon is detected the item will be auto removed from the pokemon.
        - Kanto Island 5.
    - Includes a somewhat working example of farming the Pewter City Gym with:
        - 1st round whimsicott and torkoal
        - Switch to 2 typhlosions and spam Eruption 
- farmBeast.py
    - farmBeasts function:
        - Go to any patch of grass in Johto and use the walkaround function to define a direction to walk. It is supposed to be used with a meowth using payday and, if the pokemon survives, night slash.
    - farmHordes
        - Use one of the functions followin functions to select the place you'll farm. All of them use sweet scent and then teleport to the PC and go back. Supported spots:
            - runJohtoFromPCToBellowSafari
            - runJohtoFromPCToRoute42
            - runJohtoFromPCToRoute45
    - farmDittoCave
        - Not sure what I wanted to do with it but right now it doesn't do anything.
        - includes a runHoennFromPCToDittoCave that may be useful for other scripts.
- fish.py
    - This is a simple script that can be used anywhere. Position youself somewhere it's possible to fish and it will spam encounter until it finds a shiny. It will then send a push notification to your phone and stop the script. 
It's finally up! Star the repo and follow me because I've some commitment to this project!

- farmGyms already has a bunch of functions to run from PC to gyms, mostly in kanto. It's hard to get it to work, atleast with my current team. If the 2 initial pokemon die and the typhlosion don't it works fine!

## Farm.py
# Farm Abras funtion
This was the very first function developed for this bot and it's not very easy to setup but it's a good example of how to use the bot!
It has a walking function that's random but tries to keep itself in the lower right and preferes to walk up and down since the farm area in kanto is around 3*15.
It's programmed to use sleep powder in the first move so that you can throw at least 2 poke balls!
[Watch it sped up!](pokemmo8x.mp4)

# Shiny Detection
This was the hardest function to implement requiring a bit of research!
The best way i found to detect shinies was to use opencv and pytesseract!
Checkout pokeGame.py's check_for_shiny(self)! 
The idea is to extract color using HSV decomposition and then pytesseract to accuratly detect the text name of pokemons in battle!
Since pokemmo writes Shiny in the name of the pokemon if it is one!
Keep in mind that IF YOU USE ANY CUSTOM STRINGS make sure to remove any alteration to the name of shiny pokemons! Billy's string put two white squares around the name.

# Push notifications
I've implemented a push notification system using the gotify api!
You should download the gotify server on [github](https://github.com/gotify/server/releases) and run the exe. This will create a server on port 80 and you can access a web ui through your browser on localhost. Login with the default credentials:
Username: admin
Password: admin
Setup an application and copy the token to the code. Download the gotify app on your phone and use your local network ip to connect to the server. You should now be able to receive notifications on your phone!  
**Remember to always turn on the server before running the bot!**

I love doing openCV bots for my favorite games since if you don't abuse the amount of time the bot is running there's no real danger of being bannned!
Hopefully this will be of use for you!