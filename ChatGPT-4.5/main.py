import pygame
import random

# Initialize pygame
pygame.init()

# Game window dimensions
width, height = 600, 400
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')

# Colors
white = pygame.Color(255, 255, 255)
black = pygame.Color(0, 0, 0)
green = pygame.Color(0, 255, 0)
red = pygame.Color(255, 0, 0)

# Snake settings
snake_pos = [100, 50]
snake_body = [[100, 50], [80, 50], [60, 50]]
snake_direction = 'RIGHT'
change_to = snake_direction
speed = 10

# Food settings
food_pos = [random.randrange(1, (width//20)) * 20, random.randrange(1, (height//20)) * 20]
food_spawn = True

# Score
score = 0

# Speed increment tracker
food_eaten = 0

# Game Over flag
game_over = False

# Clock
fps = pygame.time.Clock()

# Score display function
def show_score():
    font = pygame.font.SysFont('consolas', 20)
    score_surface = font.render(f'Score: {score}', True, white)
    window.blit(score_surface, (10, 10))

# Game over function
def game_over_screen():
    window.fill(black)
    font = pygame.font.SysFont('consolas', 30)
    go_surface = font.render(f'Game Over! Final Score: {score}', True, red)
    window.blit(go_surface, (width//2 - go_surface.get_width()//2, height//2 - go_surface.get_height()//2))
    pygame.display.flip()
    # Wait for a key press
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                pygame.quit()
                quit()

# Main game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        # Arrow key controls
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != 'DOWN':
                change_to = 'UP'
            elif event.key == pygame.K_DOWN and snake_direction != 'UP':
                change_to = 'DOWN'
            elif event.key == pygame.K_LEFT and snake_direction != 'RIGHT':
                change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT and snake_direction != 'LEFT':
                change_to = 'RIGHT'

    snake_direction = change_to

    # Snake movement logic
    if snake_direction == 'UP':
        snake_pos[1] -= 20
    if snake_direction == 'DOWN':
        snake_pos[1] += 20
    if snake_direction == 'LEFT':
        snake_pos[0] -= 20
    if snake_direction == 'RIGHT':
        snake_pos[0] += 20

    # Snake body growing mechanism
    snake_body.insert(0, list(snake_pos))
    if snake_pos == food_pos:
        score += 10
        food_spawn = False
        food_eaten += 1
        if food_eaten % 5 == 0:
            speed += 2  # Increase speed every 5 foods eaten
    else:
        snake_body.pop()

    # Spawn food
    if not food_spawn:
        while True:
            food_pos = [random.randrange(1, (width//20)) * 20,
                        random.randrange(1, (height//20)) * 20]
            if food_pos not in snake_body:
                break
        food_spawn = True

    # Clear the screen
    window.fill(black)

    # Draw snake
    for pos in snake_body:
        pygame.draw.rect(window, green, pygame.Rect(pos[0], pos[1], 20, 20))

    # Draw food
    pygame.draw.rect(window, red, pygame.Rect(food_pos[0], food_pos[1], 20, 20))

    # Check collisions
    if snake_pos[0] < 0 or snake_pos[0] >= width:
        game_over_screen()
    if snake_pos[1] < 0 or snake_pos[1] >= height:
        game_over_screen()
    for block in snake_body[1:]:
        if snake_pos == block:
            game_over_screen()

    # Display score
    show_score()

    # Refresh game screen
    pygame.display.update()

    # Control game speed
    fps.tick(speed)

# Exit the game
pygame.quit()
