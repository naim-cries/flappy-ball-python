import pygame
import random
import sys

pygame.init()

# Window setup
WIDTH, HEIGHT = 400, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 200, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.SysFont("comicsans", 40)
small_font = pygame.font.SysFont("comicsans", 30)

# Clock
clock = pygame.time.Clock()
FPS = 60

def draw_text(text, size, color, x, y, center=True):
    f = pygame.font.SysFont("comicsans", size)
    text_surf = f.render(text, True, color)
    text_rect = text_surf.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    win.blit(text_surf, text_rect)

def start_menu():
    while True:
        win.fill(BLUE)
        draw_text("🐦 Flappy Bird", 60, WHITE, WIDTH//2, HEIGHT//3)
        draw_text("Tap to Start", 40, WHITE, WIDTH//2, HEIGHT//2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Tap or click
            if event.type == pygame.MOUSEBUTTONDOWN:
                return

        pygame.display.update()
        clock.tick(30)

def game_over_screen(score):
    while True:
        win.fill(BLUE)
        draw_text("Game Over", 60, WHITE, WIDTH//2, HEIGHT//3)
        draw_text(f"Score: {score}", 40, WHITE, WIDTH//2, HEIGHT//2)
        draw_text("Tap to Restart", 30, WHITE, WIDTH//2, HEIGHT - 100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return

        pygame.display.update()
        clock.tick(30)

def main_game():
    # Bird
    bird_x = 50
    bird_y = 300
    bird_radius = 20
    bird_velocity = 0
    gravity = 0.5
    jump_strength = -10

    # Pipe
    pipe_width = 60
    pipe_gap = 150
    pipe_x = WIDTH
    pipe_height = random.randint(100, 400)
    pipe_speed = 3

    # Score
    score = 0

    running = True
    while running:
        clock.tick(FPS)
        win.fill(BLUE)

        # Bird physics
        bird_velocity += gravity
        bird_y += bird_velocity

        # Pipe movement
        pipe_x -= pipe_speed
        if pipe_x + pipe_width < 0:
            pipe_x = WIDTH
            pipe_height = random.randint(100, 400)
            score += 1

        # Draw pipes
        pygame.draw.rect(win, GREEN, (pipe_x, 0, pipe_width, pipe_height))
        pygame.draw.rect(win, GREEN, (pipe_x, pipe_height + pipe_gap, pipe_width, HEIGHT))

        # Draw bird
        pygame.draw.circle(win, WHITE, (bird_x, int(bird_y)), bird_radius)

        # Score
        draw_text(f"Score: {score}", 30, WHITE, 10, 10, center=False)

        # Collision
        if (
            bird_y - bird_radius < 0
            or bird_y + bird_radius > HEIGHT
            or (pipe_x < bird_x + bird_radius < pipe_x + pipe_width and
                (bird_y - bird_radius < pipe_height or bird_y + bird_radius > pipe_height + pipe_gap))
        ):
            game_over_screen(score)
            return

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Space or Tap
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird_velocity = jump_strength
            if event.type == pygame.MOUSEBUTTONDOWN:
                bird_velocity = jump_strength

        pygame.display.update()

# Run game
while True:
    start_menu()
    main_game()

