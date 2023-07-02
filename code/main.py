import pygame as pg
import sys
from sprites import Player, Goals, Ball, Goalie
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
    height=20,
    xpos=(SCREEN_WIDTH // 2) - 20,
    ypos=0
)

ball = Ball(
    colour=(255, 255, 255),
    xpos=100,
    ypos=140,
    radius=10,
    width=20,
    y_change=0.75,
    x_change=1.1,
    acceleration=0.01
)

goalie = Goalie(
    colour=(100, 50, 150),
    width=20,
    height=10,
    xpos=(SCREEN_WIDTH // 2) - 5,
    ypos=32,
    speed=0.2
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
    paused = False

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if paused:
                        paused = False
                    else:
                        paused = True

            if event.type == pg.MOUSEBUTTONDOWN:
                if player.get_ball_player_distance(ball) < BALL_PLAYER_KICK_DISTANCE:
                    ball.kicked = True

        if not paused:

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

            goalie.draw(screen)
            goalie.move(ball, goals)

            if ball.kicked:
                if goalie.shot_saved(ball):
                    if ball.xpos <= goalie.get_center()[0] // 2:
                        ball.x_change = 1
                    else:
                        ball.x_change = -1

                    ball.y_change = 1
                    ball.acceleration = -0.001
                    ball.kicked = False

            #ui
            goals_counter.blit(screen)

            clock.tick(FPS)
            pg.display.update()
            screen.blit(background, (0,0))

        else:
            exit_button = Block(
                colour=(255, 0, 0),
                xpos=SCREEN_WIDTH // 2 + 50,
                ypos=SCREEN_HEIGHT // 2 + 20,
                width=100,
                height=40
            )
            exit_text = Text(
                colour=(255, 100, 150),
                xpos=SCREEN_WIDTH // 2 + 50,
                ypos=SCREEN_HEIGHT // 2 + 20,
                text='EXIT',
                font_size=15
            )

            exit_button.draw(screen)
            exit_text.blit(screen)


if __name__ == '__main__':
    main()