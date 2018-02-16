# -*- coding: utf-8 -*-
"""
Created on Sat Feb 03 14:00:22 2018

@author: admin
"""
import os, sys
import pygame
from pygame.locals import *
#from win32api import GetSystemMetrics
#from Babyclass import *
from screeninfo import get_monitors

import recorder.myRecorder as mR
#Get screensize
#x= GetSystemMetrics(0)*0.8
#y= int(GetSystemMetrics(1)*0.8)
mon = get_monitors()
y = mon[0].height;
SCREENRECT     = Rect(0, 0, y, y)

main_dir = os.path.split(os.path.abspath(__file__))[0]

def load_image(file):
    #global y
    "loads an image, prepares it for play"
    file = os.path.join(main_dir, file)
    #y= int(GetSystemMetrics(1)*0.8)
    try:
        surface = pygame.image.load(file)
        surface=pygame.transform.scale(surface, (y,y))
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    return surface.convert()

def load_images(path):
    imgs = []
    for file in os.listdir(path):
        if '.png' in file:
            imgs.append(load_image(path+'/'+file))
    return imgs

class Baby(pygame.sprite.Sprite):
    smile=[]
    sad=[]
    bored = []
    sleep = []
    sleepy = []
    cry = []
    laugh = []
    speak = []
    wakeup = []

    def __init__(self, fps = 2):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.frames=self.smile
        self.current = 0
        self.image = self.frames[0]
        print(self.frames)
        print(self.image)
        self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
        self._next_update = 0    # next time it has to be updated in ms
        self._period = 1000./fps # period of the animation in ms
        self._inv_period = 1./self._period
        self._paused_time = 0
        self._pause_start = 0
        self._frames_len = len(self.frames)

    def changeFace(self):
        if self.frames==self.smile:
            self.frames=self.sad
        else:
            self.frames=self.smile

        self.current = 0
        self._frames_len = len(self.frames)

    def update(self, dt,t):
        if self._next_update <= t:
            # time past since it should have updated
            delta = t - self._paused_time - self._next_update
            # calculate if there are any skipped frames
            skipped_frames = int(delta*self._inv_period)
            # next time to update
            self._next_update = self._next_update + self._period + skipped_frames * self._period
            # update to next image
            self.current += (1+skipped_frames)
            # bind it to the length of the animation
            self.current %= self._frames_len

            self.image = self.frames[self.current]
            self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
        #self.current += 1
        #if self.current == len(self.frames):
        #    self.current = 0


# main window function
def main(winstyle = 0):
    # Initialize pygame
    pygame.init()
    if pygame.mixer and not pygame.mixer.get_init():
        print ('Warning, no sound')
        pygame.mixer = None

    # Set the display mode
    winstyle = 0  # |FULLSCREEN
    bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

    #Load images, assign to sprite classes
    #(do this before the classes are used, after screen setup)
    path='./Faces/'
    Baby.smile = load_images(path+'smile')
    Baby.sad = load_images(path+'sad')
    Baby.bored = load_images(path+'bored')
    Baby.sleep = load_images(path+'sleep')
    Baby.sleepy = load_images(path+'sleepy')
    Baby.cry = load_images(path+'cry')
    Baby.laugh = load_images(path+'laugh')
    Baby.speak = load_images(path+'speak')
    Baby.wakeup = load_images(path+'wakeup')

    #decorate the game window
    icon = pygame.transform.scale(load_image('icon.png'), (32, 32))
    pygame.display.set_icon(icon)
    pygame.display.set_caption('BaoBao')
    #pygame.mouse.set_visible(0)

    #create the background, tile the bgd image
    bgdtile = load_image('background.jpg')
    background = pygame.Surface(SCREENRECT.size)
    for x in range(0, SCREENRECT.width, bgdtile.get_width()):
        background.blit(bgdtile, (x, 0))
    screen.blit(background, (0,0))
    pygame.display.flip()

    #Initialise baby
    all = pygame.sprite.RenderUpdates()
    Baby.containers=all
    Baobao=Baby()
    clock = pygame.time.Clock()

    rec = mR.Recorder(num_chunk = 1)
    rec.stream_init()
    getTicksLastFrame = pygame.time.get_ticks()
    #Game loop
    while 1:
        # get input
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                del rec
                pygame.quit()
                return
        # clear/erase the last drawn sprites
        all.clear(screen, background)

        t = pygame.time.get_ticks()
        dt = (t - getTicksLastFrame) / 1000.0
        getTicksLastFrame = t

        #update all the sprites
        all.update(dt,t)

        keystate = pygame.key.get_pressed()
        #handle player input
        #firing = keystate[K_SPACE]
        audio_data,_ = rec.get_buffer()
        #print(max(abs(audio_data))[0])
        firing = max(abs(audio_data))> 0.1

        if firing:
            Baobao.changeFace()

        #update baby's internal clock
        #Baobao.updateTime(pygame.time.get_ticks())
        #update the baby's state
        #Baobao.setState()
        #get action from the baby
        #Baobao.getAction()
        #Baobao.getReward()
        #pygame.time.delay(2000)
        #draw the scene
        pygame.display.update(all.draw(screen))
        clock.tick(40)
#call the "main" function if running this script
if __name__ == '__main__': main()
