import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Fonts
FONT = pygame.font.Font(pygame.font.get_default_font(), 25)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Snake and Food
snake = [(100, 100), (90, 100), (80, 100)]
snake_dir = "RIGHT"
food_pos = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
            random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)
food_spawn = True

# Power-up
powerup_pos = None
powerup_spawn = False
powerup_timer = 0

# Game variables
score = 0
speed = 10
game_over = False

def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE))

def draw_food(food_pos):
    pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], CELL_SIZE, CELL_SIZE))

def draw_powerup(powerup_pos):
    if powerup_pos:
        pygame.draw.rect(screen, YELLOW, pygame.Rect(powerup_pos[0], powerup_pos[1], CELL_SIZE, CELL_SIZE))

def show_score():
    score_text = FONT.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def game_over_screen():
    screen.fill(BLACK)
    game_over_text = FONT.render("Game Over!", True, RED)
    score_text = FONT.render(f"Your Score: {score}", True, WHITE)
    restart_text = FONT.render("Press R to Restart or Q to Quit", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
    screen.blit(score_text, (WIDTH // 2 - 100, HEIGHT // 2))
    screen.blit(restart_text, (WIDTH // 2 - 200, HEIGHT // 2 + 50))
    pygame.display.flip()

# Main game loop
while True:
    if game_over:
        game_over_screen()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Restart the game
                    snake = [(100, 100), (90, 100), (80, 100)]
                    snake_dir = "RIGHT"
                    food_pos = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
                                random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)
                    food_spawn = True
                    powerup_pos = None
                    powerup_spawn = False
                    powerup_timer = 0
                    score = 0
                    speed = 10
                    game_over = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_dir != "DOWN":
                snake_dir = "UP"
            elif event.key == pygame.K_DOWN and snake_dir != "UP":
                snake_dir = "DOWN"
            elif event.key == pygame.K_LEFT and snake_dir != "RIGHT":
                snake_dir = "LEFT"
            elif event.key == pygame.K_RIGHT and snake_dir != "LEFT":
                snake_dir = "RIGHT"

    # Move the snake
    head_x, head_y = snake[0]
    if snake_dir == "UP":
        head_y -= CELL_SIZE
    elif snake_dir == "DOWN":
        head_y += CELL_SIZE
    elif snake_dir == "LEFT":
        head_x -= CELL_SIZE
    elif snake_dir == "RIGHT":
        head_x += CELL_SIZE
    new_head = (head_x, head_y)

    # Check for collisions
    if new_head in snake or head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
        game_over = True

    # Check if the snake eats food
    if new_head == food_pos:
        score += 10
        food_spawn = False
        speed += 0.5
    else:
        snake.pop()

    # Spawn food
    if not food_spawn:
        food_pos = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
                    random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)
        food_spawn = True

    # Spawn power-up
    if not powerup_spawn and random.randint(1, 100) > 95:
        powerup_pos = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
                       random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)
        powerup_spawn = True
        powerup_timer = time.time()

    # Check if the snake eats the power-up
    if powerup_pos and new_head == powerup_pos:
        score += 50
        powerup_pos = None
        powerup_spawn = False

    # Remove power-up after 10 seconds
    if powerup_spawn and time.time() - powerup_timer > 10:
        powerup_pos = None
        powerup_spawn = False

    # Update snake
    snake.insert(0, new_head)

    # Draw everything
    screen.fill(BLACK)
    draw_snake(snake)
    draw_food(food_pos)
    draw_powerup(powerup_pos)
    show_score()
    pygame.display.flip()

    # Control the game speed
    clock.tick(speed)