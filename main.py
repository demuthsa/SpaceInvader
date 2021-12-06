import pygame
import random
import math
from pygame import mixer # mixer allows sound to be added

# Initialize the pygame, or code won't work
pygame.init()

# create the screen, set_mode contains the width and the height of screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1) # -1 allows the song to play on loop

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_move = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_move = []
enemyY_move = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 736)) # start and end value, 0 - 800 since that is width of screen, but subtract number of pixels for the picture so it doesn't load off screen
    enemyY.append(random.randint(50, 100))
    enemyX_move.append(3)
    enemyY_move.append(40) # Changes by 40 pixels when enemy hits left or right boundary


# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480 # starts at 480 since that is where the spaceship starts
bulletX_move = 0
bulletY_move = 10 # Changes by 40 pixels when enemy hits left or right boundary
# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
bullet_state = "ready"

# Score and Font
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32) # type of font and size

textX = 10
testY = 10

# Game Over Text
game_over_font = pygame.font.Font('freesansbold.ttf', 64) # type of font and size

def show_score(x,y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250)) # Middle of the screen

# Allows an image to be placed on screen
def player(x, y):
    screen.blit(playerImg, (x, y))
# Allows enemy to be placed on screen
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))
# Allows bullet to be placed on screen
def fire_bullet(x,y):
    global bullet_state # Allows bullet_state to be accessed inside this function
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16, y+10)) # Coordinates allow bullet to be shot from the middle of the spaceship, otherwise shoots off center

def isCollision(enemyX, enemyY, bulletX, bulletY):
    # Distance between two points formula = D = sqrt(x2-x1)^2 + (y2-y1)^2
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY - bulletY, 2))) # pow = power - in this case power of 2
    if distance < 27: # proper distance between bullet and enemy for collision
        return True
    else:
        return False


# Game Loop, Allows the game to run and Register if the window has been closed
running = True
while running:
    # RGB - Red, Green, Blue - values go from 0 to 255
    screen.fill((0, 0, 0))

    # Background Image
    screen.blit(background, (0,0)) # coordinates of where image should appear. (0,0) top left corner

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed, check whether it's right or left
        if event.type == pygame.KEYDOWN: #KEYDOWN registers any key that has been pressed
            if event.key == pygame.K_LEFT:
                playerX_move = -5
            if event.key == pygame.K_RIGHT:
                playerX_move = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    # Get the current x coordinate of the spaceship
                    bulletX = playerX  # Creates a new variable for the bullet so it doesn't follow the spaceship
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP: #KEYUP registers any key that has been released
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_move = 0

    # Player Movement
    playerX += playerX_move

    if playerX <= 0: # Checking for boundaries: Doesn't allow the player to go off the screen
        playerX = 0
    elif playerX >= 736: # 800 - 64 (number of pixels chosen for img) = 736
        playerX = 736 # Checking for boundaries: Doesn't allow the player to go off the screen

    # Enemy Movement
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 440:  # number of pixels the enemy should not reach, same as the spaceship
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_move[i]

        if enemyX[i] <= 0:
            enemyX_move[i] = 3
            enemyY[i] += enemyY_move[i]
        elif enemyX[i] >= 736:  # 800 - 64 (number of pixels chosen for img) = 736
            enemyX_move[i] = -3
            enemyY[i] += enemyY_move[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480 # starts at the spaceship
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY) # starts at the spaceship current coordinate, resets to spaceship at 480
        bulletY -= bulletY_move




    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()