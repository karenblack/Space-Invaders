# Author: Karen Black
# Date: 8/19/2020
# Description: Single-player python implementation of the arcade game Space Invaders. Graphics implemented in Pygame.
#              Object: Move your ship to shoot enemy aliens. Don't let aliens get too close or the game is over.
#                      Earn points for each enemy you shoot.
#              Icons by: https://www.flaticon.com/authors/smashicons
#

import pygame
import random
import math
from pygame import mixer

# initialize pygame to use methods
pygame.init()

# Create a display screen
screen_width = 800                  # x-axis
screen_height = 600                 # y-axis
screen = pygame.display.set_mode((screen_width, screen_height))

# background
background = pygame.image.load('background.png')

# background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

#Colors
black = (0, 0, 0)
white = (255, 255, 255)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')             # load the icon for the player
playerX = 370                                           # initial x location for icon
playerY = 480                                           # initial y location for the player
playerX_change = 0                                      # initialize variable for keystrokes movements

# Enemies - initialize empty lists to store multiple enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 5

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))           # load the icon for the enemy
    enemyX.append(random.randint(0, 735))                     # initial x location for enemy
    enemyY.append(random.randint(50, 150))                    # initial y location for the enemy
    enemyX_change.append(4)                                   # initialize variable for movement change in x direction
    enemyY_change.append(40)                                  # initialize variable for movement change in y direction

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0                                         # initialize bulletX as 0
bulletY = 480                                       # initialize at same height as spaceship
bulletY_change = 15
bullet_state = "ready"                              # ready - can't see bullet on screen, 'fire' bullet is moving

# Score
score_value = 0                                     # initialize score of 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game Over test
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x,y):
    """Accepts as parameters x and y coordinates to display text. Renders text and then draws (blit) to screen."""
    score = font.render('Score : ' + str(score_value), True, white)
    screen.blit(score, (x, y))

def game_over_text():
    """Accepts no parameters. Renders and draws text for Game Over."""
    over_text = over_font.render('GAME OVER', True, white)
    screen.blit(over_text, (200, 250))

def player(x,y):
    """Player function that accepts parameters x and y that represent x and y coordinates on the screen. Draws
    player icon (blit) on the screen at the indicated x and y location"""
    screen.blit(playerImg, (x, y))

def enemy(x,y, i):
    """Enemy function that accepts parameters x and y that represent x and y coordinates on the screen. Draws
    enemy icon (blit) on the screen at the indicated x and y location"""
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    """Accepts as parameters the x and y coordinates of the spaceship. Accesses bullet_state variable as global
    variable. Changes bullet_state from ready to fire and draws bullet on the screen at indicated coordinates."""
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16, y+10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    """Accepts x and y coordinates for the enemy and bullet. Calculates the distance between enemy and bullet.
     Determines if a collision between the two has occurred."""
    distance = math.sqrt(math.pow(enemyX-bulletX, 2) + math.pow(enemyY-bulletY, 2))
    if distance < 27:
        return True
    else:
        return False

# Game Loop, while loop to keep game going and game screen open
running = True
while running:

    screen.fill(black)                             # fill screen background color
    screen.blit(background, (0, 0))                # add background image with location in upper left

    # for loop to get events and to change to Quit when close program
    for event in pygame.event.get():               # for loop through all events happening in game
        if event.type == pygame.QUIT:              # if close button pressed, then exit while loop, exit game
            running = False

        # Check if keys are pressed
        if event.type == pygame.KEYDOWN:           # check if key pressed in 'events' list
            if event.key == pygame.K_LEFT:         # check if key is left arrow key
                playerX_change = -5                # move player to left
            if event.key == pygame.K_RIGHT:        # check if key is right arrow key
                playerX_change = 5                 # move player to the right
            if event.key == pygame.K_SPACE:        # check if space key pressed to fire bullet
                if bullet_state == 'ready':        # can only fire if bullet state is 'ready'
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:             # check if key is let up, if so stop player movement
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # player icon movement within boundaries of screen
    playerX += playerX_change                      # adjusts player location on screen if keystrokes are pressed
    if playerX <= 0:                               # if player moved off the right side of screen
        playerX = 0                                # just keep location at 0
    elif playerX >= 736:                           # if player moves off left of screen (800-64(pixels of image))
        playerX = 735

    # Bullet Movement
    if bulletY <= 0:                               # if bullet goes off screen, reset it
        bulletY = 480
        bullet_state = 'ready'
    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # enemy movement within boundaries of screen
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 400:
            for j in range(num_of_enemies):             # move all enemies together off the screen
                enemyY[j] = 2000
            game_over_text()                            # display game over text
            break                                       # break the loop

        # Screen Boundaries
        enemyX[i] += enemyX_change[i]                   # adjusts enemy location on screen
        if enemyX[i] <= 0:                              # if enemy goes to right edge of screen
            enemyX_change[i] = 4                        # move in left direction
            enemyY[i] += enemyY_change[i]               # move down
        elif enemyX[i] >= 736:                          # if enemy moves to left edge of screen
            enemyX_change[i] = -4                       # move in opposite direction
            enemyY[i] += enemyY_change[i]               # move down

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)     # check if there is a collision
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 480                                                   # if collision, reset the bullet
            bullet_state = 'ready'
            score_value += 1                                                # increase the score
            enemyX[i] = random.randint(0, 735)                              # respawn the enemy
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    player(playerX, playerY)                         # run player function to draw player on screen at starting coord
    show_score(textX, textY)
    pygame.display.update()                          # need update to reflect the 'changes' on the screen
