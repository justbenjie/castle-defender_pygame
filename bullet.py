import pygame
import math


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/bullet/Cannonball.png').convert_alpha()
        w = self.image.get_width()
        h = self.image.get_height()
        self.image = pygame.transform.scale(self.image, (int(w * 0.04), int(h * 0.04)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        #print(y)
        self.angle = angle
        self.speed = 13
        # calculate speed
        self.dx = math.cos(self.angle) * self.speed
        self.dy = math.sin(self.angle) * self.speed
        self.x = x
        self.y = y

    def update(self, surface, w, h):
        # if check if bullet has gone off the screeen
        if self.rect.right < 0 or self.rect.left > w or self.rect.bottom < 0 or self.rect.top > h:
            self.kill()
        self.x += self.dx
        self.y += self.dy
        self.rect.x = self.x
        self.rect.y = self.y
        #pygame.draw.rect(surface, (255, 255, 255), self.rect, 1)
