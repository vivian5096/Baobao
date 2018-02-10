# -*- coding: utf-8 -*-
"""
Created on Sat Feb 03 14:00:22 2018

@author: admin
"""
import os, sys
import pygame
from pygame.locals import *
from win32api import GetSystemMetrics
#from Babyclass import *

#Get screensize
#x= GetSystemMetrics(0)*0.8
y= int(GetSystemMetrics(1)*0.8)
SCREENRECT     = Rect(0, 0, y, y)

main_dir = os.path.split(os.path.abspath(__file__))[0]

def load_image(file):
    "loads an image, prepares it for play"
    file = os.path.join(main_dir, file)
    y= int(GetSystemMetrics(1)*0.8)
    try:
        surface = pygame.image.load(file)
        surface=pygame.transform.scale(surface, (y,y))
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    return surface.convert()

def load_images(*files):
    imgs = []
    for file in files:
        imgs.append(load_image(file))
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

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image=self.smile
        self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
    def changeFace(self):
        if self.image==self.smile:
            self.image=self.sad
        else:
            self.image=self.smile
        self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
    #def update(self):
        


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
    path='Expression/'
    Baby.smile = load_image(path+'smile.gif')
    Baby.sad = load_image(path+'sad.gif')
    Baby.bored = load_image(path+'bored.gif')
    Baby.sleep = load_image(path+'sleep.gif')
    Baby.sleepy = load_image(path+'sleepy.gif')
    Baby.cry = load_image(path+'cry.gif')
    Baby.laugh = load_image(path+'laugh.gif')
    Baby.speak = load_image(path+'speak.gif')
    Baby.wakeup = load_image(path+'wakeup.gif')

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
    
    #Game loop
    while 1:
        # get input
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                return
        # clear/erase the last drawn sprites
        all.clear(screen, background)
        #update all the sprites
        all.update()
        
        keystate = pygame.key.get_pressed()
        #handle player input
        firing = keystate[K_SPACE]
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