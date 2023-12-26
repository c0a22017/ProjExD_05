import pygame
from pygame import mixer
import random
import math

pygame.init()

# 背景の定義
background = pygame.image.load('background.png')

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Invaders Game')

# Player
playerImg = pygame.image.load('player.png')
playerX, playerY = 370, 480
playerX_change = 0

# Enemy
enemyImg = pygame.image.load('enemy.png')
enemyX = random.randint(0, 736)
enemyY = random.randint(50, 150)
enemyX_change, enemyY_change = 4, 40

# Enemy Bullet
enemy_bulletImg = pygame.image.load('enemy_bullet.png')
enemy_bulletX, enemy_bulletY = 0, 0
enemy_bulletX_change, enemy_bulletY_change = 0, 5
enemy_bullet_state = 'ready'

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX, bulletY = 0, 480
bulletX_change, bulletY_change = 0, 10
bullet_state = 'ready'

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


def fire_enemy_bullet(x, y):
    global enemy_bullet_state
    enemy_bullet_state = 'fire'
    screen.blit(enemy_bulletImg, (x + 16, y + 10))


def isCollision(x1, y1, x2, y2):
    distance = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
    if distance < 27:
        return True
    else:
        return False

###当たり判定
def isPlayerHit(playerX, playerY, enemy_bulletX, enemy_bulletY):
    distance = math.sqrt(math.pow(playerX - enemy_bulletX, 2) + math.pow(playerY - enemy_bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


running = True
while running:
    screen.fill((0, 0, 0))
    # 背景を実装
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3.0
            if event.key == pygame.K_RIGHT:
                playerX_change = 3.0
            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Player
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy
    if enemyY > 440:
        break
    enemyX += enemyX_change
    if enemyX <= 0:  # 左端に来たら
        enemyX_change = 4
        enemyY += enemyY_change
    elif enemyX >= 736:  # 右端に来たら
        enemyX_change = -4
        enemyY += enemyY_change

    # Enemy Bullet Movementの追加
    if enemy_bullet_state is 'ready':
        enemy_bulletX = enemyX
        enemy_bulletY = enemyY
        enemy_bullet_state = 'fire'

    if enemy_bulletY >= 600:
        enemy_bullet_state = 'ready'

    if enemy_bullet_state is 'fire':
        fire_enemy_bullet(enemy_bulletX, enemy_bulletY)
        enemy_bulletY += enemy_bulletY_change

    # Bullet Movementの追加
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'

    if bullet_state is 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Check collisions
    collision_enemy = isCollision(enemyX, enemyY, bulletX, bulletY)
    if collision_enemy:
        bulletY = 480
        bullet_state = 'ready'
        score_value += 1
        enemyX = random.randint(0, 736)
        enemyY = random.randint(50, 150)

    #当たり判定の追加
    collision_player = isPlayerHit(playerX, playerY, enemy_bulletX, enemy_bulletY)
    if collision_player:
        print("Game Over")
        running = False

    # Score
    font = pygame.font.SysFont(None, 32)  # フォントの作成　Noneはデフォルトのfreesansbold.ttf
    score = font.render(f"Score : {str(score_value)}", True, (255, 255, 255))  # テキストを描画したSurfaceの作成
    screen.blit(score, (20, 50))

    player(playerX, playerY)
    enemy(enemyX, enemyY)

    pygame.display.update()
