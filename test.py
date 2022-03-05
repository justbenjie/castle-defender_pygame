import pygame
import random

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

bg1 = pygame.image.load('images/background/Снимок2.png').convert_alpha()
bg1 = pygame.transform.scale(bg1, (int(bg1.get_width()), int(bg1.get_height())))
display.blit(bg1, (0, 0))