import pygame
import random
import sys
from pygame.locals import *


FPS = 32
screenWidth = 289
screenHeight =511
screen = pygame.display.set_mode((screenWidth,screenHeight))
groundY = screenHeight*0.8
game_sprites = {}
game_sounds = {}
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/back.png'
PIPE = 'gallery/sprites/pipe.png'




def welcomeScreen():
    playerx = int(screenWidth/5)
    playery =  int((screenHeight - game_sprites['player'].get_height())/2)
    messagex = int((screenWidth - game_sprites['message'].get_width())/2)
    messagey = int(screenHeight*0.13)
    basex = 0
    while True:
         for event in pygame.event.get():
            if event.type == QUIT or(event.type == KEYDOWN and event.key == K_ESCAPE):
                 pygame.quit()
                 sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return 
            else:
                screen.blit(game_sprites['background'],(0,0))
                screen.blit(game_sprites['player'],(playerx,playery))
                screen.blit(game_sprites['message'],(messagex,messagey))
                screen.blit(game_sprites['base'],(basex,groundY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def getRandomPipe():
    """ genrate pos of 2 pipes"""  
    pipeHeight = game_sprites['pipe'][0].get_height()
    offset = screenHeight/4
    y2 = offset + random.randrange(0,int(screenHeight - game_sprites['base'].get_height()-1.2*offset))    
    pipeX = pipeHeight+10
    y1 = pipeHeight -y2+offset
    pipe =[
        {'x':pipeX , 'y':-y1},
        {'x':pipeX , 'y':y2}
    ]  
    return pipe


def mainGame():
    score = 0
    playerx = int(screenWidth/5)
    playery = int(screenWidth/2)
    basex = 0
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()
    # list of upper pipes
    upperPipes = [
        {'x':screenWidth+200,'y':newPipe1[0]['y']},
        {'x':screenWidth+200+(screenWidth/2),'y':newPipe2[0]['y']},

    ]
    # /list of lower pipes
    lowerPipes = [
        {'x':screenWidth+200,'y':newPipe1[1]['y']},
        {'x':screenWidth+200+(screenWidth/2),'y':newPipe2[1]['y']},

    ]
    pipeVelX = -4
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerSpeed = -8 #velocity flapping pr
    playerFlapped = False #true only when bird is flapping


    while True :
        for event in pygame.event.get():
            if event.type == QUIT or(event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery>0:
                    playerVelY = playerSpeed
                    playerFlapped = True 
                    game_sounds['wing'].play()


        # jb bird pipe is takrai
        crashTest  = isCollide(playerx,playery,upperPipes,lowerPipes)
        if crashTest :
            return
        # score checking and updating

        playerMidPos = playerx + game_sprites['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + game_sprites['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos <pipeMidPos+4:
                score+=1
                print(f"your score is {score}")
                game_sounds['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False
        
        playerHeight = game_sprites['player'].get_height()
        playery = playery+  min(playerVelY,groundY- playery-playerHeight)


        # for moving pipes towards left
        for upperPipe , lowerPipe in zip(upperPipes,lowerPipes):
            upperPipe['x']+=pipeVelX
            lowerPipe['x']+=pipeVelX
        # add new pipe when prev are moving out

        if 0<upperPipes[0]['x']<5:
            newpipe  = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])



        # if the pipe is out of screen remove
        if upperPipes[0]['x']< -game_sprites['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
        
        # blit our sprites
        screen.blit(game_sprites['background'],(0,0))
        for upperPipe,lowerPipe in zip(upperPipes,lowerPipes):
            screen.blit(game_sprites['pipe'][0],(upperPipe['x'],upperPipe['y']))
            screen.blit(game_sprites['pipe'][1],(lowerPipe['x'],lowerPipe['y']))


        screen.blit(game_sprites['base'],(basex,groundY))
        screen.blit(game_sprites['player'],(playerx,playery))

        mydigits = [int(x) for x in list(str(score))]
        width =0
        for digits in mydigits:
            width+=game_sprites['numbers'][digits].get_width()

        Xoffset = (screenWidth - width)/2
        for digits in mydigits :
            screen.blit(game_sprites['numbers'][digits],(Xoffset,screenHeight*0.12)) 
            Xoffset   += game_sprites['numbers'][digits].get_width()
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def isCollide(playerx,playery,upperPipes,lowerPipes):

    if playery > groundY -25 or playery<0:
        game_sounds['hit'].play()
        game_sounds['die'].play()
        return True
    for pipe in upperPipes:
        pipeHeight =  game_sprites['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x'])< game_sprites['pipe'][0].get_width()):
            game_sounds['hit'].play()
            game_sounds['die'].play()
            
            return True
    
    for pipe in lowerPipes:
        if(playery + game_sprites['player'].get_height()>pipe['y'] and abs(playerx - pipe['x'])<game_sprites['pipe'][0].get_width()):
            game_sounds['hit'].play()
            game_sounds['die'].play()
            return True

    return False




if __name__ == "__main__":
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("Chidiya Uddd")
    game_sprites['numbers'] = (
        pygame.image.load('gallery/sprites/0.png').convert_alpha(), 
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),

    )
    game_sprites['message'] = pygame.image.load('gallery/sprites/message.png').convert_alpha()
    game_sprites['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha()
    game_sprites['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
        pygame.image.load(PIPE).convert_alpha()
    )
    game_sprites['background']= pygame.image.load(BACKGROUND).convert()
    game_sprites['player']= pygame.image.load(PLAYER).convert_alpha()
    game_sounds['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    game_sounds['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    game_sounds['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    game_sounds['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    game_sounds['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    while True:
        welcomeScreen()
        mainGame()

    