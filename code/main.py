import pygame as pg
import sys
from sprites import Player, Goals, Ball
from ui import Block, Text
from config import (
    SCREEN_HEIGHT, SCREEN_WIDTH, BACKGROUND_IMG, FPS, BALL_PLAYER_KICK_DISTANCE
)

pg.init()

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 

player = Player(
    colour=(255, 0, 0), 
    width=30, 
    height=30, 
    xpos=400, 
    ypos=100, 
    speed=3.5
)

goals = Goals(
    colour=(0, 255, 0),
    width=60,
    height=30,
    xpos=(SCREEN_WIDTH // 2) - 30,
    ypos=0
)

ball = Ball(
    colour=(255, 255, 255),
    xpos=100,
    ypos=140,
    radius=10,
    width=20,
    y_change=0.75,
    x_change=1.1
)

goals_counter = Text(
    colour=(0, 0, 0),
    xpos=10,
    ypos=10,
    text='Score : 0',
    font_size=25
)

clock = pg.time.Clock()
background = pg.image.load(BACKGROUND_IMG)

def main():

    score = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                if player.get_ball_player_distance(ball) < BALL_PLAYER_KICK_DISTANCE:
                    ball.kicked = True

        #sprites
        player.move(pg.mouse.get_pos())            
        player.draw(screen)

        if ball.kicked:
            if goals.has_scored(ball):
                score += 1
                goals_counter.update_text(f'Score : {score}')

        if ball.display:
            ball.draw(screen)
            
        if ball.kicked:
            ball.travel_to_goal()

        ball.move()

        #ui
        goals_counter.blit(screen)

        clock.tick(FPS)
        pg.display.update()
        screen.blit(background, (0,0))


if __name__ == '__main__':
    main()