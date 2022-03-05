import pygame
import random
import os
from pygame import mixer

# initialise pygame
pygame.init()

# game window
DISPLAY_WIDTH = 1136
DISPLAY_HEIGHT = 720

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)

display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption('Castle Defender game')


bg1 = pygame.image.load('images/background/Снимок3.png').convert_alpha()
bg1 = pygame.transform.scale(bg1, (int(bg1.get_width()), int(bg1.get_height())))
mixer.music.load('sounds/back.wav')
mixer.music.set_volume(0.3)
mixer.music.play(-1)
display.blit(bg1, (0, 0))
pygame.display.update()

clock = pygame.time.Clock()
FPS = 60

level = 1
level_difficulty = 0
target_difficulty = 1000
high_score = 0
DIFFICULTY_MYLTIPLIER = 1.1
game_over = True
wait = False
next_level = False
ENEMY_TIMER = 1000
last_enemy = pygame.time.get_ticks()
enemies_alive = 0
TOWER_COST = 2500
flag = False
active = True

tower_positions = [
    [DISPLAY_WIDTH - 50, DISPLAY_HEIGHT - 200],
    [DISPLAY_WIDTH - 115, DISPLAY_HEIGHT - 200],
    [DISPLAY_WIDTH - 65, DISPLAY_HEIGHT - 150],
    [DISPLAY_WIDTH - 130, DISPLAY_HEIGHT - 150],
]

import castle
from castle import Tower, Castle
import enemies
from crosshair import Crosshair
import labels
from button import Button
import images

bad_castle_img, bg, bg1, backgr, backgr1, backgr2, button1, button2, button3, button4, tower100, repair_img, armour_img = images.process_images()

# create castle
good_castle = castle.Castle(display, castle.image, DISPLAY_WIDTH - 190, DISPLAY_HEIGHT - 450, 0.3)
#tower100 = pygame.transform.scale(tower100, (int(tower100.get_width()*0.28), int(tower100.get_height()*0.195)))

# create crosshair
crosshair = Crosshair()

# create towers
tower_group = pygame.sprite.Group()

# create bullets
bullet_group = pygame.sprite.Group()

# create enemies
enemy_group = pygame.sprite.Group()

# create buttons

repair_button = Button(DISPLAY_WIDTH - 320, 20, repair_img, 0.125)
tower_button = Button(DISPLAY_WIDTH - 208, 20, tower100, 0.153)
armour_button = Button(DISPLAY_WIDTH - 115, 20, armour_img, 0.04166)
start_button = Button(DISPLAY_WIDTH // 2 - 220, DISPLAY_HEIGHT // 2 - 70, button1, 0.4)
#setting_button = Button(DISPLAY_WIDTH // 2 - 220, DISPLAY_HEIGHT // 2 - 30, button2, 0.4)
exit_button = Button(DISPLAY_WIDTH // 2 - 220, DISPLAY_HEIGHT // 2 + 40, button3, 0.4)
restart_button = Button(DISPLAY_WIDTH // 2 - 220, DISPLAY_HEIGHT // 2 - 70, button4, 0.4)

# game loop
run = True
while run:

    clock.tick(FPS)
    if not game_over:
        display.blit(bg, (0, 0))

        # draw castle
        good_castle.draw()

        # draw tower
        #tower_group.draw(display)
        tower_group.update(enemy_group, bullet_group, good_castle.health)

        # draw crosshair
        pygame.mouse.set_visible(False)

        # draw enemies
        enemy_group.update(display, good_castle, bullet_group)

        labels.show_info(display, backgr1, backgr2, WHITE, good_castle, high_score, level, DISPLAY_WIDTH,
                         DISPLAY_HEIGHT)

        display.blit(bad_castle_img, (-230, DISPLAY_HEIGHT - 465))

        # draw buttons
        if repair_button.draw(display, active):
            good_castle.repair()

        if tower_button.draw(display, active):
            if good_castle.money >= TOWER_COST and len(tower_group) < len(tower_positions):
                tower = Tower(display, good_castle.images_tower,
                              tower_positions[len(tower_group)][0], tower_positions[len(tower_group)][1], 1)
                good_castle.money -= TOWER_COST
                tower_group.add(tower)

        if armour_button.draw(display, active):
            good_castle.armour()

        if good_castle.health > 0:

            good_castle.shoot(bullet_group)
            bullet_group.update(display, DISPLAY_WIDTH, DISPLAY_HEIGHT)
            bullet_group.draw(display)
            # check if max of enemies has been reached
            if level_difficulty < target_difficulty:
                if pygame.time.get_ticks() - last_enemy > ENEMY_TIMER and pygame.time.get_ticks() - now > 3500:
                    # create enemies
                    if wait:
                        wait = False
                    e = random.randint(0, len(enemies.enemy_types) - 1)
                    y = random.choice([150, 155, 160, 165, 170, 190, 185, 180, 175])
                    enemy = enemies.Enemy(enemies.enemy_health[e], enemies.enemy_animations[e],
                                            150, DISPLAY_HEIGHT - y, 1)
                    enemy_group.add(enemy)
                    last_enemy = pygame.time.get_ticks()
                    level_difficulty += enemies.enemy_health[e]

            if level_difficulty >= target_difficulty:
                enemies_alive = 0
                for e in enemy_group:
                    if e.alive:
                        enemies_alive += 1
                #print(enemies_alive)

                if enemies_alive == 0 and not next_level:
                    next_level = True
                    level_reset_time = pygame.time.get_ticks()

            if good_castle.score > high_score:
                high_score = good_castle.score

            if next_level:
                labels.draw_text(display, 'LEVEL COMPLETE!', labels.font70, WHITE, int(DISPLAY_WIDTH/3-10), int(DISPLAY_HEIGHT/2-50))

                if pygame.time.get_ticks() - level_reset_time > 2000:
                    next_level = False
                    level += 1
                    last_enemy = pygame.time.get_ticks()
                    target_difficulty *= DIFFICULTY_MYLTIPLIER
                    level_difficulty = 0
                    enemy_group.empty()

                # draw crosshair

        # check game_over
        else:
            #print("start")
            active = False

            flag = True
            #print("before restart")
            if restart_button.draw(display):

                active = True
                with open('score.txt', 'w') as file:
                    file.write(str(high_score))
                pygame.time.wait(800)
                pygame.mouse.set_visible(False)
                mixer.music.pause()
                tower_group.empty()
                bullet_group.empty()
                enemy_group.empty()
                level = 1
                good_castle = Castle(display, castle.image, DISPLAY_WIDTH - 190, DISPLAY_HEIGHT - 450)
                flag = False
                with open('score.txt', 'r') as file:
                    high_score = int(file.read())
                wait = True
                now = pygame.time.get_ticks()

            else:
                pass
            #print("exit")
            if exit_button.draw(display):
                with open('score.txt', 'w') as file:
                    file.write(str(high_score))
                run = False
            else:
                pass
            #print("before enemy update")
            enemy_group.update(display, good_castle, bullet_group, True)
        #print("before crosshair")
        crosshair.draw(display, flag)

    else:
        display.blit(bg1, (0, 0))
        pygame.mouse.set_visible(True)
        if start_button.draw(display):
            with open('score.txt', 'r') as file:
                high_score = int(file.read())
            mixer.music.pause()
            game_over = False
            now = pygame.time.get_ticks()
            pygame.time.wait(800)

        if exit_button.draw(display):
            with open('score.txt', 'w') as file:
                file.write(str(high_score))
            run = False

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
