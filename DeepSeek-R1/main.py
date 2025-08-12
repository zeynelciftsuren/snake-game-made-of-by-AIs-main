import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 15

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Retro Snake Game")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont("arcade", 30)
game_over_font = pygame.font.SysFont("arcade", 50)

# Snake and Food
class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.grow = False

    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def change_direction(self, new_dir):
        if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
            self.direction = new_dir

    def check_collision(self):
        head = self.body[0]
        return (head in self.body[1:] or
                head[0] < 0 or head[0] >= GRID_WIDTH or
                head[1] < 0 or head[1] >= GRID_HEIGHT)

    def draw(self):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

class Food:
    def __init__(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        self.type = random.choice(["normal", "powerup"])

    def draw(self):
        color = RED if self.type == "normal" else YELLOW
        pygame.draw.rect(screen, color, (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

# Game Functions
def draw_grid():
    for x in range(0, WIDTH, GRID_SIZE):
        for y in range(0, HEIGHT, GRID_SIZE):
            rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 1)

def display_score(score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def game_over():
    text = game_over_font.render("GAME OVER", True, RED)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    quit()

# Main Game Loop
def main():
    snake = Snake()
    food = Food()
    score = 0
    level = 1

    running = True
    while running:
        clock.tick(FPS + level * 2)  # Increase speed with level

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction((0, -1))
                if event.key == pygame.K_DOWN:
                    snake.change_direction((0, 1))
                if event.key == pygame.K_LEFT:
                    snake.change_direction((-1, 0))
                if event.key == pygame.K_RIGHT:
                    snake.change_direction((1, 0))

        snake.move()

        # Check if snake eats food
        if snake.body[0] == food.position:
            snake.grow = True
            if food.type == "normal":
                score += 10
            else:
                score += 20
            food = Food()
            if score % 50 == 0:
                level += 1

        # Check collision
        if snake.check_collision():
            game_over()

        # Draw everything
        screen.fill(BLACK)
        draw_grid()
        snake.draw()
        food.draw()
        display_score(score)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()