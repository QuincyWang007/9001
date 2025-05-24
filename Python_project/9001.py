import pygame
import sys
import random

pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jotaro Level")
clock = pygame.time.Clock()
FPS = 60
pygame.mixer.music.load("assets/killer_queen.mp3")
pygame.mixer.music.set_volume(1.0)
pygame.mixer.music.play(-1)
the_world_sound = pygame.mixer.Sound("assets/the_world.mp3")
game_over_sound = pygame.mixer.Sound("assets/game_over.mpeg")
victory_sound = pygame.mixer.Sound("assets/victory.mp3")


# 摄像头
camera_x = 0
LEVEL_WIDTH = 8000

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
flag_img = pygame.transform.scale(flag_img, (50, 50))

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
    if random.random() < 0.6:  # ✅ 60% 概率放置一个金币
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

# 白金之星时停
time_stop_active = False
time_stop_start = 0
TIME_STOP_DURATION = 5000  # 5秒
can_time_stop = False    # 可以时停（吃到白金之星）
TIME_STOP_DURATION = 5000
TIME_STOP_COOLDOWN = 8000  # 可选冷却8秒（可删去）
time_stop_active = False
time_stop_start = 0
time_stop_cooldown_ready = True  # 可重复使用控制

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

frame_count = 0

running = True

pause_start = 0
# 游戏主循环
while running:
    frame_count += 1
    dt = clock.tick(FPS) / 1000
    if time_stop_active:
        # 闪屏效果（短暂白屏）
        if pygame.time.get_ticks() - time_stop_start < 300:  # 前0.3秒白屏
            screen.fill((255, 255, 255))  # 白色闪屏
        else:
            screen.fill((180, 180, 180))  # 灰色背景表示时间冻结
    else:
        screen.fill((135, 206, 235))  # 正常天蓝色背景

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

    if not time_stop_active:
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

    # 敌人更新（只有非时停时才移动）
    if not time_stop_active:
        for enemy in enemies:
            # 更新敌人位置
            if abs(player.centerx - enemy["rect"].centerx) < enemy.get("see_range", 200):
                move_speed = enemy.get("chase_speed", 4)
                if player.centerx > enemy["rect"].centerx:
                    enemy["rect"].x += move_speed
                else:
                    enemy["rect"].x -= move_speed
            else:
                enemy["rect"].x += enemy["dir"] * 2
                if enemy["rect"].left < enemy["range"][0] or enemy["rect"].right > enemy["range"][1]:
                    enemy["dir"] *= -1

    # 敌人绘制（时停状态下只绘制，不移动）
    for enemy in enemies:
        if not time_stop_active and frame_count % 10 < 6:
            screen.blit(enemy_img, (enemy["rect"].x - camera_x, enemy["rect"].y))
        elif time_stop_active:
            screen.blit(enemy_img, (enemy["rect"].x - camera_x, enemy["rect"].y))

    # ✅ 敌人与玩家的碰撞检测
    for enemy in enemies:
        if player.colliderect(enemy["rect"]):
            game_over = True

     # 时停时敌人动作
    if not time_stop_active:
        for enemy in enemies:
            screen.blit(enemy_img, (enemy["rect"].x - camera_x, enemy["rect"].y))

    if game_over:
        pygame.mixer.music.stop()
        game_over_sound.play()  # 播放 Game Over 音效
        screen.fill((0, 0, 255))  # 蓝背景
        over_text = font.render("Game Over", True, (255, 0, 0))
        title_text = font.render("Jotaro vs Dio - Thanks for playing!", True, (255, 255, 255))
        screen.blit(over_text, (WIDTH // 2 - 80, HEIGHT // 2 - 20))
        screen.blit(title_text, (WIDTH // 2 - 200, HEIGHT // 2 + 20))
        pygame.display.flip()
        pygame.time.delay(7000)  # 停留 3 秒
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

    # 时停

    if can_time_stop and not time_stop_active and keys[pygame.K_t]:
        time_stop_active = True
        time_stop_start = pygame.time.get_ticks()
        pause_start = time_stop_start
        the_world_sound.play()  # 播放语音

    # 判断是否超过5秒，解除时停
    if time_stop_active and pygame.time.get_ticks() - time_stop_start > TIME_STOP_DURATION:
        pause_end = pygame.time.get_ticks()
        time_stop_active = False
        # 计算这次暂停总共多长
        pause_duration = pause_end - pause_start
        # 把它加到 start_ticks 上，彻底“剔除”这段时间
        start_ticks += pause_duration

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
        victory_sound.play()
        pygame.mixer.music.stop()
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
    if time_stop_active:
        ts_text = font.render("Time Stop!", True, (0, 0, 0))
        screen.blit(ts_text, (WIDTH // 2 - 60, HEIGHT // 2 - 100))

    if win:
        win_text = font.render("You Win!", True, (255, 0, 0))
        screen.blit(win_text, (WIDTH // 2 - 50, 50))
        # 可选的延迟退出
        pygame.display.flip()
        pygame.time.delay(37000)
        pygame.quit()
        sys.exit()

    pygame.display.flip()

pygame.quit()
sys.exit()