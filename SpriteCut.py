import pygame

class SpriteCut():
    def __init__(self,file_name):
        self.sprites=pygame.image.load(file_name).convert()

    def image_cut(self,x,y,width,height):
        image=pygame.Surface([width,height]).convert()
        image.blit(self.sprites,(0,0),(x,y,width,height))
        image.set_colorkey((0,0,0))
        return image
