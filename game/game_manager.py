import random
from pyglet import text
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
        self.game_gestures.clear()
        self.tie = False
    

    def determine_winner(self):
        if len(self.game_gestures) == 2:
            if self.game_gestures[0] == self.game_gestures[1]:
                self.winner = None
                return
            if self.game_gestures[0] == "rectangle":
                if self.game_gestures[1] == "v":
                    if self.mode == "com":
                        self.winner = "Player"
                    elif self.mode == "multi":
                        self.winner = "Player 2"
                elif self.game_gestures[1] == "circle":
                    if self.mode == "com":
                        self.winner = "COM"
                    elif self.mode == "multi":
                        self.winner = "Player 1"

            elif self.game_gestures[0] == "circle":
                if self.game_gestures[1] == "rectangle":
                    if self.mode == "com":
                        self.winner = "Player"
                    elif self.mode == "multi":
                        self.winner = "Player 2"
                elif self.game_gestures[1] == "v":
                    if self.mode == "com":
                        self.winner = "COM"
                    elif self.mode == "multi":
                        self.winner = "Player 1"

            elif self.game_gestures[0] == "v":
                if self.game_gestures[1] == "circle":
                    if self.mode == "com":
                        self.winner = "Player"
                    elif self.mode == "multi":
                        self.winner = "Player 2"
                elif self.game_gestures[1] == "rectangle":
                    if self.mode == "com":
                        self.winner == "COM"
                    elif self.mode == "multi":
                        self.winner = "Player 1"


    def draw_game_info(self, height):
        if self.mode == "com":
            text.Label(f'Your turn', font_size=20, x=100, y=height-30, anchor_x='center').draw()
        elif self.mode == "multi":
            if len(self.game_gestures) == 0:
                text.Label('Turn: Player 1', font_size=20, x=100, y=height-30, anchor_x='center').draw()
            elif len(self.game_gestures) == 1:
                text.Label('Turn: Player 2', font_size=20, x=100, y=height-30, anchor_x='center').draw()


    def draw_finish_screen(self, width, height, y_default):
        if len(self.game_gestures) == 2:
            text.Label(f"Winner: {self.winner}", font_size=24, x=width // 2, y=y_default + 40, anchor_x='center').draw()
            if self.mode == "com":
                text.Label(f"Your symbol: {self.game_gestures[1]}", font_size=16, x=width // 2, y=y_default - 30, anchor_x='center').draw()
                text.Label(f"COM symbol: {self.game_gestures[0]}", font_size=16, x=width // 2, y=y_default - 2 * 30, anchor_x='center').draw()
            elif self.mode == "multi":
                text.Label(f"Player 1 symbol: {self.game_gestures[0]}", font_size=16, x=width // 2, y=y_default - 30, anchor_x='center').draw()
                text.Label(f"Player 2 symbol: {self.game_gestures[1]}", font_size=16, x=width // 2, y=y_default - 2 * 30, anchor_x='center').draw()