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
LEVEL_WIDTH = 10000

# 加载图片资源
Jotaro_img = pygame.image.load("assets/Jotaro.png").convert_alpha()
Jotaro_img = pygame.transform.scale(Jotaro_img, (50, 50))

coin_img = pygame.image.load("assets/coin.png").convert_alpha()
coin_img = pygame.transform.scale(coin_img, (30, 30))

enemy_img = pygame.image.load("assets/Dio.png").convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (40, 40))

plat_img = pygame.image.load("assets/platform.png").convert_alpha()
plat_img = pygame.transform.scale(plat_img, (100, 20))

ground_img = pygame.image.load("assets/ground.png").convert_alpha()
ground_img = pygame.transform.scale(ground_img, (100, 30))

flag_img = pygame.image.load("assets/Joseph.png").convert_alpha()
flag_img = pygame.transform.scale(flag_img, (50, 100))

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

# 平台与金币
platforms = [pygame.Rect(x, y, 100, 20) for x, y in zip(range(400, 8000, 400), [450, 400, 350, 300, 400, 350, 300, 250])]
coins = []
coin_collected = []
for plat in platforms:
    if random.random() < 0.6:
        coin = pygame.Rect(plat.x + 35, plat.y - 30, 30, 30)
        coins.append(coin)
        coin_collected.append(False)

# 敌人
enemies = [
    {"rect": pygame.Rect(x, 540, 40, 40), "dir": -1, "range": (x - 100, x + 100), "see_range": 200, "chase_speed": 4}
    for x in range(1000, 3600, 300)
]

# 终点旗帜
flag = pygame.Rect(9500, 470, 50, 100)

# 白金之星
star = pygame.Rect(1200, 300, 30, 30)
has_star = False
show_star_text = False
star_text_timer = 0

# 分数、状态
score = 0
win = False
game_over = False
space_last = False
frame_count = 0

# 时停
can_time_stop = False
time_stop_active = False
time_stop_start = 0
TIME_STOP_DURATION = 5000

# 时间
total_time = 120
start_ticks = pygame.time.get_ticks()

# 地面
ground = pygame.Rect(0, 570, LEVEL_WIDTH, 100)

# 游戏主循环
running = True
while running:
    frame_count += 1
    dt = clock.tick(FPS) / 1000
    screen.fill((135, 206, 235))

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

    # 启动时停
    if can_time_stop and not time_stop_active and keys[pygame.K_t]:
        time_stop_active = True
        time_stop_start = pygame.time.get_ticks()

    # 解除时停
    if time_stop_active and pygame.time.get_ticks() - time_stop_start > TIME_STOP_DURATION:
        time_stop_active = False

    # 时间流逝
    if not time_stop_active:
        seconds_passed = (pygame.time.get_ticks() - start_ticks) // 1000
        time_left = max(0, total_time - seconds_passed)

    if time_left <= 0:
        game_over = True

    # 玩家移动
    vel_y += gravity
    player.x += vel_x
    player.y += vel_y

    camera_x = max(0, min(player.centerx - WIDTH // 2, LEVEL_WIDTH - WIDTH))

    # 地面与平台碰撞
    if player.colliderect(ground):
        player.bottom = ground.top
        vel_y = 0
        jump_count = 0

    for plat in platforms:
        if player.colliderect(plat) and vel_y >= 0:
            player.bottom = plat.top
            vel_y = 0
            jump_count = 0

    # 敌人逻辑
    if not time_stop_active:
        for enemy in enemies:
            if abs(player.centerx - enemy["rect"].centerx) < enemy["see_range"]:
                dx = enemy["chase_speed"] if player.centerx > enemy["rect"].centerx else -enemy["chase_speed"]
                enemy["rect"].x += dx
            else:
                enemy["rect"].x += enemy["dir"] * 2
                if enemy["rect"].left < enemy["range"][0] or enemy["rect"].right > enemy["range"][1]:
                    enemy["dir"] *= -1

    # 碰撞检测
    for enemy in enemies:
        if player.colliderect(enemy["rect"]):
            game_over = True

    if player.colliderect(star) and not has_star:
        has_star = True
        speed = 6
        can_time_stop = True
        show_star_text = True
        star_text_timer = pygame.time.get_ticks()

    # UI
    if show_star_text and pygame.time.get_ticks() - star_text_timer > 3000:
        show_star_text = False

    if player.colliderect(flag):
        win = True

    for i, coin in enumerate(coins):
        if player.colliderect(coin) and not coin_collected[i]:
            coin_collected[i] = True
            score += 1

    # Game Over
    if game_over:
        screen.fill((0, 0, 255))
        screen.blit(font.render("Game Over", True, (255, 0, 0)), (WIDTH // 2 - 80, HEIGHT // 2 - 20))
        pygame.display.flip()
        pygame.time.delay(3000)
        break

    # 绘图
    for x in range(0, LEVEL_WIDTH, 100):
        screen.blit(ground_img, (x - camera_x, ground.y))
    for plat in platforms:
        screen.blit(plat_img, (plat.x - camera_x, plat.y))
    for i, coin in enumerate(coins):
        if not coin_collected[i]:
            screen.blit(coin_img, (coin.x - camera_x, coin.y))
    for enemy in enemies:
        screen.blit(enemy_img, (enemy["rect"].x - camera_x, enemy["rect"].y))
    if not has_star:
        screen.blit(star_img, (star.x - camera_x, star.y))
    screen.blit(flag_img, (flag.x - camera_x, flag.y))
    screen.blit(Jotaro_img, (player.x - camera_x, player.y))

    screen.blit(font.render(f"Coins: {score}", True, (0, 0, 0)), (10, 10))
    screen.blit(font.render(f"Time: {time_left}s", True, (255, 0, 0) if time_left <= 10 else (0, 0, 0)), (WIDTH - 150, 10))
    if time_stop_active:
        screen.blit(font.render("Time Stop!", True, (0, 0, 0)), (WIDTH // 2 - 60, HEIGHT // 2 - 100))
    if show_star_text:
        screen.blit(font.render("StarPlatinum Activated!", True, (255, 255, 0)), (WIDTH // 2 - 100, 10))
    if win:
        screen.blit(font.render("You Win!", True, (255, 0, 0)), (WIDTH // 2 - 50, 50))

    pygame.display.flip()

pygame.quit()
sys.exit()