import pygame
from pygame import mixer
import random
import math

pygame.init()

screen = pygame.display.set_mode((800, 600))
# screen.fill((150, 150, 150))
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

#ここ
# Shield
shield_radius = 80
shield_color = (218, 12, 95)  # Blue color for the shield
shield_state = 'ready'

# Score
score_value = 0

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y):
    screen.blit(enemyImg, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))
    
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False
    
#ここ
def draw_shield(x, y):
    pygame.draw.circle(screen, shield_color, (x + 33, y), shield_radius)

def isCollision_shield(obj1X, obj1Y, obj2X, obj2Y, obj1_radius, obj2_radius):
    distance = math.sqrt(math.pow(obj1X - obj2X, 2) + math.pow(obj1Y - obj2Y, 2))
    if distance < (obj1_radius + obj2_radius):
        return True
    else:
        return False
    
#test
# gaugeの値設定
gauge_value = 0
gauge_max = 5
font_gauge = pygame.font.Font(None, 40)
font_gauge_power = pygame.font.Font(None, 30)    
"""
gaugeの描画設定
ゲージの増加を表すゲージを緑に設定
ゲージが満たされていない事を表す色を赤に設定
スコアの下あたり表示させる
"""

def gauge():
    pygame.draw.rect(screen, (255, 0, 0), [20, 80, gauge_max * 20, 20])  #　赤のゲージ
    pygame.draw.rect(screen, (0, 255, 0), [20, 80, gauge_value * 20, 20])  # 緑のゲージ
    text_gauge_power = font_gauge_power.render("POWER"+str(gauge_value), True, (0,255,0))   # 描画する文字列の設定
    screen.blit(text_gauge_power, [20, 130])# 文字列の表示位置

running = True
while running:
    screen.fill((0, 0, 0))

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
            #ここ        
            if event.key == pygame.K_s:  # Press 'S' to activate shield
                if shield_state == 'ready':
                    shieldX, shieldY = playerX, playerY
                    shield_state = 'active'
            #test        
            #capslockを押すとゲージが一増える
            if event.key == pygame.K_CAPSLOCK and gauge_value >= 2:
                gauge_value  -= 2
                gauge_max += 1
                if gauge_max >= 15:
                    gauge_max -=1
                    gauge_value += 2   
                         
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    # Player
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    #ここ
    # Shield
    if shield_state == 'active':
        draw_shield(playerX, playerY)


    # Enemy
    if enemyY > 440:
        break
    enemyX += enemyX_change
    if enemyX <= 0: #左端に来たら
        enemyX_change = 1#4 
        enemyY += enemyY_change
    elif enemyX >=736: #右端に来たら
        enemyX_change = -1#-4
        enemyY += enemyY_change
        
    #test    
    collision = isCollision(enemyX, enemyY, bulletX, bulletY)
    if collision:
        bulletY = 480
        bullet_state = 'ready'
        score_value += 1

        # ゲージの描画を、当たり判定でする。
        if gauge_value<gauge_max:
            gauge_value += 1 # ゲージの値を1増加する。
        if gauge_value >= gauge_max:
            gauge_value=gauge_max

    #ここ
    if shield_state == 'active' and isCollision_shield(enemyX, enemyY, playerX, playerY, shield_radius, 32):
        shield_state = 'ready'
        enemyX = random.randint(0, 736)
        enemyY = random.randint(50, 150)

    # Bullet Movement
    if bulletY <=0:
        bulletY = 480
        bullet_state = 'ready'

    if bullet_state is 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change  

    # Score
    font = pygame.font.SysFont(None, 32) # フォントの作成　Noneはデフォルトのfreesansbold.ttf
    score = font.render(f"Score : {str(score_value)}", True, (255,255,255)) # テキストを描画したSurfaceの作成
    screen.blit(score, (20,50))
    
    gauge()

    player(playerX, playerY)
    enemy(enemyX, enemyY)

    pygame.display.update()
