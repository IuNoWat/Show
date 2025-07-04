import time

import pygame
#import rpi_ws281x as ws

import bib_new as bib

#pygame.init()

#BLACK=ws.Color(0,0,0)
#RED=ws.Color(255,0,0)
#GREEN=ws.Color(0,255,0)
#BLUE=ws.Color(0,0,255)
#BLACK=ws.Color(255,255,255)

BLACK=[0,0,0]
RED=[255,0,0]
GREEN=[0,255,0]
BLUE=[0,0,255]
WHITE=[255,255,255]

band=[
    [[0,0,0]]*144,
    [[255,255,255]]*144,
    [[0,0,0]]*144,
    [[255,255,255]]*144,
    [[0,0,0]]*144,
    [[255,255,255]]*144,
    [[0,0,0]]*144,
    [[255,255,255]]*144,
    [[0,0,0]]*144,
    [[255,255,255]]*144
]


class Bar() :
    def __init__(self,strip_length=144,led_pin=10,freq=800000,dma=10,invert=False,brightness=255,channel=0) :
        #constantes
        self.strip_length=strip_length
        self.led_pin=led_pin
        self.freq=freq
        self.dma=dma
        self.invert=invert
        self.brightness=brightness
        self.channel=channel
        #création de la strip
        self.strip = ws.PixelStrip(strip_length, led_pin, freq, dma, invert, brightness, channel)
        self.strip.begin()
        #variable de fonctionnement
        self.band=[]
        self.current_frame=0
        self.framerate=10
        self.clock=pygame.time.Clock()
        self.on=True
    def fill(self,col=[0,0,0]) :
        for i in range(0,self.strip_length) :
            self.strip.setPixelColorRGB(i,col[0],col[1],col[2])
    def load_band(self,band) :
        self.band=band
    def update_current_frame(self) :
        #print(self.current_frame)
        #print(self.band[self.current_frame])
        frame=self.band[self.current_frame]
        for i,pxl in enumerate(frame) :
            #print(self.band[self.current_frame-1][i])
            if pxl!=self.band[self.current_frame-1][i] :
                self.strip.setPixelColorRGB(i,pxl[0],pxl[1],pxl[2])
    def play(self) :
        while self.current_frame<len(self.band) and self.on :
            self.update_current_frame()
            self.strip.show()
            #time.sleep(1/self.framerate)
            self.clock.tick(self.framerate)
            self.current_frame+=1
        self.current_frame=0
    def set_brightness(self,value) :
        ws.ws.ws2811_channel_t_brightness_set(self._channel,value)

class Show() :
    def __init__(self,name,strip_length=144,led_pin=10,brightness=255,music_path=False,screen=False) :
        #constantes
        self.name=name
        self.strip_length=strip_length
        self.led_pin=10
        #création de la strip
        #self.strip = ws.PixelStrip(strip_length, self.led_pin, 800000, 10, False, brightness, 0)
        #self.strip.begin()
        #variable de fonctionnement du player
        self.band=[]
        self.screen_instructions=[]
        self.current_frame=0
        self.framerate=10
        self.clock=pygame.time.Clock()
        self.on=True
        self.screen=screen
        #Gestion de la musique
        self.music_path=music_path
    def fill(self,col=[0,0,0]) :
        for i in range(0,self.strip_length) :
            self.strip.setPixelColorRGB(i,col[0],col[1],col[2])
    def load_music(self) :
        self.my_sound=pygame.mixer.Sound(self.music_path)
    def load_band(self,band) :
        self.band=band
    def load_screen(self,screen) :
        self.screen_instructions=screen
    def update_current_frame(self) :
        if self.band!=[] :
            frame=self.band[self.current_frame]
            for i,pxl in enumerate(frame) :
                if pxl!=self.band[self.current_frame-1][i] :
                    self.strip.setPixelColorRGB(i,pxl[0],pxl[1],pxl[2])
    def update_current_screen(self) :
        if self.screen!=False :
            self.screen_instructions[self.current_frame][0](self.screen)
    def play(self) :
        if self.music_path!=False :
            self.my_sound.play()
        while self.current_frame<len(self.band) or self.current_frame<len(self.screen_instructions) and self.on :
            self.update_current_frame()
            self.update_current_screen()
            #self.strip.show()
            if self.screen!=False :
                pygame.display.flip()
            #
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.on=False
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    self.on=False
                    if self.music_path!=False :
                        self.my_sound.stop()
            self.clock.tick(self.framerate)
            self.current_frame+=1
        self.current_frame=0
        self.on=True
        if self.music_path!=False :
            self.my_sound.stop()
    def set_brightness(self,value) :
        ws.ws.ws2811_channel_t_brightness_set(self._channel,value)

def main() :
    #Launch Core
    on=True
    Screen=pygame.display.set_mode((1920,1080))
    current_show=0
    Shows=[0,1,2,3,4,5,6,7]
    #Create Shows database
    Shows[0]=(Show("0 - Introduction",screen=Screen))
    Shows[0].load_screen(bib.classic_white_projector.frames)
    #Shows[0].load_band(bib.white_projector.frames)
    #Shows[0].load_music()
    Shows[1]=(Show("1 - Interlude Musicale",screen=Screen))
    Shows[1].load_screen(bib.classic_white_projector.frames)
    #Shows[0].load_band(bib.ambiance_nicolas.frames)
    Shows[2]=(Show("2 - Danse Rock",screen=Screen))
    #Shows[2].load_band(bib.envole_moi.frames)
    #Shows[2].load_music()
    Shows[3]=(Show("3 - Infidèle",screen=Screen))
    #Shows[3].load_band(bib.band_v1.frames)
    #Shows[3].load_music()
    Shows[4]=(Show("4 - Interlude Musicale",screen=Screen))
    Shows[4].load_screen(bib.classic_white_projector.frames)
    #Shows[4].load_band(bib.ambiance_nicolas.frames)
    Shows[5]=(Show("5 - One Man Show",screen=Screen))
    Shows[6]=(Show("6 - Chelou",screen=Screen))
    Shows[7]=(Show("7 - Final",screen=Screen))

    #text handler
    my_font = pygame.font.Font('freesansbold.ttf', 10)
       
    #Main Loop
    while on :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                on=False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                if current_show>=len(Shows)-1 :
                    current_show=0
                else :
                    current_show+=1
            if keys[pygame.K_LEFT]:
                if current_show<=0 :
                    current_show=len(Shows)-1
                else :
                    current_show-=1
            if keys[pygame.K_SPACE]:
                Shows[current_show].play()
        text = my_font.render(str(current_show)+" : "+Shows[current_show].name, True, (255,255,255))
        Screen.fill((0,0,0))
        Screen.blit(text,(0,0))
        pygame.display.flip()


pygame.mixer.init(48000, -16, 1, 4096)
pygame.font.init()

main()

#    
#    test_screen.load_screen(bib.screen_v1.frames)
#    test_screen.load_music()
#    test_screen.play()



#meh=Bar()
#meh.load_band(bib.band_v1.frames)


def do_the_thing() :
    my_sound.play()
    meh.play()
    meh.fill()
    meh.strip.show()

#do_the_thing()

#def go() :
#    test_screen=Show("Projector",screen=True,music_path="infidele.mp3")
#    test_screen.load_screen(bib.screen_v1.frames)
#    test_screen.load_music()
#    test_screen.play()



#meh.fill([0,0,0])
#meh.strip.show()