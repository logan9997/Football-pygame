import pygame as pg
from utils import distance_two_points
import random
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT
)

class Sprite(pg.sprite.Sprite):
    def __init__(self, colour, width, xpos, ypos) -> None:
        self.colour = colour
        self.width = width
        self.xpos = xpos
        self.ypos = ypos
        self.display = True

    def draw(self, screen:pg.Surface) -> None:
        pg.draw.rect(screen, self.colour, pg.Rect(
            self.xpos, self.ypos, self.width, self.height
        ))
    
    def get_center(self) -> tuple[int]:
        return (self.xpos - (self.width // 2), self.ypos - (self.width // 2))


class Rect(Sprite):

    def __init__(self, colour, width, height, xpos, ypos) -> None:
        super().__init__(colour, width, xpos, ypos)
        self.height = height

    def boundaries(self):
        if self.xpos >= SCREEN_WIDTH - (self.width):
            self.xpos = SCREEN_WIDTH - (self.width)
        elif self.xpos <= 0:
            self.xpos = 0 
        
        if self.ypos >= SCREEN_HEIGHT - self.height:
            self.ypos = SCREEN_HEIGHT - self.height
        elif self.ypos <= 0:
            self.ypos = 0 

    def get_center(self) -> tuple[int]:
        return (self.xpos - (self.width // 2), self.ypos - (self.height // 2))
    

class Ball(Sprite):

    def __init__(self, colour, xpos, ypos, radius, width, y_change, x_change, acceleration) -> None:
        super().__init__(colour, width, xpos, ypos)
        self.radius = radius
        self.kicked = False
        self.x_change = y_change
        self.y_change = x_change
        self.acceleration = acceleration
        self.kicked_speed = 3
        
    def reset(self):
        print('RESETING')
        xpos = random.choice([random.randint(15, 100), random.randint(450, SCREEN_WIDTH-5)])
        ypos = -random.randint(5,25)
        acceleration = random.randint(1,5) / 1000
        x_change = random.randint(2, 3)  
        y_change = random.randint(2, 3) 
        if xpos > (500 - 20) // 2:
            y_change *= -1

        self.__init__(
            self.colour, xpos, ypos, self.radius, self.width, y_change, x_change, acceleration
        )

    def draw(self, screen:pg.Surface):
        pg.draw.circle(screen, self.colour, (self.xpos, self.ypos), self.radius, self.width)

    def move(self):
        if self.x_change > 0:
            self.x_change -= self.acceleration
        if self.y_change > 0:
            self.y_change -= self.acceleration

        self.xpos += self.x_change
        self.ypos += self.y_change

        off_screen_conditions = (
            self.xpos > SCREEN_WIDTH + (self.radius * 2),
            self.xpos < 0,
            self.ypos > SCREEN_HEIGHT + (self.radius * 2),
        )
        if True in off_screen_conditions:
            self.reset()

    def get_center(self) -> tuple[int]:
        return self.xpos, self.ypos


    def travel_to_goal(self):
        if self.kicked:
            self.ypos -= self.kicked_speed
            self.x_change = 0
            self.y_change = 0
        if self.ypos < 0:
            self.kicked = False
            self.display = False
            self.reset()


class Player(Rect):

    def __init__(self, colour, width, height, xpos, ypos, speed) -> None:
        super().__init__(colour, width, height, xpos, ypos)
        self.speed = speed

    def move(self, mouse_pos:tuple[int]):
        self.xpos = mouse_pos[0]- (self.width // 2)
        self.ypos = mouse_pos[1] - (self.height // 2)
        self.boundaries()

    def get_ball_player_distance(self, ball:Ball):
        plr_xpos, plr_ypos = self.get_center()
        ball_xpos, ball_ypos = ball.get_center()

        ball_player_distance = distance_two_points(
            plr_xpos, ball_xpos, plr_ypos, ball_ypos
        )
        return ball_player_distance
    
        
class Goals(Rect):

    def __init__(self, colour, width, height, xpos, ypos) -> None:
        super().__init__(colour, width, height, xpos, ypos)

    def has_scored(self, ball:Ball) -> bool:
        if (
            ball.xpos > self.xpos 
            and ball.xpos < self.xpos + self.width
            and ball.ypos < self.ypos + self.height
        ):
            ball.kicked = False
            ball.reset()
            return True
        return False


class Goalie(Rect):

    def __init__(self, colour, width, height, xpos, ypos, speed) -> None:
        super().__init__(colour, width, height, xpos, ypos)
        self.speed = speed

    def move(self, ball:Ball, goals:Goals):
        if self.xpos > ball.xpos:
            self.xpos -= self.speed
        elif self.xpos < ball.xpos:
            self.xpos += self.speed

        self.boundaries(goals)

    def boundaries(self, goals:Goals):
        if self.xpos > goals.xpos + goals.width:
            self.xpos = goals.xpos + goals.width
        elif self.xpos < goals.xpos - self.width:
            self.xpos = goals.xpos - self.width

    def shot_saved(self, ball:Ball) -> bool:
        ball_center = ball.get_center()
        ball_x_center = ball_center[0]
        ball_y_center = ball_center[1] - ball.radius

        goalie_center = self.get_center()
        goalie_x_center = goalie_center[0] 
        goalie_y_center = goalie_center[1] + (self.height // 2)

        if (
            ball_y_center <= goalie_y_center 
            and ball_x_center + ball.radius > goalie_x_center
            and ball_x_center - ball.radius < goalie_x_center 
        ):
            return True
        return False

        
