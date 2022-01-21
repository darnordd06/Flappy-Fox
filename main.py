import random
import pygame
import sys


def draw_floor():
    screen.blit(floor, (floor_x_pos, 800))
    screen.blit(floor, (floor_x_pos + 1280, 800))


def create_tube():
    random_tube_pos = random.choice(tube_height)
    random_hole_size = random.randint(230, 300)
    bottom_tube = tube_surface.get_rect(midtop=(1400, random_tube_pos))
    top_tube = tube_surface.get_rect(midbottom=(1400, random_tube_pos - random_hole_size))
    return bottom_tube, top_tube


def move_tubes(tubes):
    for tube in tubes:
        tube.centerx -= 7
    return tubes


def draw_tubes(tubes):
    for tube in tubes:
        screen.blit(tube_surface, tube)


def check_collision(tubes):
    for tube in tubes:
        if fox_rect.colliderect(tube):
            die_sound.play()
            return False

    if fox_rect.top <= -100 or fox_rect.bottom >= 900:
        return False

    return True


def rotate_fox(fox):
    new_fox = pygame.transform.rotozoom(fox, -fox_movement * 2, 1)
    return new_fox


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(640, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(640, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(640, 700))
        screen.blit(high_score_surface, high_score_rect)

        restart_surface = game_font.render('SPACE to RESTART', True, (0, 0, 0))
        restart_rect = restart_surface.get_rect(center=(640, 425))
        screen.blit(restart_surface, restart_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


pygame.init()
pygame.display.set_caption('Flappy Fox')
screen = pygame.display.set_mode((1280, 1000))
clock = pygame.time.Clock()
game_font = pygame.font.Font('шрифт.otf', 40)

# переменные для игры:
gravity = 0.35
fox_movement = 0
game_active = True
score = 0
high_score = 0

bg = pygame.image.load('assets/summer_bg.png').convert()
floor = pygame.image.load('assets/summer_floor.png').convert()
floor_x_pos = 0

fox = pygame.image.load('assets/fox_idle.png').convert_alpha()
fox_scale = pygame.transform.scale(fox, (135, 135))
fox_rect = fox_scale.get_rect(center=(300, 500))

tube_surface = pygame.image.load('assets/tube.png')
tube_list = []
SPAWNTUBE = pygame.USEREVENT
pygame.time.set_timer(SPAWNTUBE, 2400)
tube_height = [400, 450, 500, 550, 600, 650, 700]

# Звуки
flap_sound = pygame.mixer.Sound('sound/sound_sfx_wing.wav')
die_sound = pygame.mixer.Sound('sound/sound_sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sound_sfx_point.wav')
score_sound_countdown = 100

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                fox_movement = 0
                fox_movement -= 7
                flap_sound.play()
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                tube_list.clear()
                fox_rect.center = (300, 500)
                fox_movement = 0
                score = 0

        if event.type == SPAWNTUBE:
            tube_list.extend(create_tube())
    screen.blit(bg, (0, 0))

    if game_active:
        # Движение лисы
        fox_movement += gravity
        rotated_fox = rotate_fox(fox_scale)
        fox_rect.centery += fox_movement
        screen.blit(rotated_fox, fox_rect)
        game_active = check_collision(tube_list)

        # Трубы
        tube_list = move_tubes(tube_list)
        draw_tubes(tube_list)

        score += 0.01
        score_display('main_game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound_countdown = 100
    else:
        high_score = update_score(score, high_score)
        score_display('game_over')

    # Движение пола
    floor_x_pos -= 7
    draw_floor()
    if floor_x_pos <= -1280:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(60)
