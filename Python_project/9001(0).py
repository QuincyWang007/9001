import pygame
import sys
import random

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jotaro Level")
clock = pygame.time.Clock()
FPS = 60

# 摄像头
camera_x = 0
LEVEL_WIDTH = 8000

# 加载图片资源
Jotaro_img = pygame.image.load("assets/Jotaro.png").convert_alpha()
Jotaro_img = pygame.transform.scale(Jotaro_img, (50, 50))

coin_img = pygame.image.load("assets/coin.png").convert_alpha()
coin_img = pygame.transform.scale(coin_img, (30, 30))

enemy_img = pygame.image.load("assets/Dio.png").convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (50, 50))

plat_img = pygame.image.load("assets/platform.png").convert_alpha()
plat_img = pygame.transform.scale(plat_img, (100, 20))

ground_img = pygame.image.load("assets/ground.png").convert_alpha()
ground_img = pygame.transform.scale(ground_img, (100, 30))

flag_img = pygame.image.load("assets/Joseph.png").convert_alpha()
flag_img = pygame.transform.scale(flag_img, (100, 100))

star_img = pygame.image.load("assets/StarPlatinum.png").convert_alpha()
star_img = pygame.transform.scale(star_img, (50, 50))

# 字体
font = pygame.font.SysFont(None, 32)

# 玩家
player = pygame.Rect(100, 500, 50, 50)
vel_x = 0
vel_y = 0
speed = 5
gravity = 1
jump_force = -15
jump_count = 0
max_jumps = 2

# 地面/平台/金币/敌人/终点
ground = pygame.Rect(0, 570, LEVEL_WIDTH, 8000)
# LEVEL_WIDTH = max([plat.x + plat.width for plat in platforms] + [flag.x + flag.width, 4000])
platforms = [
    pygame.Rect(400, 450, 100, 20),
    pygame.Rect(800, 400, 100, 20),
    pygame.Rect(1200, 350, 100, 20),
    pygame.Rect(1600, 300, 100, 20),
    pygame.Rect(1900, 400, 120, 20),
    pygame.Rect(2200, 350, 150, 20),
    pygame.Rect(2500, 300, 150, 20),
    pygame.Rect(2800, 250, 100, 20),
    pygame.Rect(2300, 300, 100, 20),
    pygame.Rect(2400, 250, 100, 20),
    pygame.Rect(2600, 400, 100, 20),
    pygame.Rect(2800, 250, 100, 20),
    pygame.Rect(3100, 300, 100, 20),
    pygame.Rect(3400, 150, 100, 20),
    pygame.Rect(3500, 200, 100, 20),
    pygame.Rect(3600, 250, 100, 20),
    pygame.Rect(3700, 300, 100, 20),
    pygame.Rect(3800, 250, 100, 20),
    pygame.Rect(3900, 250, 100, 20),
    pygame.Rect(4100, 300, 100, 20),
    pygame.Rect(4200, 300, 100, 20),
    pygame.Rect(5000, 300, 100, 20),
    pygame.Rect(5200, 100, 100, 20),
    pygame.Rect(5300, 200, 100, 20),
    pygame.Rect(5600, 300, 100, 20),
    pygame.Rect(5700, 400, 100, 20),
    pygame.Rect(6100, 500, 100, 20),
    pygame.Rect(6200, 100, 100, 20),
    pygame.Rect(6300, 250, 100, 20),
    pygame.Rect(6400, 330, 100, 20),
    pygame.Rect(6500, 320, 100, 20),
    pygame.Rect(6600, 100, 100, 20),
    pygame.Rect(6700, 200, 100, 20),
    pygame.Rect(6800, 400, 100, 20),
    pygame.Rect(6900, 100, 100, 20),
    pygame.Rect(7100, 300, 100, 20),
    pygame.Rect(7200, 100, 100, 20),
]
coins = []
coin_width = 30
coin_height = 30

coins = []
coin_collected = []
coin_width = 30
coin_height = 30

for plat in platforms:
    if random.random() < 0.5:  # ✅ 50% 概率放置一个金币
        coin_x = plat.x + (plat.width - coin_width) // 2
        coin_y = plat.y - coin_height
        coins.append(pygame.Rect(coin_x, coin_y, coin_width, coin_height))
        coin_collected.append(False)


enemies = [
    {"rect": pygame.Rect(1000, 520, 50, 50), "dir": -1, "range": (900, 1100),"see_range": 200,   # 视野范围
"chase_speed": 4},
    {"rect": pygame.Rect(1700, 520, 50, 50), "dir": -1, "range": (1650, 1800),"see_range": 200,   # 视野范围
"chase_speed": 4},
    {"rect": pygame.Rect(2000, 520, 50, 50), "dir": -1, "range": (1950, 2100),"see_range": 200,   # 视野范围
"chase_speed": 4},
    {"rect": pygame.Rect(2600, 520, 50, 50), "dir": -1, "range": (2550, 2700),"see_range": 200,   # 视野范围
"chase_speed": 4},
    {"rect": pygame.Rect(2800, 520, 50, 50), "dir": -1, "range": (2750, 2900),"see_range": 200,   # 视野范围
"chase_speed": 4},
    {"rect": pygame.Rect(3100, 520, 50, 50), "dir": -1, "range": (3050, 3200),"see_range": 200,   # 视野范围
"chase_speed": 4},
    {"rect": pygame.Rect(3400, 520, 50, 50), "dir": -1, "range": (3350, 3500),"see_range": 200,   # 视野范围
"chase_speed": 4},
    {"rect": pygame.Rect(3500, 520, 50, 50), "dir": -1, "range": (3450, 3600),"see_range": 200,   # 视野范围
"chase_speed": 4},
    {"rect": pygame.Rect(1000, 520, 50, 50), "dir": -1, "range": (900, 1100),"see_range": 200,   # 视野范围
"chase_speed": 4},
    {"rect": pygame.Rect(1700, 520, 50, 50), "dir": -1, "range": (1650, 1800),"see_range": 200,   # 视野范围
"chase_speed": 4},
    {"rect": pygame.Rect(2000, 520, 50, 50), "dir": -1, "range": (1950, 2100),"see_range": 200,   # 视野范围
"chase_speed": 4},
    {"rect": pygame.Rect(2600, 520, 50, 50), "dir": -1, "range": (2550, 2700),"see_range": 200,   # 视野范围
"chase_speed": 4},
    {"rect": pygame.Rect(2800, 520, 50, 50), "dir": -1, "range": (2750, 2900),"see_range": 200,   # 视野范围
"chase_speed": 4},
    {"rect": pygame.Rect(3100, 520, 40, 40), "dir": -1, "range": (3050, 3200),"see_range": 200,   # 视野范围
"chase_speed": 4},
    {"rect": pygame.Rect(4000, 520, 50, 50), "dir": -1, "range": (3950, 4100),"see_range": 200,   # 视野范围
"chase_speed": 4},
    {"rect": pygame.Rect(4500, 520, 50, 50), "dir": -1, "range": (4400, 4550),"see_range": 200,   # 视野范围
"chase_speed": 4},
    {"rect": pygame.Rect(5000, 520, 50, 50), "dir": -1, "range": (4900, 5100),"see_range": 200,   # 视野范围
"chase_speed": 4},
    {"rect": pygame.Rect(5200, 520, 50, 50), "dir": -1, "range": (5150, 5300),"see_range": 200,   # 视野范围
"chase_speed": 4},
    {"rect": pygame.Rect(5800, 520, 50, 50), "dir": -1, "range": (5700, 5900),"see_range": 200,   # 视野范围
"chase_speed": 4},
    {"rect": pygame.Rect(6000, 520, 50, 50), "dir": -1, "range": (5950, 6100),"see_range": 200,   # 视野范围
"chase_speed": 4},
    {"rect": pygame.Rect(6400, 520, 50, 50), "dir": -1, "range": (6300, 6450),"see_range": 200,   # 视野范围
"chase_speed": 4},
    {"rect": pygame.Rect(6800, 520, 50, 50), "dir": -1, "range": (6750, 6900),"see_range": 200,   # 视野范围
"chase_speed": 4},
    {"rect": pygame.Rect(7000, 520, 50, 50), "dir": -1, "range": (6950, 7100),"see_range": 200,   # 视野范围
"chase_speed": 4},
    {"rect": pygame.Rect(7500, 520, 50, 50), "dir": -1, "range": (7450, 7600),"see_range": 200,   # 视野范围
"chase_speed": 4},
]
enemy_dirs = [-1] * len(enemies)

flag = pygame.Rect(7800, 470, 50, 100)

# 分数
score = 0
win = False

# 总时间（秒）
total_time = 120
start_ticks = pygame.time.get_ticks()

star = pygame.Rect(1200, 300, 30, 30)
star_timer = 0
STAR_DURATION = 5000  # milliseconds
has_star = False
show_star_text = False
star_text_timer = 0

space_last = False
game_over = False
running = True
# 游戏主循环
while running:
    dt = clock.tick(FPS) / 1000
    screen.fill((135, 206, 235))  # 天蓝背景

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 控制输入
    keys = pygame.key.get_pressed()
    vel_x = 0
    if keys[pygame.K_LEFT]:
        vel_x = -speed
    if keys[pygame.K_RIGHT]:
        vel_x = speed
    space_now = keys[pygame.K_SPACE]
    if space_now and not space_last:
        if jump_count < max_jumps:
            vel_y = jump_force
            jump_count += 1
    space_last = space_now

    seconds_passed = (pygame.time.get_ticks() - start_ticks) // 1000
    time_left = max(0, total_time - seconds_passed)

    time_text = font.render(f"Time: {time_left}s", True, (0, 0, 0))
    screen.blit(time_text, (WIDTH - 150, 10))
    color = (255, 0, 0) if time_left <= 10 else (0, 0, 0)
    time_text = font.render(f"Time: {time_left}s", True, color)

    if time_left <= 0:
        game_over = True

    # 更新位置
    vel_y += gravity
    player.x += vel_x
    player.y += vel_y

    # 摄像头跟随
    camera_x = max(0, min(player.centerx - WIDTH // 2, LEVEL_WIDTH - WIDTH))

    # 碰撞检测
    if player.colliderect(ground):
        player.bottom = ground.top
        vel_y = 0
        jump_count = 0

    for plat in platforms:
        if player.colliderect(plat) and vel_y >= 0:
            player.bottom = plat.top
            vel_y = 0
            jump_count = 0

    # 敌人移动
    frame_count = 0
    for enemy in enemies:
        if frame_count % 10 < 6:  # 每10帧闪4帧
            screen.blit(enemy_img, (enemy["rect"].x - camera_x, enemy["rect"].y))

        # 碰撞检测
        if player.colliderect(enemy["rect"]):
            game_over = True

    player_center_x = player.centerx

    for enemy in enemies:
        # 是否看到 Jotaro
        if abs(player_center_x - enemy["rect"].centerx) < enemy.get("see_range", 200):
            move_speed = enemy.get("chase_speed", 4)
            if player_center_x > enemy["rect"].centerx:
                enemy["rect"].x += move_speed
            else:
                enemy["rect"].x -= move_speed
        else:
            # 常规来回移动
            enemy["rect"].x += enemy["dir"] * 2
            if enemy["rect"].left < enemy["range"][0] or enemy["rect"].right > enemy["range"][1]:
                enemy["dir"] *= -1

    for enemy in enemies:
        screen.blit(enemy_img, (enemy["rect"].x - camera_x, enemy["rect"].y))

    if game_over:
        screen.fill((0, 0, 255))  # 蓝背景
        over_text = font.render("Game Over", True, (255, 0, 0))
        title_text = font.render("Jotaro vs Dio - Thanks for playing!", True, (255, 255, 255))
        screen.blit(over_text, (WIDTH // 2 - 80, HEIGHT // 2 - 20))
        screen.blit(title_text, (WIDTH // 2 - 200, HEIGHT // 2 + 20))
        pygame.display.flip()
        pygame.time.delay(3000)  # 停留 3 秒
        pygame.quit()
        sys.exit()

    # 收集 StarPlatinum
    if player.colliderect(star) and not has_star:
        has_star = True
        speed = 6
        player.inflate_ip(10, 10)
        show_star_text = True
        star_text_timer = pygame.time.get_ticks()
        can_time_stop = True  # ✅ 吃到白金之星后解锁时停


    if show_star_text and pygame.time.get_ticks() - star_text_timer > 3000:
        show_star_text = False

    if show_star_text:
        star_text = font.render("StarPlatinum Activated!", True, (255, 255, 0))
        screen.blit(star_text, (WIDTH // 2 - 100, 10))

    if not has_star:
        screen.blit(star_img, (star.x - camera_x, star.y))

    if has_star:
        star_text = font.render("StarPlatinum Activated!", True, (255, 255, 0))
        screen.blit(star_text, (WIDTH // 2 - 100, 10))



    # 收集金币
    for i, coin in enumerate(coins):
        if player.colliderect(coin) and not coin_collected[i]:
            coin_collected[i] = True
            score += 1

    # 判断胜利
    if player.colliderect(flag):
        win = True

    # 绘制地面与平台
    for x in range(0, LEVEL_WIDTH, 100):
        screen.blit(ground_img, (x - camera_x, ground.y))

    for plat in platforms:
        screen.blit(plat_img, (plat.x - camera_x, plat.y))

    # 绘制金币
    for i, coin in enumerate(coins):
        if not coin_collected[i]:
            screen.blit(coin_img, (coin.x - camera_x, coin.y))


    # 终点旗帜
    screen.blit(flag_img, (flag.x - camera_x, flag.y))

    # 玩家
    screen.blit(Jotaro_img, (player.x - camera_x, player.y))

    # UI 分数显示
    score_text = font.render(f"Coins: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    if win:
        win_text = font.render("You Win!", True, (255, 0, 0))
        screen.blit(win_text, (WIDTH // 2 - 50, 50))

    pygame.display.flip()

pygame.quit()
sys.exit()