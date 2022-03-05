import pygame
import castle
import button


# define font
font40 = pygame.font.SysFont('Futura', 35)
font70 = pygame.font.SysFont('Funta', 70)


def draw_text(screen, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def show_info(display, image1, image2, text_col, castle, score, level, w, h):
    display.blit(image1, (0, 10))
    draw_text(display, 'Money: ' + str(castle.money), font40, text_col, 10, 20)
    display.blit(image1, (230, 10))
    draw_text(display, 'Score: ' + str(castle.score), font40, text_col, 240, 20)
    display.blit(image1, (230, 50))
    draw_text(display, 'High Score: ' + str(score), font40, text_col, 240, 60)
    display.blit(image1, (460, 10))
    draw_text(display, 'Level: ' + str(level), font40, text_col, 470, 20)
    display.blit(image2, (w - 313, h - 70))
    draw_text(display, 'Health: ' + str(castle.health) + ' / ' + str(castle.max_health), font40, text_col, w - 300, h - 60)
    draw_text(display, '1000', font40, text_col, w - 315, 97)
    draw_text(display, '2500', font40, text_col, w - 213, 97)
    draw_text(display, '800', font40, text_col, w - 100, 97)
