import pygame
import numpy as np
from constants import (
    SCREEN_RESOLUTION,
    GREY,
    RED,
    PLAYER_IMAGE_PATH,
    ENEMY_IMAGE_PATH
)
from controls import Player, Enemy

pygame.init()


screen = pygame.display.set_mode(SCREEN_RESOLUTION)

pygame.display.set_caption('Space Invaders')
clock = pygame.time.Clock()


def quitgame():
    pygame.quit()
    quit()


def game_loop():
# LOOP PRINCIPAL DEL JUEGO
    player = Player(
        [SCREEN_RESOLUTION[0] * 0.45, SCREEN_RESOLUTION[1] * 0.8],
        [82, 82],
        [0, 0],
        pygame.image.load(PLAYER_IMAGE_PATH)
    )

    enemys = []
    for i in range(3):
        enemy = Enemy(
            [0 + 95*i, 100],
            [82, 82],
            [0, 0],
            pygame.image.load(ENEMY_IMAGE_PATH)
        )
        enemys.append(enemy)

    looping = True
    while looping:
        # read keys
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            player.speed = [0, 0]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    quitgame()
                if event.key == pygame.K_LEFT:
                    if player.pos[0] > 0:
                        player.speed[0] = - 5
                if event.key == pygame.K_RIGHT:
                    if player.pos[0] < SCREEN_RESOLUTION[0]:
                        player.speed[0] = 5
                if event.key == pygame.K_SPACE:
                    player.shoot()
        # Move
        player.move()
        player.move_projectils()
        [e.move() for e in enemys]
        
        # Collisions
        # looping = looping * player.collision(enemy)
        for i, e in enumerate(enemys):
            hit = player.collision_projectils(e)
            if hit:
                hit = False
                enemys.pop(i)
                if len(enemys) == 0:
                    print('Ganamo')
                break
        
        # Draw
        screen.fill(GREY)

        # DRAW
        player.draw(screen)
        player.draw_projectils(screen)
        [e.draw(screen) for e in enemys]

        # New line
        if enemys[0].pos[0] < 0 and enemys[0].dir == -1:
            [e.new_line(1) for e in enemys]

        if (
            ((enemys[-1].pos[0] + enemys[-1].size[0]) > SCREEN_RESOLUTION[0])
            and enemys[-1].dir == 1):
            [e.new_line(-1) for e in enemys]


        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    game_loop()
