import pygame as pg
import sys
from sprites import Player, Goals, Ball
from ui import Block, Text
from config import (
    SCREEN_HEIGHT, SCREEN_WIDTH, BACKGROUND_COLOUR, FPS, BALL_PLAYER_KICK_DISTANCE
)

pg.init()

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 

player = Player(
    colour=(255, 0, 0), 
    width=50, 
    height=50, 
    xpos=400, 
    ypos=100, 
    speed=3.5
)

goals = Goals(
    colour=(0, 255, 0),
    width=100,
    height=40,
    xpos=(SCREEN_WIDTH // 2) - 50,
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
    colour=(255, 0, 0),
    xpos=10,
    ypos=10,
    text='Score : 0',
    font_size=25
)

# menu = Block(
#     colour=(255, 0, 0),
#     xpos=0,
#     ypos=SCREEN_HEIGHT + 50,
#     width=SCREEN_WIDTH,
#     height=100
# )

# exit_button = Block(
#     colour=(100, 100, 100),
#     xpos=SCREEN_WIDTH // 6,
#     ypos=SCREEN_HEIGHT + 80,
#     width=100,
#     height=40
# )

# pause_button = Block(
#     colour=(100, 100, 100),
#     xpos=(SCREEN_WIDTH // 6) * 3,
#     ypos=SCREEN_HEIGHT + 80,
#     width=100,
#     height=40
# )

clock = pg.time.Clock()

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

        goals.draw(screen)
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
        # menu.draw(screen)
        # exit_button.draw(screen)
        # pause_button.draw(screen)

        clock.tick(FPS)
        pg.display.update()
        screen.fill(BACKGROUND_COLOUR)


if __name__ == '__main__':
    main()