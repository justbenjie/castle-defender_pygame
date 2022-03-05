import pygame


class Crosshair:
    def __init__(self):
        image1 = pygame.image.load('images/crosshair/crosshair-removebg-preview.png').convert_alpha()
        image2 = pygame.image.load('images/crosshair/hand.png').convert_alpha()
        self.width1 = image1.get_width()
        self.height1 = image1.get_height()
        self.width2 = image2.get_width()
        self.height2 = image2.get_height()

        self.image1 = pygame.transform.scale(image1, (int(self.width1*0.05), int(self.height1*0.05)))
        self.image2 = pygame.transform.scale(image2, (int(self.width2*0.4), int(self.height2 * 0.4)))
        self.rect1 = self.image1.get_rect()
        self.rect2 = self.image2.get_rect()

        # hide mouse
        pygame.mouse.set_visible(False)

    def draw(self, display, draw=False):

        mx, my = pygame.mouse.get_pos()
        if draw:
            self.rect2.center = (mx + 8, my + 8)
            display.blit(self.image2, self.rect2)
        else:
            if my < 100:
                self.rect2.center = (mx+8, my+8)
                display.blit(self.image2, self.rect2)
            else:
                self.rect1.center = (mx, my)
                display.blit(self.image1, self.rect1)

    def __del__(self):
        pass
