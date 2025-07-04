
import pygame


def white_spot(screen,current_frame) :
    size=screen.get_size()
    pygame.draw.circle(screen,(255,255,255),(size[0]/2,size[1]/2),100)

def changing_white_spot(screen,current_frame) :
    size=screen.get_size()
    if 200<current_frame<500 :
        pygame.draw.circle(screen,(255,255,255),(size[0]/2,size[1]/2),100+current_frame-200)
    elif 500<current_frame<800 :
        pygame.draw.circle(screen,(255,255,255),(size[0]/2,size[1]/2),100+300-(current_frame-500))
    else :
        pygame.draw.circle(screen,(255,255,255),(size[0]/2,size[1]/2),100)



