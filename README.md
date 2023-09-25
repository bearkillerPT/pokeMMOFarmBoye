This is a tool for pokeMMO automated farm! Built with fun in mind :))

# PokeGame
This class has many utility functions for manipulating the game's input!

# FarmBoye
Defined in farm.py this is the actual bot. The objectives are easy to set (search for abra_text).
It's finally up! Star the repo and follow me because I've some commitment to this project!

## Current State
# Farm Abras funtion
Currently the bot knows only how to farm abras. 
It has a walking function that's random but tries to keep itself in the lower right and preferes to walk up and down since the farm area in kanto is around 3*15.
It's programmed to use sleep powder in the first move so that you can throw at least 2 poke balls!
[Watch it sped up!](pokemmo8x.mp4)

# Farm EXP Island 2
A function that uses Sweet scent (hotkey 5) and teleport (hotkey 6) to farm exp killing golducks while performing image to text analysis to check for shinies!

# Pokemon League Cave Shiny Hunt
A function purely made to catch shinies. It uses Sweet Scent 6 times and then teleports to the PC.

# Shiny Detection
This was the hardest function to implement requiring a bit of research!
The best way i found to detect shinies was to use opencv and pytesseract!
Checkout pokeGame.py's check_for_shiny(self)! 
The idea is to extract color using HSV decomposition and then pytesseract to accuratly detect the text name of pokemons in battle!
Since pokemmo writes Shiny in the name of the pokemon if it is one!

# Push notifications
I've implemented a push notification system using the gotify api!
You should download the gotify server on [github](https://github.com/gotify/server/releases) and run the exe. This will create a server on port 80 and you can access a web ui through your browser on localhost. Setup an application and copy the token to the code. Download the gotify app on your phone and use your local network ip to connect to the server. You should now be able to receive notifications on your phone!  

I love doing openCV bots for my favorite games since if you don't abuse the amount of time the bot is running there's no real danger of being bannned!
Hopefully this will be of use for you!