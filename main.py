from unlock import unlock
from game import GamePlay

name  = unlock()

if name.lower() == "q":
    exit()
else:
    GamePlay(name)


