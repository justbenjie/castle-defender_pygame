import pygame
import math
import bullet
from pygame import mixer

castles = {"castle100": "images/castle/good100.png", "castle50": "images/castle/good50.png",
           "castle25": "images/castle/good25.png"}
image = [pygame.image.load(castles["castle100"]).convert_alpha(),
          pygame.image.load(castles["castle50"]).convert_alpha(),
          pygame.image.load(castles["castle25"]).convert_alpha()]
bullet_sound = mixer.Sound('sounds/shoot.wav')
bullet_sound.set_volume(0.27)


class Castle:
    def __init__(self, display, image, x, y, scale=0.3):
        self.health = 1000
        self.display = display
        self.images = list(image)

        self.max_health = self.health
        self.fired = False
        self.money = 0
        self.score = 0

        self.last_shoot = pygame.time.get_ticks()
        self.cooldown = 400

        w = self.images[0].get_width()
        h = self.images[0].get_height()
        self.images[0] = pygame.transform.scale(self.images[0], (int(w * scale), int(h * scale)))
        self.images[1] = pygame.transform.scale(self.images[1], (int(w * scale), int(h * scale)))
        self.images[2] = pygame.transform.scale(self.images[2], (int(w * scale), int(h * scale)))
        self.rect = self.images[0].get_rect()
        self.rect.x = x
        self.rect.y = y

    def shoot(self, bullet_group):
        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - self.rect.midleft[0]
        y_dist = pos[1] - self.rect.midleft[1]
        self.angle = math.atan2(y_dist, x_dist)

        # print(math.degrees(self.angle))
        if pygame.mouse.get_pressed()[0] and not self.fired and pygame.time.get_ticks() - self.last_shoot > self.cooldown and pos[1] > 100:
            bullet_sound.play()
            self.last_shoot = pygame.time.get_ticks()
            self.fired = True
            #print(pos, " ", self.angle)
            arrow = bullet.Bullet(self.rect.midleft[0], self.rect.midleft[1] - 10, self.angle)
            bullet_group.add(arrow)
            #print("line", self.rect.midleft[1])
        #pygame.draw.line(self.display, (255, 255, 255), (self.rect.midleft[0], self.rect.midleft[1]), pos)

        if not pygame.mouse.get_pressed(3)[0]:
            self.fired = False

    def draw(self):
        if self.health <= 250:
            self.current_image = self.images[2]
        elif self.health <= 500:
            self.current_image = self.images[1]
        else:
            self.current_image = self.images[0]

        #pygame.draw.rect(self.display, (255, 255, 255), self.rect, 1)
        self.display.blit(self.current_image, self.rect)

    def repair(self):
        if self.money >= 1000 and self.health < self.max_health:
            self.health += 500
            self.money -= 1000
            if self.health > self.max_health:
                self.health = self.max_health

    def armour(self):
        if self.money >= 800:
            self.max_health += 500
            self.money -= 800
            if self.health > self.max_health:
                self.health = self.max_health

    towers = {"tower100": "images/castle/tower100.png", "tower50": "images/castle/tower50.png",
               "tower25": "images/castle/tower25.png"}
    images_tower = [pygame.image.load(towers["tower100"]).convert_alpha(),
              pygame.image.load(towers["tower50"]).convert_alpha(),
              pygame.image.load(towers["tower25"]).convert_alpha()]


class Tower(pygame.sprite.Sprite, Castle):
    def __init__(self, display, images, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        Castle.__init__(self,  display, images, x, y, scale)
        self.image = self.images[0]
        self.got_target = False
        self.angle = 0
        self.last_shot = pygame.time.get_ticks()

    def set_health(self, health):
        self.health = health

    def update(self, enemy_group, bullet_group, health):
        self.health = health
        self.got_target = False
        target_x = 0
        target_y = 0
        for e in enemy_group:
            if e.alive:
                target_x, target_y = e.rect.midbottom
                self.got_target = True
                break

        if self.got_target:
            #pygame.draw.line(self.display, (255, 255, 255), (self.rect.center[0], self.rect.center[1]),
                             #(target_x, target_y-30))
            x_dist = target_x - self.rect.center[0]
            y_dist = (target_y-30) - self.rect.center[1]
            self.angle = math.atan2(y_dist, x_dist)

            shot_cooldown = 1500
            if pygame.time.get_ticks() - self.last_shot > shot_cooldown:
                bullet_sound.play()
                self.last_shot = pygame.time.get_ticks()
                arrow = bullet.Bullet(self.rect.center[0], self.rect.center[1], self.angle)
                bullet_group.add(arrow)

        self.draw()







