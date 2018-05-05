# coding=ISO-8859-1
import pygame
import random
import math

#A Vaca (coitada)
class Cow(pygame.sprite.Sprite):
    def __init__(self,posx):
        super(Cow,self).__init__()
        self.posx=posx
        self.posy=380
        self.direction=''

        self.animation_idle=[]
        self.animation_idle_tied=[]
        self.animation_tied_abducting=[]
        self.animation_abducting=[]

        self.rope_resist=3
        self.status='Normal'
        self.search='Free'
        self.now_animated=0
        self.last_animated=0
        self.last=0
        self.now=0
        self.cooldown = 3000
        self.frame =0

        sprite_sheet = SpriteCut('images/cow.png')
        for x in xrange(6):
            image = sprite_sheet.image_cut((x * 128)+256, 128, 128, 128)
            self.animation_idle.append(image)

        for x in xrange(6):
            image = sprite_sheet.image_cut(x * 128, 384, 128, 128)
            self.animation_idle_tied.append(image)

        for x in xrange(4):
            image = sprite_sheet.image_cut((x * 128) + 384, 512, 128, 128)
            self.animation_tied_abducting.append(image)

        for x in xrange(2):
            image=sprite_sheet.image_cut((x*128)+1024,512,128,128)
            self.animation_abducting.append(image)

        self.image = self.animation_idle[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.posx
        self.rect.y = self.posy
        self.last_animated=pygame.time.get_ticks()


#Chama qdo for abduzida
    def being_abduction(self):
        self.last=pygame.time.get_ticks()
        if self.status == 'Normal':
            self.posy=30
            self.status='Abducting'
            self.direction='A'
            self.frame=0
        elif self.status=='TiedUp' and self.rope_resist==0:
            self.posy=30
            self.status='Abducting'
            self.status='A'
            self.frame=0
        elif self.status=='TiedUp' and self.rope_resist>0:
            self.posy=310
            self.status='AbductingTied'
            self.direction='AT'
            self.frame=0
        elif self.status=='AbductingTied' and self.rope_resist==0:
            self.posy=30
            self.status='Abducting'
            self.direction='A'
            self.frame=0
        elif self.status=='WFD' and self.rope_resist==0:
            self.posy=30
            self.status='Abducting'
            self.direction='A'
            self.frame=0
        self.rope_resist -= 1
        pass

#Chama a cada frame para movimentacao (se ainda vai ver mto disso la pra baixo)
    def update(self):
        if self.status=='Normal':
            self.now_animated=pygame.time.get_ticks()
            if self.now_animated - self.last_animated >= 300 and self.frame <6:
                self.image=self.animation_idle[self.frame]
                self.frame+=1
                self.last_animated=pygame.time.get_ticks()
            elif self.frame==6:
                self.frame=0
                self.last_animated=pygame.time.get_ticks()
        elif self.status=='TiedUp':
            self.now_animated = pygame.time.get_ticks()
            if self.now_animated - self.last_animated >= 200 and self.frame < 5:
                self.image = self.animation_idle_tied[self.frame]
                self.frame += 1
                self.last_animated = pygame.time.get_ticks()
            elif self.frame==5:
                self.frame = 0
                self.last_animated = pygame.time.get_ticks()
        elif self.status=='AbductingTied':
            if self.rect.y > self.posy:
                self.rect.y-=2
            elif self.rect.y==self.posy:
                self.status = 'WFD'
                self.now = pygame.time.get_ticks()
                if self.now - self.last >= self.cooldown:
                    self.being_abduction()
        elif self.status=='WFD':
            self.now = pygame.time.get_ticks()
            if self.now - self.last >= self.cooldown:
                self.being_abduction()
        elif self.status=='Abducting':
            if self.rect.y>self.posy:
                self.rect.y-=4
            else:
                self.status='Dead'
        elif self.status=='Dead':
            pass
        if self.direction=='AT':
            self.now_animated = pygame.time.get_ticks()
            if self.now_animated - self.last_animated >= 200 and self.frame < 3:
                self.image = self.animation_tied_abducting[self.frame]
                self.frame += 1
                self.last_animated = pygame.time.get_ticks()
            elif self.frame == 3:
                self.frame = 0
                self.last_animated = pygame.time.get_ticks()
        elif self.direction=='A':
            self.now_animated = pygame.time.get_ticks()
            if self.now_animated - self.last_animated >= 200 and self.frame < 1:
                self.image = self.animation_abducting[self.frame]
                self.frame += 1
                self.last_animated = pygame.time.get_ticks()
            elif self.frame == 1:
                self.image= self.animation_abducting[self.frame]
                self.frame=0
                self.last_animated = pygame.time.get_ticks()
                self.direction='D'


        pass

#Os "Aliens"
class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super(Ship, self).__init__()
        dice = random.randint(1, 2)
        self.posx = ''
        if dice == 1:
            self.posx = -200
            self.direction='R'
        else:
            self.posx = 1300
            self.direction='L'
        self.posy=50

        self.animation_frames_left = []
        self.animation_frames_right = []
        self.animation_abduction = []
        self.animation_dead_cow=[]
        self.now_push = 0
        self.last_push = 0
        self.now_animate = 0
        self.last_animate = 0
        self.frames = 0
        self.frames_abducting=0
        self.now_abducting=0
        self.last_abducting=0

        sprite_sheet = SpriteCut('images/ship.png')
        sprite_sheet2 = SpriteCut('images/ship2.png')


        for x in xrange(4):
            image = sprite_sheet2.image_cut((x * 128)+640, 640, 128, 160)
            self.animation_dead_cow.append(image)


        image=sprite_sheet.image_cut(1280,0,128,160)
        self.animation_frames_right.append(image)
        for x in xrange(7):
            image = sprite_sheet.image_cut(x * 128, 160, 128, 160)
            self.animation_frames_right.append(image)


        image = sprite_sheet.image_cut(1280, 0, 128, 160)
        image = pygame.transform.flip(image,True,False)
        self.animation_frames_left.append(image)
        for x in range(7):
            image = sprite_sheet.image_cut(x * 128, 160, 128, 160)
            image = pygame.transform.flip(image,True,False)
            self.animation_frames_left.append(image)

        for x in range(7):
            image= sprite_sheet.image_cut((x*128)+384,480,128,160)
            self.animation_abduction.append(image)






        # self.image=pygame.Surface([50,20]).convert()
        # self.image.fill((255,255,0))
        # self.rect=self.image.get_rect()



        self.image = self.animation_frames_right[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.posx
        self.rect.y = self.posy

        self.target=Cow(0)
        self.status='Normal'
        self.speed=1


#Procura uma vaca sozinha para ser sua presa
    def search_cow(self,list_cow):
        if self.status=='Normal':
            for x in xrange(0,len(list_cow)):
                y=random.randint(0,(len(list_cow))-1)
                if list_cow[y].search=='Free':
                    self.target=list_cow[y]
                    list_cow[y].search='NotFree'
                    self.status='GetingCow'
                    if self.rect.x < self.target.rect.x:
                        self.direction='R'
                        self.frames=0
                    elif self.rect.x > self.target.rect.x:
                        self.direction='L'
                        self.frames=0
                    break
        pass

#Chamada a cada frame para realizar as tarefas e animacao
    def update(self):
        if self.status=='Normal':
            #IdleAnimation
            pass
        elif self.status=='GetingCow':
            if self.rect.x+30 < self.target.rect.x-20:
                self.rect.x+=self.speed
            elif self.rect.x+30 < self.target.rect.x+10:
                self.rect.x+=1
                self.direction='-R'
            elif self.rect.x+30 > self.target.rect.x+40:
                self.rect.x-=self.speed
            elif self.rect.x+30 > self.target.rect.x+10:
                self.rect.x-=1
                self.direction='-L'
            elif self.rect.x+30 == self.target.rect.x+10 and self.status=='GetingCow':
                self.status='Abductin'
                self.target.being_abduction()
                self.direction='A'
                self.last_abducting=pygame.time.get_ticks()
        elif self.status=='Abductin':
            if self.target.search=='Free':
                self.get_away()
        elif self.status=='GetingAway':
            if self.rect.x > self.posx:
                self.rect.x-=self.speed
            elif self.rect.x < self.posx:
                self.rect.x+=self.speed
            elif self.rect.x < 0 or self.rect.x >1024:
                self.status='Normal'
        if self.direction=='R':
            self.now_push=pygame.time.get_ticks()
            if self.now_push - self.last_push >= 100 and self.frames < 7:
                self.image=self.animation_frames_right[self.frames]
                self.frames+=1
                self.last_push=pygame.time.get_ticks()
            elif self.frames==7:
                self.direction = 'S'
        elif self.direction == 'L':
            self.now_push = pygame.time.get_ticks()
            if self.now_push - self.last_push >= 100 and self.frames < 7:
                self.image = self.animation_frames_left[self.frames]
                self.frames += 1
                self.last_push = pygame.time.get_ticks()
            elif self.frames == 7:
                self.direction = 'S'
        elif self.direction == '-R':
            self.now_push = pygame.time.get_ticks()
            if self.now_push - self.last_push >= 100 and self.frames > 0:
                self.image = self.animation_frames_right[self.frames]
                self.frames -= 1
                self.last_push = pygame.time.get_ticks()
            elif self.frames == 0:
                self.direction = 'S'
                self.image = self.animation_frames_left[self.frames]
        elif self.direction == '-L':
            self.now_push = pygame.time.get_ticks()
            if self.now_push - self.last_push >= 100 and self.frames > 0:
                self.image = self.animation_frames_left[self.frames]
                self.frames -= 1
                self.last_push = pygame.time.get_ticks()
            elif self.frames == 0:
                self.direction = 'S'
                self.image = self.animation_frames_left[self.frames]
        elif self.direction =='A':
            self.now_abducting=pygame.time.get_ticks()
            if self.now_abducting - self.last_abducting >= 100 and self.frames_abducting<6:
                self.image=self.animation_abduction[self.frames_abducting]
                self.frames_abducting+=1
                self.last_abducting=pygame.time.get_ticks()
            elif self.frames_abducting==6:
                self.frames_abducting=0
                self.last_abducting=pygame.time.get_ticks()
        # elif self.direction=='D':
        #     self.now_animate = pygame.time.get_ticks()
        #     if self.now_animate - self.last_animate >= 150 and self.frames_abducting < 3:
        #         self.image = self.animation_dead_cow[self.frames_abducting]
        #         self.frames_abducting += 1
        #         self.last_animate = pygame.time.get_ticks()
        #         print 1
        #     elif self.frames_abducting == 3:
        #         self.image = self.animation_dead_cow[self.frames_abducting]
        #         self.frames_abducting = 0
        #         self.get_away()
        #         print 2
            pass


        pass

    def get_away(self):

        dice=random.randint(1,2)
        if dice==1:
            self.posx=-200
            self.direction='L'
            self.frames=0
        else:
            self.posx=1300
            self.direction='R'
            self.frames=0
        self.status = 'GetingAway'

        pass

#O Fazendeiro
class Farmer(pygame.sprite.Sprite):
    def __init__(self,file_name,sound):
        super(Farmer,self).__init__()
        self.posx=550
        self.posy=395
        self.move_x=0
        self.left=False
        self.right=False

        self.animation_frames_left = []
        self.animation_frames_right = []
        self.animation_frames_tied=[]
        self.animation_frames_push=[]
        self.now_push=0
        self.last_push=0
        self.frames=0
        self.tied_sound=sound.Sound('sound/tiedcow.wav')
        self.walk_sound=sound.Sound('sound/walk.wav')
        self.push_sound=sound.Sound('sound/push.wav')
        self.player= pygame.mixer.Channel(5)
        self.push_channel= pygame.mixer.Channel(6)


        # self.image=pygame.Surface([20,20]).convert()
        # self.image.fill((0,255,255))
        # self.rect=self.image.get_rect()

        sprite_sheet = SpriteCut(file_name)


        for x in xrange(13):
            image = sprite_sheet.image_cut(x*64, 0, 64, 80)
            self.animation_frames_left.append(image)

        for x in xrange(13):
            image = sprite_sheet.image_cut(x*64, 80, 64, 80)
            self.animation_frames_right.append(image)

        for x in xrange(9):
            image = sprite_sheet.image_cut(x*64, 160, 64, 80)
            self.animation_frames_tied.append(image)

        image = sprite_sheet.image_cut(640, 160, 64, 80)
        self.animation_frames_push.append(image)
        image = sprite_sheet.image_cut(704, 160, 64, 80)
        self.animation_frames_push.append(image)
        image = sprite_sheet.image_cut(768, 160, 64, 80)
        self.animation_frames_push.append(image)
        image = sprite_sheet.image_cut(832, 160, 64, 80)
        self.animation_frames_push.append(image)


        for x in xrange(10):
            image = sprite_sheet.image_cut(x*64, 160, 64, 80)
            self.animation_frames_tied.append(image)



        self.direction = 'R'
        self.image = self.animation_frames_right[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.posx
        self.rect.y = self.posy

    #Amarra a vaquinha
    def tied(self,target):
        self.stop_move()
        channel=self.tied_sound.play(0,0,0)
        if target.rope_resist < 3:
            target.rope_resist+=1
        self.direction='T'
        target.status='TiedUp'
        pass
#Puxa a vaquinha
    def push(self,target):
        self.stop_move()
        self.push_channel=self.push_sound.play(0,350,0)
        self.direction='P'
        if target.rect.y < self.posy - 20:
            target.rect.y+=10
        else:
            target.status='TiedUp'
            target.search='Free'
        pass
#MOVIMENTOGERAL
    def move_left(self):
        if self.direction!='T' and self.direction!='P':
            self.move_x=-3
            self.direction = 'L'
            if not self.player.get_busy():
                self.player=self.walk_sound.play(0,0,0)

        pass

    def move_right(self):
        if self.direction != 'T' and self.direction != 'P':
            self.move_x=3
            self.direction = 'R'
            if not self.player.get_busy():
                self.player=self.walk_sound.play(0,0,0)

        pass

    def stop_move(self):
        self.move_x=0
        pass

#Chamado a cada frame para movimentacao e animacao
    def update(self):
        if self.left is True and self.right is False:
            self.move_left()

        elif self.left is False and self.right is True:
            self.move_right()

        elif self.left is False and self.right is False:
            self.stop_move()

        self.posx += self.move_x
        self.rect.x = self.posx
        x_position = self.rect.x
        if self.direction == 'R':
            frame = (x_position // 15) % len(self.animation_frames_right)
            self.image = self.animation_frames_right[frame]
        elif self.direction == 'L':
            frame = (-x_position // 15) % len(self.animation_frames_left)
            self.image = self.animation_frames_left[frame]
        elif self.direction=='P':
            self.now_push=pygame.time.get_ticks()
            if self.now_push - self.last_push >= 40 and self.frames < 3:
                self.image=self.animation_frames_push[self.frames]
                self.frames+=1
                self.last_push=pygame.time.get_ticks()
            elif self.frames==3:
                self.frames=0
                self.direction='R'
        elif self.direction=='T':
            self.now_push=pygame.time.get_ticks()
            if self.now_push - self.last_push >= 150 and self.frames < 8:
                self.image=self.animation_frames_tied[self.frames]
                self.frames+=1
                self.last_push=pygame.time.get_ticks()
            elif self.frames==8:
                self.frames=0
                self.direction='R'


        pass

#Mapa Sera responsavel pelo aumento de nivel procedural
class Map:

    def __init__(self,sound):
        self.num_level=1
        self.list_pos=[50,200,350,500,650]
        self.num_cow=5
        self.min_ship=2
        self.max_ship=5
        self.num_ship=2
        self.cow_list=pygame.sprite.Group()
        self.draw_sprites=pygame.sprite.Group()
        self.ship_list=pygame.sprite.Group()
        self.obj_cow_list=[]
        self.obj_ship_list=[]
        self.start_cooldown=8000
        self.spawn_cd=6000
        self.cooldown_level=40000
        self.cd_trans=3000
        self.last=0
        self.free_cow_status=False
        self.now=0
        self.last_level=0
        self.now_level=0
        self.last_trans=0
        self.now_trans=0
        self.status='Inicio'
        self.myfont=pygame.font.SysFont("monospace",35)
        self.texto1=pygame.font.SysFont("impact",72)
        self.texto2=pygame.font.SysFont("impact",50)
        self.texto3=pygame.font.SysFont("impact",35)
        self.texto4=pygame.font.SysFont("impact",18)
        self.fps=pygame.time.Clock()
        self.screen=pygame.display.set_mode((1024,768),pygame.FULLSCREEN,32)
        self.speed=1
        self.bg_song=sound.Sound('sound/bg.wav')
        self.bg_menu=sound.Sound('sound/intro.wav')
        self.bg_menu.set_volume(0.1)
        self.bg_song.set_volume(0.5)
        self.bg_channel=pygame.mixer.Channel(1)
        self.background = pygame.image.load('images/main_menu.png').convert()
        self.background_level = pygame.image.load('images/bg_level.png').convert()
        pygame.mixer.set_reserved(4)

    def level_start(self):

        self.num_ship = 2
        self.last=pygame.time.get_ticks()
        texto=self.myfont.render('Level ' + str(self.num_level),1,(255,255,255))
        while self.now - self.last <= self.cd_trans:
            self.screen.fill((0,0,0))
            self.now=pygame.time.get_ticks()
            self.screen.blit(texto, (512-20, 384))
            pygame.display.flip()
            self.fps.tick(60)

        pos = random.randint(0, 4)
        for x in xrange(5):  # numCow
            vaca = Cow(self.list_pos[pos])
            if pos == 4:
                pos = 0
            else:
                pos += 1
            self.cow_list.add(vaca)
            self.obj_cow_list.append(vaca)
            self.num_cow-=1

        for x in xrange(self.num_ship):
            nave=Ship()
            self.ship_list.add(nave)
            self.obj_ship_list.append(nave)
            nave.speed=self.speed

        pass
        self.last=pygame.time.get_ticks()
        self.last_level=pygame.time.get_ticks()
        self.status='Inicio'

    def new_level(self):
        if not self.bg_channel.get_busy():
            self.bg_channel=self.bg_song.play(1,0,10000)
        self.speed=int(math.floor(self.num_level / 5))+1
        self.last_trans=pygame.time.get_ticks()
        texto = self.myfont.render('Level ' + str(self.num_level), 0, (255, 255, 255))
        while self.now_trans - self.last_trans <= self.cd_trans:
            self.screen.fill((0, 0, 0))
            self.now_trans = pygame.time.get_ticks()
            self.screen.blit(texto, (512-texto.get_width()/2,384-texto.get_height()/2))
            pygame.display.flip()

        for vaca in self.cow_list:
            self.cow_list.remove(vaca)
            self.obj_cow_list.remove(vaca)
            self.num_cow+=1

        for ship in self.ship_list:
            self.ship_list.remove(ship)
            self.obj_ship_list.remove(ship)


        if self.num_ship < self.max_ship:
            self.num_ship=int(self.min_ship+(math.floor(self.num_level/5)))
        else:
            self.num_ship=5


        for nave in xrange(self.num_ship):
            nave = Ship()
            self.draw_sprites.add(nave)
            self.ship_list.add(nave)
            self.obj_ship_list.append(nave)
            nave.speed = self.speed

        if self.num_cow >=5:
            pos = random.randint(0, 4)
            for x in xrange(5):
                vaca = Cow(self.list_pos[pos])
                if pos == 4:
                    pos = 0
                else:
                    pos += 1
                self.cow_list.add(vaca)
                self.obj_cow_list.append(vaca)
                self.num_cow-=1
        elif self.num_cow >0:
            pos = random.randint(0, 4)
            for x in xrange(self.num_cow):
                vaca = Cow(self.list_pos[pos])
                if pos == 4:
                    pos = 0
                else:
                    pos += 1
                self.cow_list.add(vaca)
                self.obj_cow_list.append(vaca)
                self.num_cow-=1


        self.last_level=pygame.time.get_ticks()
        self.last=pygame.time.get_ticks()
        self.status='Inicio'
        self.num_level += 1
        self.spawn_cd-=200
        self.free_cow_status = False


        pass

    def update(self):
        if not self.bg_channel.get_busy():
            self.bg_channel=self.bg_song.play(1,0,10000)
        self.draw_sprites.update()
        self.cow_list.update()
        self.ship_list.update()
        if self.status=='Inicio':
            self.now=pygame.time.get_ticks()
            if self.now - self.last >= self.start_cooldown:
                self.status='OnGame'
                self.obj_ship_list[random.randint(0,self.num_ship-1)].search_cow(self.obj_cow_list)
                self.last=pygame.time.get_ticks()
        if self.status=='OnGame':
            self.now=pygame.time.get_ticks()
            self.now_level=pygame.time.get_ticks()
            if self.now_level-self.last_level>=self.cooldown_level:
                self.status='FinishingLevel'
            if self.now - self.last >= self.spawn_cd:
                self.obj_ship_list[random.randint(0,self.num_ship-1)].search_cow(self.obj_cow_list)
                self.last=pygame.time.get_ticks()
        if self.status=='FinishingLevel':
            x=0
            for nave in self.obj_ship_list:
                if nave.status=='Normal':
                    x+=1
                else:
                    x-=1
                if x == len(self.obj_ship_list):
                    self.free_cow_status=True
                else:
                    self.free_cow_status=False

            if self.free_cow_status is True:
                self.last_level=pygame.time.get_ticks()
                self.new_level()
        pass

    def main_menu(self):
        self.bg_channel = self.bg_menu.play(1, 0, 2000)
        texto = self.texto1.render('Play', 0, (255, 255, 255))
        texto2 = self.texto2.render('Info',0,(255,255,255))
        texto4 = self.texto2.render('CREW',0,(255,255,255))
        texto5 = self.texto4.render("Programmers: Gabriel 'Sensei' Faggione / George 'Shisho' Dourado / Lucas 'Jesus' Moura",0,(0,0,0))
        texto6 = self.texto4.render("Arte Design: Matheus 'CJ' Freitas / Carlos 'Eduardo' Roberto ",0,(0,0,0))
        texto7 = self.texto4.render("Game and Sound Designer: Flávio 'Erro de NAT' Alves",0,(0,0,0))
        texto8 = self.texto1.render('BACK',0,(255,255,255))
        texto9 = self.texto3.render('Comandos Setas(LEFT/RIGHT)- Movimento',0,(255,255,255))
        texto10 = self.texto3.render('Comando Seta(UP)- Amarra Vaca', 0, (255, 255, 255))
        texto11 = self.texto3.render('Comando Seta(DOWN)- Puxa Vaca', 0, (255, 255, 255))
        texto12 = self.texto1.render('SPACE COW', 0, (255, 255, 255))

        show_text=0
        endmenu=False
        while endmenu==False:

            if not self.bg_channel.get_busy():
                self.bg_channel = self.bg_menu.play(1, 0, 2000)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                        m_pos=pygame.mouse.get_pos()
                        t1= pygame.Rect(470,200,texto.get_width(),texto.get_height())
                        t2= pygame.Rect(470,300,texto2.get_width(),texto2.get_height())
                        t3=pygame.Rect(800,500,texto8.get_width(),texto2.get_height())
                        if (t1.collidepoint(m_pos)) and show_text==0:
                            endmenu=True
                        elif (t2.collidepoint(m_pos)) and show_text==0:
                            show_text=1
                        elif (t3.collidepoint(m_pos)) and show_text==1:
                            show_text=0
                            pass


            self.screen.fill((0, 0, 0))
            self.screen.blit(self.background,(0,0))
            if show_text==0:
                self.screen.blit(texto12, (512 - (texto12.get_width() / 2), 50))
                self.screen.blit(texto, (512 - (texto.get_width() / 2), 200))
                self.screen.blit(texto2, (512 - (texto2.get_width() / 2), 300))
            elif show_text==1:
                self.screen.blit(texto4, (100 , 400))
                self.screen.blit(texto5, (100 , 500))
                self.screen.blit(texto6, (100 , 525))
                self.screen.blit(texto7, (100 , 550))
                self.screen.blit(texto8,(800,500))
                self.screen.blit(texto9, (400, 100))
                self.screen.blit(texto10, (400, 140))
                self.screen.blit(texto11, (400, 180))


                pass



            pygame.display.flip()
            self.fps.tick(60)
        self.bg_menu.stop()
        pass
    def pause_game(self):
        pass

class SpriteCut():
    def __init__(self,file_name):
        self.sprites=pygame.image.load(file_name).convert()

    def image_cut(self,x,y,width,height):
        image=pygame.Surface([width,height]).convert()
        image.blit(self.sprites,(0,0),(x,y,width,height))
        image.set_colorkey((0,0,0))
        return image

