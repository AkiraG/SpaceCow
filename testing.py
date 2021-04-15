import pygame
from game_classes import Farmer, Cow, Ship

COLOR_BLACK = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((1024, 768), 0, 32)
fps = pygame.time.Clock()
mixer = pygame.mixer
mixer.init()
farmer = Farmer('images/caipira.png', position_x=550, position_y=395, mixer=mixer)
draw = pygame.sprite.Group()
draw.add(farmer)
endgame = False

while not endgame:
    for event in pygame.event.get([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP], pump=True):
        print(event)
        if event.type == pygame.QUIT:
            endgame = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                endgame = True
            if event.key == pygame.K_LEFT:
                farmer.movement['left'] = True
            if event.key == pygame.K_RIGHT:
                farmer.movement['right'] = True
            if event.key == pygame.K_UP:
                farmer.rescue_cow(0)
            if event.key == pygame.K_DOWN:
                farmer.tie_cow(0)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                farmer.movement['left'] = False
            if event.key == pygame.K_RIGHT:
                farmer.movement['right'] = False

    screen.fill(COLOR_BLACK)
    farmer.update()
    draw.draw(screen)
    fps.tick(60)
    pygame.display.flip()
