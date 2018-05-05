'''

Feito para GAME JAM FATEC CARAPICUIBA - CARACAS GEEK FEST
Programmers: George 'Shisho' Dourado , Gabriel 'Sensei' Faggione , Moura 'Senshi' Jesus
Arte Designer: Matheus 'CJ' Freitas, Carlos 'Eduardo' Augusto
Sound Designer: Flavio 'Brinde pras gordinhas, pras magrinhas e pras boqueteiras' Alves
Game Designer: Flavio 'Sim ele denovo' Alves

'''

#ImportThings
import pygame
from CLASSES import Farmer,Map

#INIT Screen and FPS
pygame.init()
sounds=pygame.mixer
sounds.init()
myfont=pygame.font.SysFont("monospace",35)
pygame.display.set_caption('SPACECOW')

#Variables
endgame=False
white=(255,255,255)
black=(0,0,0)


#InstantiateClasses(TESTE)
mapa = Map(sounds)
farmer=Farmer('images/caipira.png',sounds)
mapa.draw_sprites.add(farmer)
mapa.main_menu()
mapa.new_level()

#UpdateLoop
while endgame==False:

    #Event Get
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            endgame=True
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                endgame=True
            if event.key==pygame.K_LEFT:
                farmer.left=True
            if event.key==pygame.K_RIGHT:
                farmer.right=True
            if event.key==pygame.K_UP:
                cow_collide=pygame.sprite.spritecollide(farmer,mapa.cow_list,False)
                for vaca in mapa.obj_cow_list:
                    if (farmer.posx+10>=vaca.posx-10 and farmer.posx+10<=vaca.posx+30) and vaca.status=='TiedUp' and vaca.rope_resist<3:
                        farmer.tied(vaca)


                for vaca in cow_collide:
                    if vaca.status=='Normal':
                        farmer.tied(vaca)
            if event.key==pygame.K_DOWN:
                for vaca in mapa.cow_list:
                    if (farmer.posx+10>=vaca.posx-10 and farmer.posx+10<=vaca.posx+30) and vaca.status=='WFD':
                        farmer.push(vaca)
                pass
            if event.key==pygame.K_SPACE:
                for x in xrange(mapa.num_ship):
                    mapa.obj_ship_list[x].search_cow(mapa.obj_cow_list)
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT:
                farmer.left=False
            if event.key==pygame.K_RIGHT:
                farmer.right=False


    #FillScreenwhitecolor
    mapa.screen.fill(black)


    #DrawSprites na tela principal
    mapa.screen.blit(mapa.background_level,(0,0))
    mapa.cow_list.draw(mapa.screen)
    mapa.ship_list.draw(mapa.screen)
    mapa.draw_sprites.draw(mapa.screen)

    #CallUpdateFunctionsofSprites(TESTE)
    mapa.update()
    for x in xrange(mapa.num_ship):
        cow_collide=pygame.sprite.spritecollide(mapa.obj_ship_list[x-1],mapa.cow_list,False)
        for vaca in cow_collide:
            if mapa.obj_ship_list[x-1].status=='Abductin':
                mapa.cow_list.remove(vaca)
                mapa.draw_sprites.remove(vaca)
                mapa.obj_cow_list.remove(vaca)
                mapa.obj_ship_list[x-1].get_away()

    if len(mapa.obj_cow_list)==0:
        endgame=True



    #Locka FPS
    mapa.fps.tick(60)



    #Atualiza display
    pygame.display.flip()


#EndGame
pygame.quit()