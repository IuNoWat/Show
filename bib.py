
import pygame




def interlude_musicale_spot(screen,current_frame) :
    size=screen.get_size()
    pygame.draw.circle(screen,(100,100,100),(1300,600),300)
    pygame.draw.circle(screen,(100,100,100),(400,400),300)

def red(screen,current_frame) :
    screen.fill((255,0,0))

def red_spot(screen,current_frame) :
    pygame.draw.circle(screen,(255,0,0),(1920/2,1080/2),500)

def white_spot(screen,current_frame) :
    pygame.draw.circle(screen,(200,200,200),(1920/2,400),400)

def bi_spot(screen,current_frame) :
    i=current_frame%510
    if i<=255 :
        pygame.draw.circle(screen,(i,0,255-i),(1920/2,400),400)
    else :
        pygame.draw.circle(screen,(510-i,0,i-255),(1920/2,400),400)

def double_bi_spot(screen,current_frame) :
    size=screen.get_size()
    pygame.draw.circle(screen,(255,0,0),(400,540),400)
    pygame.draw.circle(screen,(0,0,255),(1220,540),400)

def changing_white_spot(screen,current_frame) :
    size=screen.get_size()
    if 200<current_frame<500 :
        pygame.draw.circle(screen,(255,255,255),(size[0]/2,size[1]/2),100+current_frame-200)
    elif 500<current_frame<800 :
        pygame.draw.circle(screen,(255,255,255),(size[0]/2,size[1]/2),100+300-(current_frame-500))
    else :
        pygame.draw.circle(screen,(255,255,255),(size[0]/2,size[1]/2),100)

def nothing(sceen,current_frame) :
    pass

