# coding=ISO-8859-1
import pygame
from Player import Player


sounds=pygame.mixer
sounds.init()
def wait_play(channel):
    while channel.get_busy():
        pass
s=sounds.Sound('C:/Users/saita/Desktop/SMAUG/sound/bg.wav')
pygame.init()
fps=pygame.time.Clock()
myfont=pygame.font.SysFont("monospace",15)


main_screen=pygame.display.set_mode([1280,720],0,32)
pygame.display.set_caption('SMAUG')
active_sprites=pygame.sprite.Group()


#bg = pygame.image.load('image/Arena01.png').convert()

player_1=Player('image/sprite_walk.png')
player_1.rect.x=300
player_1.rect.y=300

active_sprites.add(player_1)
texto = myfont.render(str(fps.get_fps()), 1, (0, 0, 0))
end_game=False
s.set_volume(0.1)
channel=s.play(0,0,10000)
pygame.mouse.set_visible(0)
fps=pygame.time.Clock()

while not end_game:
   # if not channel.get_busy():
    #    s.play(0,0,0)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end_game=True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                end_game=True
            if event.key == pygame.K_RIGHT:
                player_1.right=True
            if event.key == pygame.K_LEFT:
                player_1.left=True
            if event.key == pygame.K_UP:
                player_1.up=True
            if event.key == pygame.K_DOWN:
                player_1.down=True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                player_1.right=False
            if event.key == pygame.K_LEFT:
                player_1.left=False
            if event.key == pygame.K_UP:
                player_1.up=False
            if event.key == pygame.K_DOWN:
                player_1.down=False



    active_sprites.update()
    main_screen.fill((255,255,255))
    main_screen.blit(bg,(0,0))
    main_screen.blit(texto,(25,50))
    active_sprites.draw(main_screen)
    fps.tick(60)
    texto = myfont.render('FPS:%s'%str(fps.get_fps()), 1, (0, 0, 0))
    pygame.display.flip()
pygame.quit()
