import pygame
from pygame import mixer
import random
import math

pygame.init()
mixer.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Invaders Game')

# Player
playerImg = pygame.image.load('ex05/player.png')
playerX, playerY = 370, 480
playerX_change = 0

# Enemy
enemyImg = pygame.image.load('ex05/enemy.png')
enemyX = random.randint(0, 736)
enemyY = random.randint(50, 150)
enemyX_change, enemyY_change = 4, 40

# Bullet
bulletImg = pygame.image.load('ex05/bullet.png')
bulletX, bulletY = 0, 480
bulletX_change, bulletY_change = 0, 3
bullet_state = 'ready'

# Score
score_value = 0

# gauge
gauge_value = 0
gauge_max = 5
font_gauge = pygame.font.Font(None, 40)
font_gauge_power = pygame.font.Font(None, 30)

# Shield
shield_timer = 0
shield_x = 0
shield_y = 0
shield_radius = 0

# Background
background = pygame.image.load('background.png')

# Enemy Bullet
enemy_bulletImg = pygame.image.load('enemy_bullet.png')
enemy_bulletX, enemy_bulletY = 0, 0
enemy_bulletX_change, enemy_bulletY_change = 0, 5
enemy_bullet_state = 'ready'

def sound_beam():
    pygame.mixer.init()
    pygame.mixer.music.load("ex05/laser.wav")
    pygame.mixer.music.play(1)

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y):
    screen.blit(enemyImg, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))

def draw_shield(x, y, radius):
    pygame.draw.circle(screen, (0, 255, 0), (x, y), radius)

def isCollision(x1, y1, x2, y2):
    distance = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
    if distance < 27:
        return True
    else:
        return False

def gauge():
    pygame.draw.rect(screen, (255, 0, 0), [20, 80, gauge_max * 20, 20])
    pygame.draw.rect(screen, (0, 255, 0), [20, 80, gauge_value * 20, 20])
    text_gauge_power = font_gauge_power.render("POWER"+str(gauge_value), True, (0,255,0))
    screen.blit(text_gauge_power, [20, 130])

running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 1.5
            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                    sound_beam()

            if event.key == pygame.K_CAPSLOCK and gauge_value >= 2:
                gauge_value  -= 2
                gauge_max += 1
                if gauge_max >= 15:
                    gauge_max -=1
                    gauge_value += 2

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    enemyX += enemyX_change
    if enemyX <= 0:
        enemyX_change = 4
        enemyY += enemyY_change
    elif enemyX >= 736:
        enemyX_change = -4
        enemyY += enemyY_change

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LSHIFT and gauge_value >= 1:
            gauge_value -= 1
            shield_x = playerX + 31
            shield_y = playerY + 15
            shield_radius = 50
            shield_timer = 0

    if shield_timer > 0:
        shield_timer -= 1
        if shield_timer <= 0:
            shield_x = 0
            shield_y = 0
            shield_radius = 0

    draw_shield(shield_x, shield_y, shield_radius)

    collision = isCollision(enemyX, enemyY, bulletX, bulletY)
    if collision:
        bulletY = 480
        bullet_state = 'ready'
        score_value += 1

        if gauge_value < gauge_max:
            gauge_value += 1
        if gauge_value >= gauge_max:
            gauge_value = gauge_max
        
        enemyX = random.randint(0, 736)
        enemyY = random.randint(50, 150)

    if gauge_max == 15:
        text_gauge = font_gauge.render("GAUGE MAX", True, (255,0,0))
        screen.blit(text_gauge, [20, 150])

    if score_value >= 30:
        clear_text_1 = clear_font.render("congratulations...", True, (255,255,0))

        text_height = clear_text_1.get_height()
        start_y = 600
        speed = 8

        while start_y + text_height > 0:
            screen.fill((0, 0, 0))
            screen.blit(clear_text_1, (200, start_y))
            pygame.display.update()
            start_y -= speed
            pygame.time.wait(20)

        break

    gauge()
    player(playerX, playerY)
    enemy(enemyX, enemyY)

    pygame.display.update()
