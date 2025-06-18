import random
from templates import templates

class GameManager:

    GESTURES = list(templates.keys())

    def __init__(self):
        self.mode = ""
        self.has_started = False
        self.has_finished = False
        self.tie = False
        self.game_gestures = []
        self.winner = None

    
    def start(self, mode):
        self.tie = False
        self.game_gestures.clear()
        if mode == "com":
            self.has_started = True
            self.mode = "com"
            self.game_gestures.append(random.choice(GameManager.GESTURES))
            print(self.game_gestures)
        elif mode == "multi":
            self.has_started = True
            self.mode = "multi"


    def restart(self):
        self.has_finished = False
        self.has_started = False
        self.mode = ""
        self.winner = None
    

    def determine_winner(self):
        print(self.game_gestures)
        if len(self.game_gestures) == 2:
            if self.game_gestures[0] == self.game_gestures[1]:
                self.winner = None
                return
            if self.game_gestures[0] == "rectangle":
                if self.game_gestures[1] == "v":
                    if self.mode == "com":
                        self.winner = "Player"
                    elif self.mode == "multi":
                        self.winner = "Player 1"
                elif self.game_gestures[1] == "circle":
                    if self.mode == "com":
                        self.winner = "COM"
                    elif self.mode == "multi":
                        self.winner = "Player 2"

            elif self.game_gestures[0] == "circle":
                if self.game_gestures[1] == "rectangle":
                    if self.mode == "com":
                        self.winner = "Player"
                    elif self.mode == "multi":
                        self.winner = "Player 1"
                elif self.game_gestures[1] == "v":
                    if self.mode == "com":
                        self.winner = "COM"
                    elif self.mode == "multi":
                        self.winner = "Player 2"

            elif self.game_gestures[0] == "v":
                if self.game_gestures[1] == "circle":
                    if self.mode == "com":
                        self.winner = "Player"
                    elif self.mode == "multi":
                        self.winner = "Player 1"
                elif self.game_gestures[1] == "rectangle":
                    if self.mode == "com":
                        self.winner == "COM"
                    elif self.mode == "multi":
                        self.winner = "Player 2"