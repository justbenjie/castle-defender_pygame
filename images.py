import pygame


def process_images():
    # load images
    bad_castle_img = pygame.image.load('images/castle/bad100.png').convert_alpha()
    bad_castle_img = pygame.transform.scale(bad_castle_img,
                                            (int(bad_castle_img.get_width() * 0.3), int(bad_castle_img.get_height() * 0.3)))

    bg = pygame.image.load('images/background/73f87c30a1e1eb2df631a06bccee5787.png').convert_alpha()
    bg = pygame.transform.scale(bg, (int(bg.get_width()), int(bg.get_height())))
    bg1 = pygame.image.load('images/background/96f629d415d85e376ba2e0c39001f424.png').convert_alpha()

    backgr = pygame.image.load('images/GUI/background-removebg-preview.png').convert_alpha()
    backgr1 = pygame.transform.scale(backgr, (int(backgr.get_width() * 0.2), int(backgr.get_height() * 0.195)))
    backgr2 = pygame.transform.scale(backgr, (int(backgr.get_width() * 0.28), int(backgr.get_height() * 0.195)))
    button1 = pygame.image.load('images/GUI/background1.png').convert_alpha()
    button2 = pygame.image.load('images/GUI/background2.png').convert_alpha()
    button3 = pygame.image.load('images/GUI/background3.png').convert_alpha()
    button4 = pygame.image.load('images/GUI/background4.png').convert_alpha()

    tower100 = pygame.image.load('images/castle/tower1001.png').convert_alpha()

    # button images
    repair_img = pygame.image.load('images/GUI/hummer.png')
    armour_img = pygame.image.load('images/GUI/shield.png')
    return bad_castle_img, bg, bg1, backgr, backgr1, backgr2, button1, button2, button3, button4, tower100, repair_img, armour_img