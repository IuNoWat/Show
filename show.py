

import time

from threading import Thread
import pygame
pygame.mixer.init(48000, -16, 1, 4096)
pygame.font.init()
#import rpi_ws281x as ws

import bib

class Show() :
    def __init__(self,name,bg_color=pygame.Color("Black"),fps=30) :
        #Pygame core
        self.on=True
        self.Screen=pygame.display.set_mode((1920,1080))
        self.Clock=pygame.time.Clock()
        #core
        self.show_name=name
        self.fps=fps
        self.scenes=[]
        self.current_scene=0
        self.currently_playing=False
        self.show_debug=True
        self.current_music=False
        #Scene player
        self.current_frame=0
        #Style
        self.bg_color=bg_color

    def update_current_scene(self) :
        if self.current_frame==0 and self.scenes[self.current_scene].music :
            self.current_music=pygame.mixer.Sound(self.scenes[self.current_scene].music_path)
            self.current_music.play()

        self.scenes[self.current_scene].frames[self.current_frame](self.Screen,self.current_frame)
        self.current_frame+=1

        if self.current_frame==len(self.scenes[self.current_scene].frames) :
            if self.scenes[self.current_scene].loop :
                self.current_frame=0
            else :
                self.current_frame=0
                self.currently_playing=False
                if self.scenes[self.current_scene].music :
                    self.current_music.stop()

    def restart_current_scene(self) :
        self.current_frame=0
        self.current_music.stop()

    def stop_current_scene(self) :
        self.currently_playing=False
        self.current_frame=0
        self.current_music.stop()

    def load_scene(self,scene) :
        self.scenes.append(scene)

    def start(self) :
        #PREPARING MAINLOOP
        my_font = pygame.font.Font('freesansbold.ttf', 10)
        print(f"Launching mainloop of Scene {self.show_name}")
        while self.on :
            #CLEANUP
            self.Screen.fill(self.bg_color)
            #do the ting

            #EVENT HANDLING
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()

                #Commands always on
                if event.type == pygame.QUIT:
                    self.on=False
                if keys[pygame.K_p] :
                    self.on=False
                if keys[pygame.K_w] :
                    self.show_debug = True
                if keys[pygame.K_x] :
                    self.show_debug = False

                #Commands unavailable in play mode
                if self.currently_playing==False :
                    if keys[pygame.K_RIGHT]:
                        if self.current_scene==len(self.scenes)-1 :
                            self.current_scene=0
                        else :
                            self.current_scene+=1
                    if keys[pygame.K_LEFT]:
                        if self.current_scene==0 :
                            self.current_scene=len(self.scenes)-1
                        else :
                            self.current_scene-=1
                    if keys[pygame.K_SPACE]:
                        self.currently_playing=True

            if self.currently_playing :
                self.update_current_scene()

            #DEBUG
            if self.show_debug :
                text_debug = my_font.render(f"FPS : {int(self.Clock.get_fps())} | Playing : {str(self.currently_playing)} | Current_frame : {str(self.current_frame)} | "+str(self.current_scene)+" : "+self.scenes[self.current_scene].name, True, (255,255,255))
                self.Screen.blit(text_debug,(0,0))

            #END OF LOOP
            pygame.display.flip()
            self.Clock.tick(self.fps)


class Scene() :
    def __init__(self,name,nb_of_frames,loop=False) :
        self.name=name
        self.loop=loop
        self.nb_of_frames=nb_of_frames
        self.frames=[]
    def fill(self,method) :
        self.frames=[method for x in range(self.nb_of_frames)]
    def set_music(self,path) :
        self.music=True
        self.music_path=path


if __name__=="__main__" :

    my_scene=Scene("white projector for 100 frames",1000)
    my_scene.fill(bib.changing_white_spot)
    my_scene.set_music("C:\\Users\\loren\\Desktop\\Show\\assets\\infidele.mp3")
                       
    my_second_scene=Scene("white projector looping",1,True)
    my_second_scene.fill(bib.white_spot)
                         
    my_show=Show("default")
    my_show.load_scene(my_scene)
    my_show.load_scene(my_second_scene)
                       
    my_show.start()