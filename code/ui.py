import pygame as pg
from config import FONT

class Block():

    def __init__(self, colour:tuple[int], xpos:int, ypos:int, width:int, height:int) -> None:
        self.colour = colour
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height

    def draw(self, screen) -> None:
        pg.draw.rect(screen, self.colour, pg.Rect(
            self.xpos, self.ypos, self.width, self.height
        ), self.width)
        

class Text():

    def __init__(self, colour:tuple[int], xpos:int, ypos:int, text:str, font_size:int) -> None:
        pg.font.init()
        self.colour = colour
        self.xpos = xpos
        self.ypos = ypos
        self.text = text
        self.font_size = font_size
        self.font = pg.font.SysFont(FONT, font_size)
        self.text_surface = self.font.render(self.text, False, self.colour)

    def blit(self, screen:pg.Surface):
        screen.blit(self.text_surface, (self.xpos, self.ypos))

    def update_text(self, text):
        self.text_surface = self.font.render(text, False, self.colour)