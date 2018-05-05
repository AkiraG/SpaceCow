# coding=ISO-8859-1
import pygame
from pygame.locals import QUIT, Rect, MOUSEBUTTONDOWN

MENU = 0
JOGAR = 1
INFO= 2
SAIR = 3
VOLTAR = 4



dimensoes = (940, 680)
estado = 0

menu_principal = [
                    {   "texto":"Jogar", "pos":(320, 50), "tamanho":(0,0), 
                        "negrito":True, "italico":False, "size":32, "cor":(255, 0, 0) },

                    {   "texto":"Informações", "pos":(320, 150), 
                        "negrito":True, "italico":False, "size":32, "cor":(255, 0, 0) },

                    {   "texto":"Sair", "pos":(320, 250), 
                        "negrito":True, "italico":False, "size":32, "cor":(255, 0, 0) }
                  
                  
                  ]

menu_info = [

                    {   "texto":"Desenvolvedores", "pos":(120, 50), "tamanho":(0,0), 
                        "negrito":True, "italico":False, "size":32, "cor":(255, 0, 0) },

                    {   "texto":"Sonoplastia: Flavio", "pos":(120, 150), 
                        "negrito":True, "italico":False, "size":32, "cor":(255, 0, 0) },

                    {   "texto":"Arte: Carlos and Matheus", "pos":(120, 250), 
                        "negrito":True, "italico":False, "size":32, "cor":(255, 0, 0) },

                    {   "texto":"Progamação : Shisho , Sensei and Senshi", "pos":(120, 350), 
                        "negrito":True, "italico":False, "size":32, "cor":(255, 0, 0) },

                    {   "texto":"Voltar", "pos":(120, 450), 
                        "negrito":True, "italico":False, "size":32, "cor":(255, 0, 0) }

        
                   ]


pygame.init()

def desenha_menu( screen ):
    for elemento in menu_principal:
        fonte = pygame.font.SysFont('arial', elemento['size'], 
                                    elemento['negrito'], elemento['italico'] )
        texto_surface = fonte.render( elemento['texto'], True,  elemento['cor'])
        elemento['tamanho'] = (texto_surface.get_width(), texto_surface.get_height())
        screen.blit( texto_surface, elemento['pos']) 


def desenha_info( screen ):
    for elemento in menu_info:
        fonte = pygame.font.SysFont('arial', elemento['size'], 
                                    elemento['negrito'], elemento['italico'] )
        texto_surface = fonte.render( elemento['texto'], True,  elemento['cor'])
        elemento['tamanho'] = (texto_surface.get_width(), texto_surface.get_height())
        screen.blit( texto_surface, elemento['pos'])


def acao ( comando ):
    global estado
    if (comando == 'Jogar'):
        estado = JOGAR

    elif (comando == 'Informações'):
        estado = INFO

    elif (comando == 'Sair'):
        estado = SAIR

    elif (comando == 'Voltar'):
        estado = VOLTAR

    print estado
        
def menu_bosta():

    def testa_clique( evento ):
        x, y = evento.pos
        for elemento in menu_principal:
            r = Rect( elemento['pos'], elemento['tamanho'] )
            if (r.collidepoint( (x, y) )):
                print "Opcao : " + elemento['texto'] + "acionada"
                acao( elemento['texto'] )
 



    screen = pygame.display.set_mode( dimensoes, 0, 32 )



    desenha_menu( screen )


    while (True):
        pygame.display.update()
    
        if (estado == JOGAR):
            screen.fill((255, 255, 0))

        elif (estado == INFO):
            screen.fill((0, 0, 0))
            desenha_info( screen )
            def testa_clique( evento ):
                x, y = evento.pos
                for elemento in menu_info:
                    r = Rect( elemento['pos'], elemento['tamanho'] )
                    if (r.collidepoint( (x, y) )):
                        print "Opcao : " + elemento['texto'] + "acionada"
                        acao( elemento['texto'] )

        elif (estado == VOLTAR):
            screen.fill((0, 0, 0))
            desenha_menu( screen )
            def testa_clique( evento ):
                x, y = evento.pos
                for elemento in menu_principal:
                    r = Rect( elemento['pos'], elemento['tamanho'] )
                    if (r.collidepoint( (x, y) )):
                        print "Opcao : " + elemento['texto'] + "acionada"
                        acao( elemento['texto'] )





        for e in pygame.event.get():
            if (e.type == QUIT or estado == SAIR):
                exit()
            elif (e.type == MOUSEBUTTONDOWN):
                testa_clique( e )
menu_bosta()           





            
