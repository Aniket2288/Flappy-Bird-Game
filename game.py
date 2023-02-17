import numbers
import random
from string import digits #generating random numbers
import sys
from tkinter import Widget
from turtle import Screen, width  #for cross the game like to click x
import pygame
from pygame.locals import *  # Basic pygame imports

# global variables 
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENHEIGHT,SCREENWIDTH))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SOUND = {}
GAME_SPRITES = {}
PLAYER = 'flappy.bird/photos/bird.png.png'
BACKGROUND = 'flappy.bird/photos/bg_5.png'
PIPE = 'flappy.bird/photos/pipe.png.png' 
def welcomescreen():
    '''
    This shows all images on the screen
    '''
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT * 0.13)
    basex = 0
    
    while True:
        for event in pygame.event.get():
        # if user click on the cross button exit or cose the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN and (event.key == K_SPACE):
                return
            else:
                SCREEN.blit(GAME_SPRITES ['BACKGROUND'], (0 ,0))  
                SCREEN.blit(GAME_SPRITES ['player'], (playerx ,playery))
                SCREEN.blit(GAME_SPRITES ['message'], (messagex , messagey))
                SCREEN.blit(GAME_SPRITES ['base'], (basex , GROUNDY)) 
                pygame.display.update()
                FPSCLOCK.tick(FPS)  #to fix the FPS in game

def maingame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0
    #create 2 pipes 
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()
    #my list of upper pipes
    upperpipe =[
        {'x': SCREENWIDTH+200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH+200 +(SCREENWIDTH/2), 'y': newPipe2[0]['y']},
    ]
    #my list of lower pipes
    lowerpipe = [
        {'x': SCREENWIDTH+200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH+200 +(SCREENWIDTH/2), 'y': newPipe2[1]['y']},
    ]

    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8 # velocity while flapping
    playerFlapped = False # It is true only when the bird is flapping


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUND['wing'].play()

        carshTest = iscollide(playerx,playery,upperpipe,lowerpipe)
        if  carshTest:
            return
        #check for score
        PlayerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperpipe:
            PipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if PipeMidPos<= PlayerMidPos < PipeMidPos + 4:
                score +=1
            print(f"your score is {score}")
        GAME_SOUND['point'].play()


        if playerVelY <playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False            
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        # move pipes to the left
        for upperPipe , lowerPipe in zip(upperPipe, lowerPipe):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0<upperPipe[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipe.append(newpipe[0])
            lowerPipe.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if upperPipe[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipe.pop(0)
            lowerPipe.pop(0)
        
        # Lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['BACKGROUND'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipe, lowerPipe):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))
        SCREEN.blit(GAME_SPRITES['player'], (playerx,playery))
        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        xoffset = (SCREENWIDTH - Widget)/2

        for digit in myDigits:
            Screen.blit(GAME_SPRITES['numbers'][digit](xoffset, SCREENHEIGHT * 0.12))
            xoffset += GAME_SPRITES['numbers'][digit].get_width() 
            pygame.display.update()
            FPSCLOCK.tick(FPS)


def iscollide(playerx,playery,upperpipe,lowerpipe):
    if playery> GROUNDY - 25 or playery<0:
        GAME_SOUND['Hit'].play()
        return True

    for pipe in upperpipe:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUND['Hit'].play()
            return True

    for pipe in lowerpipe:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUND['Hit'].play()
            return True

    return False
 


def getRandomPipe():
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height()  - 1.2 *offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, #upper Pipe
        {'x': pipeX, 'y': y2} #lower Pipe
    ]
    return pipe

if __name__ == "__main__":
    pygame.init()   # intialise all pygame module
    FPSCLOCK = pygame.time.Clock()  
    pygame.display.set_caption("flappy Birds by Aniket")
    # GAME_SPRITES[numbers] = (
    #     pygame.image.load( ).convert_alpha(),
    #     pygame.image.load( ).convert_alpha(),
    #     pygame.image.load( ).convert_alpha(),
    #     pygame.image.load( ).convert_alpha(),
    #     pygame.image.load( ).convert_alpha(),
    #     pygame.image.load( ).convert_alpha(),
    #     pygame.image.load( ).convert_alpha(),
    #     pygame.image.load( ).convert_alpha(),
    # )

    GAME_SPRITES['message'] = pygame.image.load(r"flappy.bird/photos/message.png").convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load(r'flappy.bird/photos/download (2).png').convert_alpha()
    GAME_SPRITES['pipe'] =(pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
    pygame.image.load(PIPE).convert_alpha()
    )

    #game sounds
    GAME_SOUND['die'] = pygame.mixer.Sound(r'flappy.bird/sounds/die.wav')
    GAME_SOUND['Hit'] = pygame.mixer.Sound(r'flappy.bird/sounds/Hit.mp3')
    GAME_SOUND['point'] = pygame.mixer.Sound(r'flappy.bird/sounds/point.mp3')
    GAME_SOUND['swoosh'] = pygame.mixer.Sound(r'flappy.bird/sounds/Swoosh.mp3')
    GAME_SOUND['wing'] = pygame.mixer.Sound(r'flappy.bird/sounds/wing.wav')

    GAME_SPRITES['BACKGROUND'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomescreen() #This is the main screen to display while opening the game untill press any button
        maingame()  #This is main game function
