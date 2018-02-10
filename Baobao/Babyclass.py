'''
Created on Feb 3, 2018

@author: Zhou Renjie
'''

import random
import numpy as np
import pandas as pd
from threading import Timer
import pygame
from listentoplayer import *

class Baby(pygame.sprite.Sprite): 
    #Expression
    smile = []
    sad = []
    bored = []
    sleep = []
    sleepy = [] 
    cry = []
    laugh = []
    angry = []
    speak = []
    wakeup = []
    
    #variables needed
    babyMemory=[]
    __currentTime = 0
    __lastSleepTime = 0
    __periodsincelastsleep = 0
    __sleepiness = 0
    __currentState = "Happy"
    __currentFace = []
    state=["Happy","Sad","Bored","NeedAttention","Sleep","Sleepy","Hungry","JustWake"]
    #states
 
    #the initial state shud be randomised but here we put Happy state first
    #currentFace is contained in the State
    #assume it's happy first altho it shud be randomised whenever the interface is opened
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.sleeptimer=15*60*100
        self.__currentFace=self.smile
        self.actionProb=pd.read_csv('action_prob.csv').values
        self.rect = self.__currentFace.get_rect()
    
    #def update(self):
    #    self.rect = self.currentState.get_rect()
        
    def setState(self):
        if self.__sleepiness >= 1:
            self.__currentState = "Sleep"
        if self.__sleepiness >= 0.8:
            __currentState = "Sleepy"
        
    def getState(self):
        return self.__currentState
    
    def updateTime(self, time):
        self.__currentTime = time
        self.__periodsincelastsleep = self.__currentTime - self.__lastSleepTime
        self.__sleepiness = self.__periodsincelastsleep / 15*60*100  #seconds
        
    #def getAction(self):
        
    def smileF(self):
        self.__currentFace = self.smile
        self.rect = self.__currentFace.get_rect()
        
    def sadF(self):
        self.__currentFace = self.sad
        self.rect = self.__currentFace.get_rect()
            
    def laughF(self):
        self.__currentFace = self.laugh
        self.rect = self.__currentFace.get_rect()
        
    def cryF(self):
        self.__currentFace = self.cry
        self.rect = self.__currentFace.get_rect()
        
    def speakF(self):
        self.__currentFace = self.speak
        self.rect = self.__currentFace.get_rect()
        
    def wakeUpF(self):
        self.__currentFace = self.awake
        self.rect = self.__currentFace.get_rect()
        self.__currentState="JustWake"
        self.__lastSleepTime = self.__currentTime
        
    def sleepF(self):
        self.__currentFace = self.sleep
        self.rect = self.__currentFace.get_rect()
        self.__currentState="Sleep"
        t=Timer(15,self.wakeUpF)
        t.start()
        
    def sleepyF(self):
        self.__currentFace = self.sleepy
        self.rect = self.__currentFace.get_rect()
        self.__currentState="Sleepy"
        
    def boredF(self):
        self.__currentFace = bored
        self.rect = self.__currentFace.get_rect()
        self.__currentState="Bored"
        
    def getAction(self):
        #if self.__currentState == "Happy":
        #    self.smileF()
                     
        #elif self.__currentState == "Sad":
        #    self.sadF()
            
        #elif self.__currentState == "Bored":
        #    self.boredF()
            
        #elif self.__currentState == "NeedAttention":
        #    self.speakF()
           
        #elif self.__currentState == "Sleep":
            #depend on the sleepiness call sleep
        #    self.wakeUpF()
            
        #elif self.__currentState == "Sleepy":
        #    self.sleepyF()
                
        #elif self.__currentState == "Hungry":
        #    self.cryF()
        
        i = random.random()
        self.chooseAction(i)
                
             
    #if user_input == "play toy":  #NEED ACTIONlISTNER HERE
    #     the baby crawls towards the toy
    #    self.currentState = happyState
    #
    #if currentState = hungryState:
    #   if timer <= 30s:
    #      if user_input == "drink milk": #NEED ACTIONLISTENER HERE
    #         the baby crawls towards the milk bottle and drink the milk  
    #         self.currentState = happyState
    #   else:
    #       hungryState(or shud it be currentSTate?).noFoodReceived(self.angry)
    #       currentState = angrySTate
    def chooseAction(self,action):
        #loc=np.where(self.state == self.__currentState)
        loc=self.state.index(self.__currentState)
        prob=np.cumsum(self.actionProb,axis=1)[loc]
        print(prob,loc,self.state == self.__currentState,self.state,self.__currentState)
        print(np.shape(self.actionProb))
        if action< prob[0]:
            self.simleF()
            actionNo=0
        elif action< prob[1]:
            self.laughF()
            actionNo=1
        elif action< prob[2]:
            self.cryF()
            actionNo=2
        elif action< prob[3]:
            self.speakF()
            actionNo=3
        elif action< prob[4]:
            self.wakeUpF()
            actionNo=4
        elif action< prob[5]:
            self.sleepF
            actionNo=5
        elif action< prob[6]:
            self.boredF()
            actionNo=6
        elif action< prob[7]:
            self.sadF()
            actionNo=7
        elif action< prob[8]:
            self.sleepyF()
            actionNo=8
        self.state_action=[loc,actionNo]
    def getReward(self):
        [speechvalue,self.babyMemory]=listening(self.babyMemory)
        #Update action probability matrix
        self.actionProb[self.state_action[0],self.state_action[1]]=self.actionProb[self.state_action[0],self.state_action[1]]*(speechvalue+0.5)
    #if user gives a response:
    #   t.cancel()
    #   state is then changed
    #   new timer will start
#boredTest = State.Bored
#babyTest = Baby(boredTest)
#babyTest.setState(State.Happy)
#babyTest.getState().getExpression()
    
