import pygame
import random
import math
from pygame import mixer
#Initialize the pygame 
pygame.init()

#create screen
screen=pygame.display.set_mode((800,600))

#background music
mixer.music.load('background.wav')
mixer.music.play(-1)

#Change Icon and Title
pygame.display.set_caption("Manisha")
icon=pygame.image.load('lion.png')
pygame.display.set_icon(icon)

# player
player_img=pygame.image.load('ufo.png')
player_x=300
player_y=480
player_x_change=0

#enemy
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 6

for i  in range (num_of_enemies):
    enemy_img.append(pygame.image.load('enemy1.png'))
    enemy_x.append(random.randint(0,735))
    enemy_y.append(random.randint(50,150))
    enemy_x_change.append(0.3)
    enemy_y_change.append(40)

#bullet
# redy = you can't see bullet in redy state
# fire = the bullet currently moving
bullet_img=pygame.image.load('bullet.png')
bullet_x=0
bullet_y=480
bullet_x_change=0
bullet_y_change=10
bullet_state='ready'

# display score on pygame window
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
text_x = 10
text_y =10
def show_score(x,y):
    score = font.render('Score:-'+str(score_value),True,(0,0,255))
    screen.blit(score,(x,y))

#game over
game = pygame.font.Font('freesansbold.ttf',84)
def game_over_text():
    over_text = font.render('GAME-OVER',True,(0,0,255))
    screen.blit(over_text,(250,250))


#create function for player 
def player(x,y):
    screen.blit(player_img,(player_x,player_y))

#create function for enemy
def enemy(x,y,i):
    screen.blit(enemy_img[i],(enemy_x[i],enemy_y[i]))

#create function for bullet

def bullet_fire(x,y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet_img,(x + 16,y + 10))

#collision
def iscollision(enemy_x,enemy_y,bullet_x,bullet_y):
    distance=math.sqrt((math.pow(enemy_x - bullet_x,2))+(math.pow(enemy_y - bullet_y,2)))
    if distance < 27:
        return True
    else:
        return False

#Game Loop
running= True
while running:
    #RGB=Red Green Black
    screen.fill((0,255,0))
    # player_x += 1
    # player_y -= 0.10
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # print('my key down ')
            #for left move press left arrow key
            if event.key == pygame.K_LEFT:
                player_x_change = -5

            if event.key == pygame.K_RIGHT:
                player_x_change = 5

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bullet_x = player_x
                    bullet_fire(bullet_x,bullet_y)

        # if any key press that movement stop
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0
    
    player_x += player_x_change
    # start code for boundries player
    if player_x <= 0:
        player_x = 0
    elif player_x >=736: #total window width subtract by image pixels size like 800-64=736. 800 is my window width and 64 is image pixcels 
        player_x = 736
    # end cof for boundries olayer
   

    #boudries for enemy
    for i in range(num_of_enemies):
         #game over
        if enemy_y[i] > 440:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000
            game_over_text()
            break
    
        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 0.3
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >=736: #total window width subtract by image pixels size like 800-64=736. 800 is my window width and 64 is image pixcels 
            enemy_x_change[i] = -0.3
            enemy_y[i] += enemy_y_change[i]

        #collsion
        collision=iscollision(enemy_x[i],enemy_y[i],bullet_x,bullet_y)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bullet_y = 480
            bullet_state = "ready"
            score_value += 1  
            enemy_x[i]=random.randint(0,735)
            enemy_y[i]=random.randint(50,150)
        enemy(enemy_x[i],enemy_y[i],i)
    #fire bullet movement
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = 'ready'
    if bullet_state == 'fire':
        bullet_fire(bullet_x,bullet_y)
        bullet_y -= bullet_y_change

   
       
    player(player_x,player_y)
    show_score(text_x,text_y)
    pygame.display.update()

