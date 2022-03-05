import pygame
import os
from pygame import mixer

enemy_animations = []
enemy_types = ['Golem', 'Golem_01', 'Golem_02', 'Golem_03', 'Minotaur_01', 'Minotaur_02',
               'Minotaur_03', 'Goblin', 'Ogre', 'Orc']
enemy_health = [200, 150, 150, 150, 100, 100, 100, 25, 50, 75]
animation_types = ['Walking', 'Attacking', 'Dying']
sound = mixer.Sound('sounds/death.wav')
sound.set_volume(0.3)
sound1 = mixer.Sound('sounds/rock.wav')
sound1.set_volume(0.3)

for enemy in enemy_types:
    # load animation
    animation_list = []
    for animation in animation_types:
        temp_list = []
        initial_count = 0
        dir = f"images/mobs/{enemy}/{animation}"
        for path in os.listdir(dir):
            if os.path.isfile(os.path.join(dir, path)):
                initial_count += 1
        frames = ['00' + str(i) if i < 10 else '0' + str(i) for i in range(initial_count)]
        for i in frames:
            try:
                img = pygame.image.load(f'images/mobs/{enemy}/{animation}/{enemy}_{animation}_{i}.png').convert_alpha()
            except FileNotFoundError:
                try:
                    img = pygame.image.load(
                        f'images/mobs/{enemy}/{animation}/0_{enemy}_{animation}_{i}.png').convert_alpha()
                except FileNotFoundError:
                    img = pygame.image.load(
                        f'images/mobs/{enemy}/{animation}/0_{enemy}_Slashing_{i}.png').convert_alpha()

            e_w = img.get_width()
            e_h = img.get_height()
            if enemy in ['Goblin', 'Ogre', 'Orc']:
                w, h = int(e_w * 0.093), int(e_h * 0.097)
            elif enemy in ['Minotaur_01', 'Minotaur_02',
               'Minotaur_03']:
                w, h = int(e_w * 0.145), int(e_h * 0.145)
            elif enemy in ['Golem']:
                w, h = int(e_w * 0.12), int(e_h * 0.12)
            else:
                w, h = int(e_w * 0.17), int(e_h * 0.17)
            img = pygame.transform.scale(img, (w, h))
            temp_list.append(img)
        animation_list.append([temp_list, frames])
    enemy_animations.append(animation_list)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, health, animation_list, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed
        self.full_health, self.health = health, health

        self.golem = False
        self.goblins = False
        self.minotavrs = False
        if self.health == enemy_health[0]:
            self.golem = True
        if self.health in enemy_health[7:10]:
            self.goblins = True
        if self.health in enemy_health[4:7]:
            self.minotavrs = True


        self.last_attack = pygame.time.get_ticks()
        self.attack_cooldown = 1000
        self.animation_list = animation_list
        self.indexes_frame = [animation_list[i][1] for i in range(len(animation_list))]
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.uupdate = True

        # select starting image
        self.image = self.animation_list[self.action][0][
            self.indexes_frame[self.action].index(self.indexes_frame[self.action][self.frame_index])]
        #print(self.image)
        self.rect = pygame.Rect(0, 0, 22, 50)
        self.rect.center = (x, y)

    def update(self, surface, target, bullets, freeze=False):
        if target.health < 10:
            self.update_action(0)

        if freeze:
            self.action = 0
            self.frame_index = 0
            self.alive = False
            self.uupdate = False

        if self.alive:
            # collision with bullets
            if pygame.sprite.spritecollide(self, bullets, True):
                self.health -= 25

            # collision with castle
            if self.rect.right > target.rect.left:
                self.update_action(1)

            # move
            if self.action == 0:
                self.rect.x += self.speed

            # attack
            if self.action == 1:
                if pygame.time.get_ticks() - self.last_attack > self.attack_cooldown:
                    sound1.play()
                    target.health -= 25
                    if target.health <= 0:
                        target.health = 0
                    #print(target.health)
                    self.last_attack = pygame.time.get_ticks()

            # check if health = 0
            if self.health <= 0:
                target.money += int(self.full_health)
                target.score += int(self.full_health)
                self.update_action(2) # death
                sound.play()
                self.alive = False
                #print(target.money)

        if self.uupdate:
            self.update_animation()

        # draw image on the screen
        #pygame.draw.rect(surface, (255, 255, 255), self.rect, 1)

        if self.golem:
            surface.blit(self.image, (self.rect.x - 47, self.rect.y - 34))
        elif self.goblins:
            surface.blit(self.image, (self.rect.x - 30, self.rect.y - 23))
        elif self.minotavrs:
            surface.blit(self.image, (self.rect.x - 45, self.rect.y - 17))
        else:
            surface.blit(self.image, (self.rect.x - 51, self.rect.y - 23))

    def update_animation(self):
        # define animation cooldown
        ANIMATION_COOLDOWN = 50
        # update image depending on current action
        self.image = self.animation_list[self.action][0][
            self.indexes_frame[self.action].index(self.indexes_frame[self.action][self.frame_index])]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.indexes_frame[self.action]):
            if self.action == 2:
                self.frame_index = len(self.indexes_frame[self.action])-1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        if self.action != new_action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
