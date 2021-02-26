import pygame
from random import randrange as rnd

WIDTH, HEIGHT = 1200, 800
fps = 60
print()
# настройки платформы
platform_width = 330
platform_height = 35
platform_speed = 15SDSDFSDFSDF
platform = pygame.Rect(WIDTH // 2 - platform_width // 2, HEIGHT - platform_height - 10, platform_width, platform_height)
# шарик
ball_radius = 20
ball_speed = 6
ball_rect = int(ball_radius * 2 ** 0.5)
ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)
score = 0
dx, dy = 1, -1
# блоки
block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(10) for j in range(4)]

pygame.init()
pygame.display.set_caption('ARKANOID')
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
# задний фон
img = pygame.image.load('dog.jpg.').convert()
# счет игры
font_score = pygame.font.SysFont('Broadway', 26, bold=True)
pygame.mixer.music.load('background.mp3')
pygame.mixer.music.set_volume(0.5)


# определяем столкновения
def detect_collision(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    screen.blit(img, (0, 0))
    # тут будут рисоваться все объекты в игре
    [pygame.draw.rect(screen, color_list[color], block) for color, block in enumerate(block_list)]
    pygame.draw.rect(screen, pygame.Color('yellow'), platform)
    pygame.draw.circle(screen, pygame.Color('white'), ball.center, ball_radius)
    # рендарим счёт игры
    render_score = font_score.render(f'SCORE: {score}', 1, pygame.Color('orange'))
    screen.blit(render_score, (35, 760))
    # передвижение шарика
    ball.x += ball_speed * dx
    ball.y += ball_speed * dy
    # столкновение шарика с правой и левой стенами
    if ball.centerx < ball_radius or ball.centerx > WIDTH - ball_radius:
        dx = -dx
    # столкновение шарика с верхней стеной
    if ball.centery < ball_radius:
        dy = -dy
    # столкновение шарика с платформой
    if ball.colliderect(platform) and dy > 0:
        dx, dy = detect_collision(dx, dy, ball, platform)
    # cтолкновение шарика с блоками
    hit_index = ball.collidelist(block_list)
    if hit_index != -1:
        hit_rect = block_list.pop(hit_index)
        hit_color = color_list.pop(hit_index)
        dx, dy = detect_collision(dx, dy, ball, hit_rect)
        score += 1

        # спецэфекты!(увеличение блока в 5 раз при его столкновении с шаром);
        # повышение сложности - увеличиваем фпс - увеличивается скорость шарика
        hit_rect.inflate_ip(ball.width * 5, ball.height * 5)
        pygame.draw.rect(screen, hit_color, hit_rect)
        fps += 1
    # проигрыш или выигрыш
    # вывод в консоль(пока что в консоль)
    if ball.bottom > HEIGHT:
        print('ВЫ ПРОИГРАЛИ')
        print('Ваш счёт:', score)
        exit()
    elif not len(block_list):
        print('!ПОБЕДА!')
        exit()
    # управление
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and platform.left > 0:
        platform.left -= platform_speed
    if key[pygame.K_RIGHT] and platform.right < WIDTH:
        platform.right += platform_speed
    pygame.mixer.music.play(-1)

    pygame.display.flip()
    clock.tick(fps)
