import pygame
import os
import RPi.GPIO as GPIO
import time
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.IN)
GPIO.setup(27, GPIO.IN)
GPIO.setup(23, GPIO.IN)
GPIO.setup(24, GPIO.IN)

pygame.init()

## Global Variables
width = 1230
heigth= 900
edge  = 10
shome = 0
sguest= 0
period= 1
menu  = 0
enter = 0
down  = 0
right = 0
scond1= 0
scond2= 0
scond3= 1
pause = 0
playing = 0
nextPerid = 0
Themesong = 0
stopButton1 = 0
stopButton2 = 0

## Setting of the window
#screen = pygame.display.set_mode((width,heigth))
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
screen.fill(pygame.Color(0,0,0,))

pygame.draw.rect(screen,
                 pygame.Color(255,255,255),
                 (edge,edge,width-edge*2,heigth-edge*2),
                 10)

pygame.draw.rect(screen,
                 pygame.Color(255,255,255),
                 (310,100,600,250),
                 10)

pygame.draw.rect(screen,
                 pygame.Color(255,255,255),
                 (80,500,300,250),
                 5)

pygame.draw.rect(screen,
                 pygame.Color(255,255,255),
                 (width - (80+300),500,300,250),
                 5)

Font = pygame.font.SysFont("droidserif", 220)
Font2 = pygame.font.SysFont("ARIAL BLACK", 130)
labelHome = Font2.render("HOME", 1, pygame.Color(255,255,255))
screen.blit(labelHome, (85, 760))
labelHome = Font2.render("GUEST", 1, pygame.Color(255,255,255))
screen.blit(labelHome, (width - (80+300), 760))


## Add Logo
logo2 = pygame.image.load("Rasp0.png");
logo2.convert_alpha()
screen.blit(logo2, (width-300, 30))

## Time
class TimeGame:
    """ Implements a stop watch. """                                                                
    def __init__(self):        
        self._start = 0.0        
        self._elapsedtime = 0.0
        self._running = 0
        self.endgame = 0
    
    def _update(self): 
        """ Update elapsed time. """
        self._elapsedtime = time.time() - self._start
        self._setTime(self._elapsedtime)
        
    def _setTime(self, elap):
        """ Set the time string to Minutes:Seconds:Hundreths """
        minutes = int(elap/60)
        seconds = int(elap - minutes*60.0)
        hseconds = int((elap - minutes*60.0 - seconds)*100)

        m2 = minutes % 10
        s1 = seconds / 10
        s2 = seconds % 10
        hs = hseconds / 10
        stime = str(m2)+str(s1)+":"+str(s2)+str(hs)
        timestop = stime

        if (minutes == 2) & (seconds == 0):      
            self.endgame = 1
            
        if (self.endgame == 1):
            self._elapsedtime = 0.0
            self._start = time.time() - self._elapsedtime
            print("endgame = True")
            
        labelTime = Font.render(stime, 1, pygame.Color(255,255,0))
        screen.blit(labelTime, (330, 100))

    def Start(self):                                                     
        """ Start the stopwatch, ignore if running. """    
        if not self._running:            
            self._start = time.time() - self._elapsedtime
            self._running = 1
            print("_running")
            running = 1
        self._update()
    
    def Stop(self):                                    
        """ Stop the stopwatch, ignore if stopped. """
        if self._running:        
            self._elapsedtime = time.time() - self._start    
            self._setTime(self._elapsedtime)
            self._running = 0
        else:
            self._setTime(self._elapsedtime)

    def Reset(self):                                  
        """ Reset the stopwatch. """
        self._start = time.time()         
        self._elapsedtime = 0.0    
        self._setTime(self._elapsedtime)
        print("Reset")

def clear():
    pygame.draw.rect(screen,
                     pygame.Color(0,0,0),
                     (310+10,100+10,600-20,250-20),
                     0)

    pygame.draw.rect(screen,
                     pygame.Color(0,0,0),
                     (80+5,500+5,300-10,250-10),
                     0)

    pygame.draw.rect(screen,
                     pygame.Color(0,0,0),
                     (width - (80+300)+5,500+5,300-10,250-10),
                     0)

    pygame.draw.rect(screen,
                     pygame.Color(0,0,0),
                     (width/2 - 50,heigth/2+40, 250, 250),
                     0)
    pygame.draw.rect(screen,
                 pygame.Color(0,0,0),
                 (width/2-225,400,455,450),
                 0)
   
tg = TimeGame()

while True:
    print(str(shome))
    clear()
        
    ## Events
    B1 = GPIO.input(22)
    B2 = GPIO.input(27)
    G1 = GPIO.input(23)
    G2 = GPIO.input(24)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                break
                    
            if event.key == pygame.K_e:
                enter = enter + 1
            if enter > 1:
                enter = 0
            if event.key == pygame.K_DOWN:
                down = down + 1
                enter = 0
            if down > 2:
                down = 0
            if event.key == pygame.K_RIGHT:
                right = right + 1
            if right > 1:
                right = 0
            if event.key == pygame.K_m:
                menu = menu + 1
            if menu > 1:
                menu = 0
            if event.key == pygame.K_p:
                pause = pause + 1
            if pause > 1:
                pause = 0

    ## Main Labels
    if shome < 10:
        sshome = "0" + str(shome)
    else:
        sshome = str(shome)
    if sguest < 10:
        ssguest = "0" + str(sguest)
    else:
        ssguest = str(sguest)
        
    labelHomeS = Font.render(sshome, 1, pygame.Color(255,0,0))
    screen.blit(labelHomeS, (100, 500))
    labelHomeS = Font.render(ssguest, 1, pygame.Color(255,0,0))
    screen.blit(labelHomeS, (width - (60+300), 500))

    if menu == 0:
        labelHomeS = Font.render(str(period), 1, pygame.Color(0,255,0))
        screen.blit(labelHomeS, (width/2-50, heigth/2))
        labelHome = Font2.render("PERIOD", 1, pygame.Color(255,255,255))
        screen.blit(labelHome, (width/2 - 160, heigth/2 - 50))

        if pause == 0:
        ## Playing
            if G1 == False:
                tg.Stop()
                stopButton1 = 1
                sguest = sguest + 1

                if sguest < 10:
                    ssguest = "0" + str(sguest)
                else:
                    ssguest = str(sguest)
                pygame.draw.rect(screen,
                                 pygame.Color(0,0,0),
                                 (width - (80+300)+5,500+5,300-10,250-10),
                                 0)
                labelHomeS = Font.render(ssguest, 1, pygame.Color(255,0,0))
                screen.blit(labelHomeS, (width - (60+300), 500))
                
                while stopButton1 == 1:
                    FontPressButton = pygame.font.SysFont("ARIAL BLACK", 60) 
                    labelSB = FontPressButton.render("GUEST SCORED", 1, pygame.Color(255,255,0))
                    screen.blit(labelSB, (460, 720))
                    labelSB = FontPressButton.render("-- PRESS BUTTON --", 1, pygame.Color(255,255,0))
                    screen.blit(labelSB, (420, 800))
                    if B1 == True:
                        stopButton1 = 0
                        time.sleep(.01)
                    pygame.display.update()
                    B1 = GPIO.input(22)

            if G2 == False:
                tg.Stop()
                stopButton2 = 1
                shome = shome + 1

                if shome < 10:
                    sshome = "0" + str(shome)
                else:
                    sshome = str(shome)
                pygame.draw.rect(screen,
                                 pygame.Color(0,0,0),
                                 (80+5,500+5,300-10,250-10),
                                 0)
                labelHomeS = Font.render(sshome, 1, pygame.Color(255,0,0))
                screen.blit(labelHomeS, (100, 500))
    
                while stopButton2 == 1:
                    FontPressButton = pygame.font.SysFont("ARIAL BLACK", 60) 
                    labelSB = FontPressButton.render("HOME SCORED", 1, pygame.Color(255,255,0))
                    screen.blit(labelSB, (460, 720))
                    labelSB = FontPressButton.render("-- PRESS BUTTON --", 1, pygame.Color(255,255,0))
                    screen.blit(labelSB, (420, 800))
                    if B2 == True:
                        stopButton2 = 0
                        time.sleep(.01)
                    pygame.display.update()
                    B2 = GPIO.input(27)           
            
            if scond3 == 1: ## reset
                tg.Reset()
                shome  = 0
                sguest = 0
                enter = 0
                down  = 0
                right = 0
                scond1= 0
                scond2= 0
                scond3= 1
                playing = 0
                period = 1
                Themesong = 0
            else: ## playing
                if scond1 == 0: ## Time
                    if (Themesong == 0):
                        os.system('mpg321 HockeyTheme.mp3 &')
                        print("executing...")
                        pygame.display.update()
                        sleep(17)
                    Themesong = 1
                    print("Time running")
                    playing = 1
                    tg.Start()
                    if (tg.endgame == 1):
                        period = period + 1
                        if period > 3:
                            if shome > sguest:
                                FontPE = pygame.font.SysFont("ARIAL BLACK", 60) 
                                labelHome = FontPE.render("HOME WINS", 1, pygame.Color(0,255,0))
                                screen.blit(labelHome, (width/2 - 120, heigth - 150))
                                pygame.display.update()
                                sleep(3)
                            if shome < sguest:
                                FontPE = pygame.font.SysFont("ARIAL BLACK", 60) 
                                labelHome = FontPE.render("GUEST WINS", 1, pygame.Color(0,255,0))
                                screen.blit(labelHome, (width/2 - 120, heigth - 150))
                                pygame.display.update()
                                sleep(3)
                            if shome == sguest:
                                FontPE = pygame.font.SysFont("ARIAL BLACK", 60) 
                                labelHome = FontPE.render("NOBADY WINS", 1, pygame.Color(0,255,0))
                                screen.blit(labelHome, (width/2 - 120, heigth - 150))
                                pygame.display.update()
                                sleep(3)
                            tg.Reset()
                            shome  = 0
                            sguest = 0
                            enter = 0
                            down  = 0
                            right = 0
                            scond1= 0
                            scond2= 0
                            scond3= 1
                            pause = 0
                            playing = 0
                            period = 1
                            Themesong = 0

                        else: 
                            nextPeriod = 0
                            tg.endgame = 0
                            while nextPeriod == 0:
                                tg.Stop()
                                pygame.draw.rect(screen,
                                                 pygame.Color(0,0,0),
                                                 (width/2-150,heigth - 150,300,100),
                                                 0)
                                FontPE = pygame.font.SysFont("ARIAL BLACK", 60) 
                                labelHome = FontPE.render("Press Enter", 1, pygame.Color(0,0,255))
                                screen.blit(labelHome, (width/2 - 120, heigth - 150))
                                for event in pygame.event.get():
                                    if event.type == pygame.KEYDOWN:
                                        if event.key == pygame.K_e:
                                            nextPeriod = 1
                                pygame.display.update()
                else:
                ## Score game
                    if (Themesong == 0):
                        os.system('mpg321 HockeyTheme.mp3 &')
                        print("executing...")
                        pygame.display.update()
                        sleep(17)
                    Themesong = 1
                    print("Score running")
                    playing = 1
                    clearData = 0
                    if shome == 4:
                        FontPE = pygame.font.SysFont("ARIAL BLACK", 60) 
                        labelHome = FontPE.render("HOME WINS", 1, pygame.Color(0,255,0))
                        screen.blit(labelHome, (width/2 - 120, heigth - 150))
                        pygame.display.update()
                        sleep(3)
                        clearData = 1
                    if sguest == 4:
                        FontPE = pygame.font.SysFont("ARIAL BLACK", 60) 
                        labelHome = FontPE.render("GUEST WINS", 1, pygame.Color(0,255,0))
                        screen.blit(labelHome, (width/2 - 120, heigth - 150))
                        pygame.display.update()
                        sleep(3)
                        clearData = 1
                    if clearData == 1:
                        shome  = 0
                        sguest = 0
                        enter = 0
                        down  = 0
                        right = 0
                        scond1= 0
                        scond2= 0
                        scond3= 1
                        playing = 0
                        period = 1
                        Themesong = 0
                    
        else:
            tg.Stop()
            labelHome = Font2.render("PAUSE", 1, pygame.Color(255,0,0))
            screen.blit(labelHome, (width/2 - 150, heigth - 150))
    else:
        tg.Stop()
        Font3 = pygame.font.SysFont("ARIAL BLACK", 90)
        labelHome = Font3.render("GAME MODE", 1, pygame.Color(255,255,255))
        screen.blit(labelHome, (width/2 - 185, heigth/2 - 50))
        
        Font3 = pygame.font.SysFont("ARIAL BLACK", 60)

        if down == 0:
            labelHome = Font3.render("<                                     >", 1, pygame.Color(255,255,0))
            screen.blit(labelHome, (width/2 - 225, heigth/2 + 50))
            if enter == 1:
                if right == 0:
                    scond1 = 0
                else:
                    scond1 = 1
    
        if down == 1:
            labelHome = Font3.render("<                                     >", 1, pygame.Color(255,255,0))
            screen.blit(labelHome, (width/2 - 225, heigth/2 + 170))
            if enter == 1:
                if right == 0:
                    scond2 = 0
                else:
                    scond2 = 1

        if down == 2:
            labelHome = Font3.render("<                                     >", 1, pygame.Color(255,255,0))
            screen.blit(labelHome, (width/2 - 225, heigth/2 + 230))
            if enter == 1:
                if right == 0:
                    scond3 = 0
                else:
                    scond3 = 1

        if scond1 == 0:
            labelHome = Font3.render("    Timed  Mode", 1, pygame.Color(255,255,255))
            screen.blit(labelHome, (width/2 - 165, heigth/2 + 50))
            labelHome = Font2.render("20:00", 1, pygame.Color(255,255,0))
            screen.blit(labelHome, (width/2 - 100, heigth/2 + 80))
        else:
            labelHome = Font3.render("  Scoring Mode", 1, pygame.Color(255,255,255))
            screen.blit(labelHome, (width/2 - 165, heigth/2 + 50))
            labelHome = Font2.render("4 GOALS", 1, pygame.Color(255,255,0))
            screen.blit(labelHome, (width/2 - 200, heigth/2 + 80))
        if scond2 == 0:
            labelHome = Font3.render("   Constant  Airflow", 1, pygame.Color(255,255,255))
            screen.blit(labelHome, (width/2 - 210, heigth/2 + 170))
        else:
            labelHome = Font3.render(" Random dead zones", 1, pygame.Color(255,255,255))
            screen.blit(labelHome, (width/2 - 210, heigth/2 + 170))
        if scond3 == 0:
            labelHome = Font3.render("          PLAY", 1, pygame.Color(255,255,255))
            screen.blit(labelHome, (width/2 - 170, heigth/2 + 230))
        else:
            labelHome = Font3.render("         RESET", 1, pygame.Color(255,255,255))
            screen.blit(labelHome, (width/2 - 170, heigth/2 + 230))
       
    pygame.display.update()
    time.sleep(.01)



