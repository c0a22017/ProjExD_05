import pygame
from pygame import mixer
import random
import math

pygame.init()

mixer.init()

# 背景の定義
background = pygame.image.load('ex05/background.png')

screen = pygame.display.set_mode((800, 600))
# screen.fill((150, 150, 150))
pygame.display.set_caption('ex05/Invaders Game')

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
bulletX_change, bulletY_change = 0, 9#3
bullet_state = 'ready'
#add
multishot = False  # 散弾が放たれている状態か否か
# Enemy Bullet
enemy_bulletImg = pygame.image.load('ex05/enemy_bullet.png')
enemy_bulletX, enemy_bulletY = 0, 0
enemy_bulletX_change, enemy_bulletY_change = 0, 2
enemy_bullet_state = 'ready'

# Score
score_value = 0
#クリア条件
font_1 = pygame.font.SysFont(None, 32) # フォントの作成
clear_font = pygame.font.SysFont(None, 64) # **ゲームクリアメッセージ用のフォントを作成**

def sound_beam():
    pygame.mixer.init() #初期化
    pygame.mixer.music.load("ex05/laser.wav") #読み込み
    pygame.mixer.music.play(1) #再生

    

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
    
def draw_shield(x, y, radius):
    if radius > 0:
        pygame.draw.circle(screen, (0, 0, 255), (x, y), radius)

def isCollision(enemyX, enemyY, bulletX, bulletY):
    global shield_radius, shield_x, shield_y, bullet_state

    if shield_radius > 0:
        # シールドがアクティブの場合
        distance_to_shield = math.sqrt(math.pow(shield_x - bulletX, 2) + math.pow(shield_y - bulletY, 2))
        if distance_to_shield < shield_radius:
            # シールドに当たった場合
            bullet_state = 'ready'  # 弾をリセット
            return False
        # シールドに当たらない場合
        distance_to_enemy = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
        if distance_to_enemy < 27:
            return False
        # シールドに当たった場合、敵の弾も無効にする
        distance_to_enemy_bullet = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
        if distance_to_enemy_bullet < 50:
            return False
            # シールドに当たった場合、敵の弾も無効にする
            # bullet_state = 'ready'
            # return False
    # シールドがアクティブでない場合、通常の当たり判定を行う
    distance_to_enemy = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance_to_enemy < 27:
        return True

    return False
#add
class Multishot:
    def __init__(self,playerX, playerY, power: int):
        """
        引数
        playerX, playerY:自機のX座標とY座標
        power:ゲージの溜まり具合、散弾で出る弾の数
        """
        self.playerX, self.playerY = playerX, playerY
        self.power = power
        self.image = pygame.image.load('ex05/bullet.png')
        self.bullets_locate = [[self.playerX, self.playerY]]*power   # 弾の現在地のリスト
        self.bullet_speed = bulletY_change  # 弾の進むスピード
        self.is_arrive = [False] * power  # 弾が存在するか否かのリスト

    def summon_bullets(self):
        """
        散弾を生成するための関数
        """
        self.lst = []  # 角度の違う弾丸のリスト
        self.angles = []  # 角度のリスト
        cnt = 0
        try:
            for i in range(-400, 410, 800//(self.power-1)):  # ゲージが2以上の場合、散弾発動
                self.lst.append(pygame.transform.rotozoom(self.image, i/10, 1.0))
                self.angles.append(i/10)
                self.is_arrive[cnt] = True
                cnt += 1
        except ZeroDivisionError:  # ゲージが1の場合、正面に飛ぶようにする
            self.lst.append(pygame.transform.rotozoom(self.image, 0, 1.0))
            self.angles.append(0)
            self.is_arrive[cnt] = True
            
    def move_bullets(self):
        """
        散弾を動かすための関数
        """
        for n, img in enumerate(self.lst):  # 存在するすべての弾に対して
            if self.is_arrive[n]:
                locx, locy = self.bullets_locate[n]
                screen.blit(img, (self.bullets_locate[n]))  # 弾の描画
                locx += math.cos(math.radians(self.angles[n]+90)) *self.bullet_speed  # 弾の移動
                locy -= math.sin(math.radians(self.angles[n]+90)) *self.bullet_speed
                self.bullets_locate[n] = [locx, locy]

    def kill_bullets(self):
        """
        散弾を消去するための関数
        """
        global enemyX, enemyY, score_value
        enemy = "arrive"  # 敵が生存しているか否か(複数弾同時ヒットを避けるため)
        for n, b in enumerate(self.bullets_locate):  # 全ての弾に対して
            if enemy == "arrive":  # 敵が生存しているなら
                collision = isCollision(enemyX, enemyY, b[0], b[1])
                if collision:  # 敵と衝突したなら、スコアを+1して、弾と敵をリセットする
                    score_value += 1
                    enemyX = random.randint(0, 736)
                    enemyY = random.randint(50, 150)
                    self.is_arrive[n] = False
                    enemy = "dead"  # 敵を生存していない状態にする
            if b[1] < 0:  # 画面外に出たら弾消失
                self.is_arrive[n] = False

    # シールドがアクティブでない場合、通常の当たり判定を行う
    # distance_to_enemy = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    # if distance_to_enemy < 27:
    #     return True

    # return False
    # distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    # if distance < 27:
    #     return True
    # else:
    #     return False
    
###当たり判定
def isPlayerHit(playerX, playerY, enemy_bulletX, enemy_bulletY):
    distance = math.sqrt(math.pow(playerX - enemy_bulletX, 2) + math.pow(playerY - enemy_bulletY, 2))
    if distance < 27:
        return True
    else:
        return False

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

# 変数の初期化
gauge_value = 0
gauge_max = 5
# ...（他の初期化処理）
shield_timer = 0  # shield_timer 変数を追加
shield_x = 0  # shield_x 変数を追加
shield_y = 0  # shield_y 変数を追加
shield_radius = 0  # shield_radius 変数を追加
last_time = pygame.time.get_ticks()


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
                playerX_change = -7.0#-1.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 7.0#1.5
            if event.key == pygame.K_SPACE:
                if event.key == pygame.K_SPACE:
                    if bullet_state == 'ready':
                        bulletX = playerX
                        fire_bullet(bulletX, playerY)
                        sound_beam()

            #capslockを押すとゲージが一増える
            if event.key == pygame.K_CAPSLOCK and gauge_value >= 2:
                gauge_value  -= 2
                gauge_max += 1
                if gauge_max >= 15:
                    gauge_max -=1
                    gauge_value += 2
                    
            if event.key == pygame.K_RSHIFT and gauge_value >= 1 and not multishot:  # ゲージが1以上溜まっている時にRSHIFTが押されたなら
                mshot = Multishot(playerX, playerY, gauge_value)  # Multishotインスタンス生成
                mshot.summon_bullets()
                multishot = True  # 散弾状態へ移行
                gauge_value = 0  # ゲージをすべて消費
            
            #なくてもいい        
            elif event.key == pygame.K_CAPSLOCK and gauge_value < 2:
                event_text = clear_font.render("It's not the time yet...", True, (255,255,0)) # クリアメッセージを作成
                screen.blit(event_text, (200,250)) # 画面中央に表示
                pygame.display.update()
                pygame.time.wait(500) # 5秒間待つ

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
    if enemyX <= 0: #左端に来たら
        enemyX_change = 2#4
        # enemyY += enemyY_change
    elif enemyX >=736: #右端に来たら
        enemyX_change = -2#-4
        # enemyY += enemyY_change
        
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
        
    # Multishot
    if multishot:  # 散弾についての処理
        mshot.move_bullets()
        mshot.kill_bullets()
        if True not in mshot.is_arrive:  # 存在する弾がなくなったら、multishot状態から抜ける
            multishot = False

        
    # シールドの作成
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LSHIFT and gauge_value >= 1:
            gauge_value -= 1
            shield_x = playerX + 31
            shield_y = playerY + 15
            shield_radius = 50
            shield_timer = pygame.time.get_ticks() 
            # シールドに弾が当たったら、弾を無効にする
        def isCollision(enemyX, enemyY, bulletX, bulletY):
            global shield_radius, shield_x, shield_y, bullet_state

            if shield_radius > 0:
                # シールドがアクティブの場合
                distance_to_shield = math.sqrt(math.pow(shield_x - bulletX, 2) + math.pow(shield_y - bulletY, 2))
                if distance_to_shield < shield_radius:
                    # シールドに当たった場合
                    bullet_state = 'ready'  # 弾をリセット
                    return False
                 # シールドに当たらない場合
                distance_to_enemy = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
                if distance_to_enemy < 27:
                    return True
                # シールドに当たった場合、敵の弾も無効にする
                distance_to_enemy_bullet = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
                if distance_to_enemy_bullet < 50:
                    bullet_state = 'ready'
                    return False
            # シールドがアクティブでない場合、通常の当たり判定を行う
            distance_to_enemy = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
            if distance_to_enemy < 27:
                return True

            return False

            
    # シールドの描画
    draw_shield(shield_x, shield_y, shield_radius)
                        
    # シールドの更新
    if shield_timer > 0:
        elapsed_time = pygame.time.get_ticks() - shield_timer
        if elapsed_time < gauge_max * 1000:
            shield_x = playerX + 31
            shield_y = playerY + 15
            shield_radius = 50
        else:
            shield_timer = 0
            shield_radius = 0

    collision = isCollision(enemyX, enemyY, bulletX, bulletY)
    if collision:
        bulletY = 480
        bullet_state = 'ready'
        score_value += 1

        # ゲージの描画を、当たり判定でする。
        if gauge_value<gauge_max:
            gauge_value += 1 # ゲージの値を1増加する。
        # if gauge_value >= gauge_max:
        #     gauge_value=gauge_max
        
        enemyX = random.randint(0, 736)
        enemyY = random.randint(50, 150)
        
    #当たり判定の追加
    collision_player = isPlayerHit(playerX, playerY, enemy_bulletX, enemy_bulletY)
    if collision_player:
        print("Game Over")
        game_over_time = pygame.time.get_ticks()
        
        while pygame.time.get_ticks() - game_over_time < 3000:  # Display "Game Over" for 4000 milliseconds (4 seconds)
            # Display "Game Over" message here
            screen.fill((0, 0, 0))  # Clear the screen
            game_over_text = clear_font.render("Game Over", True, (255, 0, 0))
            screen.blit(game_over_text, (290, 270))  # Display "Game Over" message at a specific position
            pygame.display.update()
            running = False

    #ゲージの最大値を文字として表示
    if gauge_max == 15:
            text_gauge = font_gauge.render("GAUGE MAX", True, (255,0,0))   # 描画する文字列の設定
            screen.blit(text_gauge, [20, 150])# 文字列の表示位置
           

    # Bullet Movement
    if bulletY <=0:
        bulletY = 480
        bullet_state = 'ready'

    if bullet_state is 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change  
        # シールドしてる時も打てるようにして
        # if collision(enemyX, enemyY, bulletX, bulletY):
        #     bulletY = 480
        #     bullet_state = 'fire'
        #     score_value += 1

        # シールドに当たった場合、敵の弾も無効にする
        # if collision(enemyX, enemyY, enemy_bulletX, enemy_bulletY):
        #     enemy_bullet_state = 'ready'

    # Score
    font = pygame.font.SysFont(None, 32) # フォントの作成　Noneはデフォルトのfreesansbold.ttf
    score = font.render(f"Score : {str(score_value)}", True, (255,255,255)) # テキストを描画したSurfaceの作成
    screen.blit(score, (20,50))

    # ゲームクリア
    """
    if score_value >= 3:
        clear_text = clear_font.render("congratulations!", True, (255,255,255)) # **クリアメッセージを作成**
        screen.blit(clear_text, (200,250)) # 画面中央に表示
        pygame.display.update()
        pygame.time.wait(5000) # 5秒間待つ
        break
"""
    # ゲームクリア
    if score_value >= 30:
        clear_text_1 = clear_font.render("congratulations...", True, (255,255,0)) # クリアメッセージを作成

        text_height = clear_text_1.get_height()
        start_y = 600  # テキストが画面下から始まるように設定
        speed = 8  # テキストが移動する速度

        while start_y + text_height > 0:  # テキストが画面上に完全に消えるまでループ
            screen.fill((0, 0, 0))  # 画面を黒で塗りつぶす
            screen.blit(clear_text_1, (200, start_y))  # テキストを新しい位置に描画
            pygame.display.update()  # 画面を更新
            start_y -= speed  # テキストのy座標を減らす（上に移動）
            pygame.time.wait(20)  # 一定時間待つ（テキストの移動速度を制御）

        
        break

    # guageの描画
    gauge()

    player(playerX, playerY)
    enemy(enemyX, enemyY)

    pygame.display.update()