import pygame
import time
import random
import numpy as np
from constants import (
    SCREEN_RESOLUTION,
    GREY,
    RED,
    PLAYER_IMAGE_PATH,
    ENEMY_IMAGE_PATH
)
from controls import Player

pygame.init()


screen = pygame.display.set_mode(SCREEN_RESOLUTION)

pygame.display.set_caption('Space Invaders')
clock = pygame.time.Clock()


def quitgame():
    pygame.quit()
    quit()


def game_loop():
# LOOP PRINCIPAL DEL JUEGO
    looping = True
    while looping:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            player.speed = [0, 0]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    quitgame()
                if event.key == pygame.K_LEFT:
                    player.speed[0] = - 5
                if event.key == pygame.K_RIGHT:
                    player.speed[0] = 5

        # Move
        player.move()
        
        # Collisions
        # looping = looping * player.collision(enemy)

        # Draw
        screen.fill(GREY)

        # Draw Map
        
        # DRAW
        player.draw(screen)

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    player = Player(
        [SCREEN_RESOLUTION[0] * 0.45, SCREEN_RESOLUTION[1] * 0.8],
        [82, 82],
        [(0, 0, 0), 0],
        pygame.image.load(PLAYER_IMAGE_PATH)
    )
    loop = True

    while loop:
        game_loop()
