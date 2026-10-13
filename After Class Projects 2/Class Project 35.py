import math
import random
from array import array

import pygame

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
PLAYER_START_X = 370
PLAYER_START_Y = 380
ENEMY_START_Y_MIN = 50
ENEMY_START_Y_MAX = 160
BULLET_SPEED_Y = 10
PLAYER_SPEED = 5

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invader")

icon = pygame.Surface((32, 32), pygame.SRCALPHA)
pygame.draw.polygon(icon, (255, 255, 255), [(16, 2), (28, 24), (20, 20), (20, 30), (12, 30), (12, 20), (4, 24)])
pygame.display.set_icon(icon)

stars = []
for _ in range(120):
    stars.append(
        {
            "x": random.randint(0, SCREEN_WIDTH),
            "y": random.randint(0, SCREEN_HEIGHT),
            "radius": random.randint(1, 3),
            "speed": random.randint(1, 3),
        }
    )

clock = pygame.time.Clock()
background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
for y in range(SCREEN_HEIGHT):
    ratio = y / SCREEN_HEIGHT
    r = int(8 + (25 - 8) * ratio)
    g = int(12 + (50 - 12) * ratio)
    b = int(38 + (90 - 38) * ratio)
    pygame.draw.line(background, (r, g, b), (0, y), (SCREEN_WIDTH, y))

for star in stars:
    pygame.draw.circle(background, (255, 255, 255), (star["x"], star["y"]), star["radius"])


def make_tone(frequency, duration, volume=0.10, sweep=0.0):
    sample_rate = 22050
    frame_count = int(sample_rate * duration)
    samples = array("h")
    for i in range(frame_count):
        time = i / sample_rate
        wave = math.sin(2 * math.pi * (frequency + sweep * time) * time)
        envelope = max(0.0, 1.0 - (time / duration))
        samples.append(int(32767 * volume * wave * envelope))
    return pygame.mixer.Sound(buffer=samples.tobytes())

shoot_sound = make_tone(520, 0.08, 0.12, sweep=180)
hit_sound = make_tone(220, 0.14, 0.16, sweep=-100)
lose_sound = make_tone(90, 0.4, 0.18, sweep=-200)
background_music = make_tone(140, 0.35, 0.04, sweep=20)
background_channel = pygame.mixer.Channel(0)
background_channel.set_volume(0.25)
background_channel.play(background_music, loops=-1)

score_value = 0
font = pygame.font.Font("freesansbold.ttf", 28)
over_font = pygame.font.Font("freesansbold.ttf", 60)

player_x = PLAYER_START_X
player_y = PLAYER_START_Y
player_x_change = 0

enemies = []
for i in range(6):
    enemies.append(
        {
            "x": random.randint(20, SCREEN_WIDTH - 80),
            "y": random.randint(ENEMY_START_Y_MIN, ENEMY_START_Y_MAX),
            "width": 36,
            "height": 24,
            "speed": random.randint(1, 2),
            "direction": 1,
            "alive": True,
        }
    )

bullet_x = 0
bullet_y = PLAYER_START_Y
bullet_y_change = BULLET_SPEED_Y
bullet_state = "ready"


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def draw_player(x, y):
    ship = [(x + 32, y), (x + 60, y + 30), (x + 48, y + 30), (x + 48, y + 50), (x + 16, y + 50), (x + 16, y + 30), (x, y + 30)]
    pygame.draw.polygon(screen, (100, 220, 255), ship)
    pygame.draw.rect(screen, (255, 255, 255), (x + 22, y + 5, 20, 15))


def draw_enemy(enemy):
    if not enemy["alive"]:
        return
    x = enemy["x"]
    y = enemy["y"]
    body = pygame.Rect(x, y, enemy["width"], enemy["height"])
    pygame.draw.ellipse(screen, (255, 100, 100), body)
    pygame.draw.circle(screen, (255, 220, 180), (x + 18, y + 10), 5)
    pygame.draw.line(screen, (255, 220, 180), (x + 8, y + 17), (x + 28, y + 17), 2)


def draw_bullet(x, y):
    pygame.draw.rect(screen, (255, 230, 100), (x, y, 4, 18))


def is_collision(enemy, bullet_x_pos, bullet_y_pos):
    bullet_rect = pygame.Rect(bullet_x_pos, bullet_y_pos, 4, 18)
    enemy_rect = pygame.Rect(enemy["x"], enemy["y"], enemy["width"], enemy["height"])
    return bullet_rect.colliderect(enemy_rect)


def game_over_text(message):
    over_text = over_font.render(message, True, (255, 255, 255))
    screen.blit(over_text, (180, 210))


running = True
while running:
    for star in stars:
        star["y"] += star["speed"]
        if star["y"] > SCREEN_HEIGHT:
            star["y"] = 0
            star["x"] = random.randint(0, SCREEN_WIDTH)

    background.fill((0, 0, 0))
    for y in range(SCREEN_HEIGHT):
        ratio = y / SCREEN_HEIGHT
        r = int(8 + (25 - 8) * ratio)
        g = int(12 + (50 - 12) * ratio)
        b = int(38 + (90 - 38) * ratio)
        pygame.draw.line(background, (r, g, b), (0, y), (SCREEN_WIDTH, y))
    for star in stars:
        pygame.draw.circle(background, (255, 255, 255), (star["x"], star["y"]), star["radius"])

    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -PLAYER_SPEED
            elif event.key == pygame.K_RIGHT:
                player_x_change = PLAYER_SPEED
            elif event.key == pygame.K_SPACE and bullet_state == "ready":
                bullet_x = player_x + 32
                bullet_y = player_y - 10
                bullet_state = "fire"
                shoot_sound.play()
        if event.type == pygame.KEYUP and event.key in (pygame.K_LEFT, pygame.K_RIGHT):
            player_x_change = 0

    player_x += player_x_change
    player_x = max(0, min(player_x, SCREEN_WIDTH - 64))

    for enemy in enemies:
        if not enemy["alive"]:
            continue
        enemy["x"] += enemy["speed"] * enemy["direction"]
        if enemy["x"] <= 0 or enemy["x"] + enemy["width"] >= SCREEN_WIDTH:
            enemy["direction"] *= -1
            enemy["y"] += 18
        if enemy["y"] > 340:
            game_over_text("GAME OVER")
            lose_sound.play()
            pygame.display.update()
            pygame.time.delay(1200)
            running = False
            break

        if bullet_state == "fire" and is_collision(enemy, bullet_x, bullet_y):
            bullet_y = PLAYER_START_Y
            bullet_state = "ready"
            enemy["alive"] = False
            score_value += 10
            hit_sound.play()

    if bullet_state == "fire":
        bullet_y -= bullet_y_change
        if bullet_y <= 0:
            bullet_y = PLAYER_START_Y
            bullet_state = "ready"

    for enemy in enemies:
        draw_enemy(enemy)

    draw_bullet(bullet_x, bullet_y) if bullet_state == "fire" else None
    draw_player(player_x, player_y)
    show_score(10, 10)

    if not any(enemy["alive"] for enemy in enemies):
        game_over_text("YOU WIN")
        pygame.display.update()
        pygame.time.delay(1500)
        running = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()
