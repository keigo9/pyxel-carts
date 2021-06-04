from collections import deque, namedtuple
from random import randint
import pyxel

Point = namedtuple("Point", ["w", "h"])  # 猫の向き

UP = Point(-16, 16)
DOWN = Point(16, 16)
RIGHT = Point(-16, 16)
LEFT = Point(16, 16)


COL_BACKGROUND = 3
COL_BODY = 11
COL_HEAD = 7
COL_DEATH = 8
COL_APPLE = 8

TEXT_DEATH = ["GAME OVER", "(Q)UIT", "(R)ESTART"]
COL_TEXT_DEATH = 0
HEIGHT_DEATH = 30

WIDTH = 160
HEIGHT = 400

HEIGHT_SCORE = pyxel.FONT_HEIGHT
COL_SCORE = 6
COL_SCORE_BACKGROUND = 5

class App:
    def __init__(self):
        pyxel.init(160, 120, caption="MarioCart")
        pyxel.load("assets/carts.pyxres")
        self.direction = RIGHT

        # Score
        self.score = 0
        # Starting Point
        self.player_x = 42
        self.player_y = 60
        self.player_vy = 0
        self.getItem = [(randint(0, 144) ,i * 45 , True) for i in range(4)]
        self.lostItem = [(i * 60, randint(0, 104), True) for i in range(4)]
        self.getItem2 = [(i * 60, randint(0, 104), True) for i in range(4)]
        self.lostItem2 = [(randint(0, 144) ,i * 45 , True) for i in range(4)]
        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self):
        """Initiate key variables (direction, snake, apple, score, etc.)"""

        self.death = False
        self.score = 0

        pyxel.playm(0, loop=True)
        

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_R):
            self.reset()
        
    
        self.update_player()

        for i, v in enumerate(self.getItem):
            self.getItem[i] = self.update_getItem(*v)
        
        for i, v in enumerate(self.lostItem):
            self.lostItem[i] = self.update_lostItem(*v)

        for i, v in enumerate(self.getItem2):
            self.getItem2[i] = self.update_getItem2(*v)

        for i, v in enumerate(self.lostItem2):
            self.lostItem2[i] = self.update_lostItem2(*v)
        

    def update_player(self):
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD_1_LEFT):
            self.player_x = max(self.player_x - 2, 0)
            self.direction = LEFT

        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD_1_RIGHT):
            self.player_x = min(self.player_x + 2, pyxel.width - 16)
            self.direction = RIGHT

        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD_1_UP):
            self.player_y = max(self.player_y - 2, 0)
            self.direction = UP

        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD_1_DOWN):
            self.player_y = min(self.player_y + 2, pyxel.height - 16)
            self.direction = DOWN

    def death_event(self):
        """Kill the game (bring up end screen)."""
        self.death = True  # Check having run into self

        pyxel.stop()
        

        


    def draw(self):
        if self.death:
            self.draw_death()

        else:

            # bg color
            pyxel.cls(12)

            # draw coin
            for x, y, is_active in self.getItem:
                if is_active:
                    pyxel.blt(x, y, 0, 16, 0, 16, 16, 12)
            # draw banana
            for x, y, is_active in self.lostItem:
                if is_active:
                    pyxel.blt(x, y, 0, 48, 0, 16, 16, 12)
            # draw kinoko
            for x, y, is_active in self.getItem2:
                if is_active:
                    pyxel.blt(x, y, 0, 80, 0, 16, 16, 12)
            # draw kuribo
            for x, y, is_active in self.lostItem2:
                if is_active:
                    pyxel.blt(x, y, 0, 64, 0, 16, 16, 12)
                    
            

            # draw car
            pyxel.blt(
                self.player_x,
                self.player_y,
                0,
                16 if self.player_vy > 0 else 0,
                0,
                self.direction[0],
                self.direction[1],
                12,
            )

            #draw ジュゲム
            for i in range(6):
                pyxel.blt(32*i,0,0,32,0,16,16,12)
            for i in range(5):
                pyxel.blt(0,32*i,0,32,0,16,16,12)
            for i in range(6):
                pyxel.blt(144-32*i,104,0,32,0,16,16,12)
            for i in range(5):
                pyxel.blt(144,104-32*i,0,32,0,16,16,12)
            
                    
            

            # スコアを表示
            s = "Score {:>4}".format(self.score)
            pyxel.text(105,95, s, 1)
            pyxel.text(104, 95, s, 7)

    def update_getItem(self, x, y, is_active):
        if is_active and abs(x - self.player_x) < 12 and abs(y - self.player_y) < 12 and not self.death:
            is_active = False
            self.score += 1
            self.player_vy = min(self.player_vy, -8)
            pyxel.play(3, 4)

        y += 1

        if y > 150:
            y -= 180
            x = randint(0, 144)
            is_active = True

        return (x, y, is_active)

    def update_lostItem(self, x, y, is_active):
        if is_active and abs(x - self.player_x) < 12 and abs(y - self.player_y) < 12:
            is_active = False
            self.player_vy = min(self.player_vy, -8)
            pyxel.play(3, 4)
            self.death_event()

        x -= 1

        if x < -40:
            x += 240
            y = randint(0, 104)
            is_active = True

        return (x, y, is_active)

    def update_getItem2(self, x, y, is_active):
        if is_active and abs(x - self.player_x) < 12 and abs(y - self.player_y) < 12 and not self.death:
            is_active = False
            self.score += 2
            self.player_vy = min(self.player_vy, -8)
            pyxel.play(3, 4)

        x += 2

        if x > 240:
            x = -240
            y = randint(0, 104)
            is_active = True

        return (x, y, is_active)


    def update_lostItem2(self, x, y, is_active):
        if is_active and abs(x - self.player_x) < 12 and abs(y - self.player_y) < 12:
            is_active = False
            self.player_vy = min(self.player_vy, -8)
            pyxel.play(3, 4)
            self.death_event()

        y -= 2

        if y < -30:
            y += 180
            x = randint(0, 144)
            is_active = True

        return (x, y, is_active)

    def draw_death(self):
        """Draw a blank screen with some text."""

        pyxel.cls(col=1)
        display_text = TEXT_DEATH[:]
        display_text.insert(1, "{:04}".format(self.score))
        for i, text in enumerate(display_text):
            y_offset = (pyxel.FONT_HEIGHT + 2) * i
            text_x = self.center_text(text, WIDTH)
            pyxel.text(text_x, HEIGHT_DEATH + y_offset, text, COL_TEXT_DEATH)

    @staticmethod
    def center_text(text, page_width, char_width=pyxel.FONT_WIDTH):
        """Helper function for calcuating the start x value for centered text."""

        text_width = len(text) * char_width
        return (page_width - text_width) // 2

App()
