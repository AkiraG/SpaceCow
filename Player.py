import pygame
from SpriteCut import SpriteCut
class Player(pygame.sprite.Sprite):
    def __init__(self,file_name):
        super(Player,self).__init__()
        self.move_x=0
        self.move_y=0
        self.animation_frames_left=[]
        self.animation_frames_right=[]
        self.animation_frames_upper=[]
        self.animation_frames_down=[]
        self.direction='R'
        self.right=False
        self.left=False
        self.up=False
        self.down=False

        sprites=SpriteCut(file_name)

        position=0
        for x in xrange(4):
            image = sprites.image_cut(position, 112, 56, 56)
            self.animation_frames_right.append(image)
            position+=56
        position=0
        for x in xrange(4):
            image = sprites.image_cut(position, 56, 56, 56)
            self.animation_frames_left.append(image)
            position+=56
        position=0
        for x in xrange(4):
            image = sprites.image_cut(position, 168, 56, 56)
            self.animation_frames_upper.append(image)
            position += 56
        position=0
        for x in xrange(4):
            image = sprites.image_cut(position, 0, 56, 56)
            self.animation_frames_down.append(image)
            position += 56

        self.image=self.animation_frames_right[0]
        self.rect=self.image.get_rect()

    def update(self):
        self.update_move()
        self.rect.x +=self.move_x
        self.rect.y +=self.move_y
        x_position=self.rect.x
        y_position=self.rect.y
        if self.direction=='R':
            frame=(x_position//20)%len(self.animation_frames_right)
            self.image=self.animation_frames_right[frame]
        elif self.direction=='L':
            frame=(x_position//20)%len(self.animation_frames_left)
            self.image=self.animation_frames_left[frame]
        elif self.direction=='U':
            frame=(y_position//20)%len(self.animation_frames_upper)
            self.image=self.animation_frames_upper[frame]
        elif self.direction=='D':
            frame=(y_position//20)%len(self.animation_frames_down)
            self.image=self.animation_frames_down[frame]

    def update_move(self):
        if self.down==True and self.up==False and self.right==False and self.left==False:
            self.move_down()
        if self.down==False and self.up==True and self.right==False and self.left==False:
            self.move_upper()
        if self.down ==False and self.up == False and self.right == True and self.left == False:
            self.move_right()
        if self.down==False and self.up==False and self.right==False and self.left==True:
            self.move_left()
        if self.down==False and self.up==False and self.right==False and self.left==False:
            self.stop_move()

    def move_left(self):
        self.move_x=-3
        self.move_y=0
        self.direction='L'

    def move_right(self):
        self.move_x=+3
        self.move_y=0
        self.direction='R'

    def move_upper(self):
        self.move_y=-3
        self.move_x=0
        self.direction='U'

    def move_down(self):
        self.move_y=+3
        self.move_x=0
        self.direction='D'

    def stop_move(self):
        self.move_x=0
        self.move_y=0

