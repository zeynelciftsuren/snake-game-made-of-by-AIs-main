import pygame
import sys
import random
import time
from pygame.math import Vector2

# Initialize pygame
pygame.init()

# Game constants
CELL_SIZE = 30
CELL_NUMBER = 20
SCREEN_WIDTH = CELL_SIZE * CELL_NUMBER
SCREEN_HEIGHT = CELL_SIZE * CELL_NUMBER
FPS = 60

# Colors
BG_COLOR = (0, 0, 0)
GRID_COLOR = (20, 20, 20)
SNAKE_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 0, 0)
SCORE_COLOR = (255, 255, 255)
POWERUP_COLOR = (0, 255, 255)
UI_BG_COLOR = (30, 30, 30)

# Fonts
game_font = pygame.font.Font(None, 42)
small_font = pygame.font.Font(None, 28)

class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False
        self.speed = 10  # Base speed
        
        # Snake head and body graphics
        self.head_up = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.head_up.fill(SNAKE_COLOR)
        self.head_down = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.head_down.fill(SNAKE_COLOR)
        self.head_right = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.head_right.fill(SNAKE_COLOR)
        self.head_left = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.head_left.fill(SNAKE_COLOR)
        
        self.body_surface = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.body_surface.fill(SNAKE_COLOR)

    def draw_snake(self, screen):
        for index, block in enumerate(self.body):
            pos = (int(block.x * CELL_SIZE), int(block.y * CELL_SIZE))
            snake_rect = pygame.Rect(pos, (CELL_SIZE, CELL_SIZE))
            
            if index == 0:  # Head
                if self.direction == Vector2(0, -1):
                    screen.blit(self.head_up, snake_rect)
                elif self.direction == Vector2(0, 1):
                    screen.blit(self.head_down, snake_rect)
                elif self.direction == Vector2(1, 0):
                    screen.blit(self.head_right, snake_rect)
                elif self.direction == Vector2(-1, 0):
                    screen.blit(self.head_left, snake_rect)
            else:  # Body
                screen.blit(self.body_surface, snake_rect)

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def grow(self):
        self.new_block = True

    def increase_speed(self):
        if self.speed < 20:  # Cap the speed
            self.speed += 0.5

    def check_collision(self):
        # Check if snake hits wall
        if (self.body[0].x < 0 or self.body[0].x >= CELL_NUMBER or 
            self.body[0].y < 0 or self.body[0].y >= CELL_NUMBER):
            return True
        
        # Check if snake hits itself
        for block in self.body[1:]:
            if block == self.body[0]:
                return True
        
        return False

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.speed = 10


class Food:
    def __init__(self):
        self.position = Vector2(0, 0)
        self.randomize()
        
        # Food graphic
        self.food_surface = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.food_surface.fill(FOOD_COLOR)

    def draw_food(self, screen):
        food_rect = pygame.Rect(int(self.position.x * CELL_SIZE), int(self.position.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
        screen.blit(self.food_surface, food_rect)
        
    def randomize(self):
        self.position.x = random.randint(0, CELL_NUMBER - 1)
        self.position.y = random.randint(0, CELL_NUMBER - 1)


class PowerUp:
    def __init__(self):
        self.position = Vector2(-1, -1)  # Off-screen initially
        self.active = False
        self.type = random.choice(["speed", "score", "invincibility"])
        self.spawn_time = 0
        self.duration = 5  # Duration in seconds
        
        # PowerUp graphic
        self.powerup_surface = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.powerup_surface.fill(POWERUP_COLOR)

    def draw_powerup(self, screen):
        if self.active:
            powerup_rect = pygame.Rect(int(self.position.x * CELL_SIZE), int(self.position.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
            screen.blit(self.powerup_surface, powerup_rect)
        
    def spawn(self):
        if not self.active and random.random() < 0.01:  # 1% chance per frame
            self.position.x = random.randint(0, CELL_NUMBER - 1)
            self.position.y = random.randint(0, CELL_NUMBER - 1)
            self.type = random.choice(["speed", "score", "invincibility"])
            self.active = True
            self.spawn_time = time.time()

    def check_timeout(self):
        if self.active and time.time() - self.spawn_time > 10:  # Despawn after 10 seconds
            self.active = False
            self.position = Vector2(-1, -1)


class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.powerup = PowerUp()
        self.score = 0
        self.high_score = 0
        self.game_active = True
        self.last_update_time = 0
        self.power_active = False
        self.power_type = None
        self.power_end_time = 0
        
        # Initialize screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + 50))  # Extra 50px for UI
        pygame.display.set_caption('Snake Game')
        
        # Game clock
        self.clock = pygame.time.Clock()

    def update(self):
        current_time = time.time()
        
        # Only move snake at certain intervals (based on speed)
        if current_time - self.last_update_time >= 1 / self.snake.speed:
            self.snake.move_snake()
            self.last_update_time = current_time
            self.check_collision()
        
        self.powerup.spawn()
        self.powerup.check_timeout()
        self.check_power_timeout()

    def draw_elements(self):
        self.screen.fill(BG_COLOR)
        
        # Draw grid
        for row in range(CELL_NUMBER):
            for col in range(CELL_NUMBER):
                if (row + col) % 2 == 0:
                    grid_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(self.screen, GRID_COLOR, grid_rect)
        
        # Draw UI bar
        ui_rect = pygame.Rect(0, SCREEN_HEIGHT, SCREEN_WIDTH, 50)
        pygame.draw.rect(self.screen, UI_BG_COLOR, ui_rect)
        
        # Draw score
        score_text = game_font.render(f'Score: {self.score}', True, SCORE_COLOR)
        self.screen.blit(score_text, (20, SCREEN_HEIGHT + 10))
        
        # Draw high score
        high_score_text = small_font.render(f'High Score: {self.high_score}', True, SCORE_COLOR)
        self.screen.blit(high_score_text, (SCREEN_WIDTH - 200, SCREEN_HEIGHT + 15))
        
        # Draw active power-up
        if self.power_active:
            power_text = small_font.render(f'Power: {self.power_type}', True, POWERUP_COLOR)
            self.screen.blit(power_text, (SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT + 15))
        
        self.food.draw_food(self.screen)
        self.powerup.draw_powerup(self.screen)
        self.snake.draw_snake(self.screen)
        
        # Game over message
        if not self.game_active:
            game_over_surf = game_font.render('GAME OVER', True, SCORE_COLOR)
            restart_surf = small_font.render('Press SPACE to Restart', True, SCORE_COLOR)
            
            self.screen.blit(game_over_surf, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 30))
            self.screen.blit(restart_surf, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 20))
        
        pygame.display.update()

    def check_collision(self):
        # Check if snake eats food
        if self.snake.body[0] == self.food.position:
            self.food.randomize()
            self.snake.grow()
            self.score += 1
            if self.score > self.high_score:
                self.high_score = self.score
            
            # Make the game progressively harder
            if self.score % 5 == 0:
                self.snake.increase_speed()
        
        # Check if snake collides with powerup
        if self.powerup.active and self.snake.body[0] == self.powerup.position:
            self.activate_powerup(self.powerup.type)
            self.powerup.active = False
            self.powerup.position = Vector2(-1, -1)
        
        # Check for game over conditions
        if not self.power_active or self.power_type != "invincibility":
            if self.snake.check_collision():
                self.game_active = False
        
        # Ensure food doesn't spawn on snake or powerup
        while self.food.position in self.snake.body or self.food.position == self.powerup.position:
            self.food.randomize()

    def activate_powerup(self, power_type):
        self.power_active = True
        self.power_type = power_type
        self.power_end_time = time.time() + self.powerup.duration
        
        if power_type == "speed":
            self.snake.speed += 5
        elif power_type == "score":
            self.score += 5

    def check_power_timeout(self):
        if self.power_active and time.time() > self.power_end_time:
            if self.power_type == "speed":
                self.snake.speed = max(10, self.snake.speed - 5)
            
            self.power_active = False
            self.power_type = None

    def reset_game(self):
        self.snake.reset()
        self.food.randomize()
        self.powerup.active = False
        self.powerup.position = Vector2(-1, -1)
        self.score = 0
        self.game_active = True
        self.power_active = False
        self.power_type = None

def main():
    game = Game()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Handle controls (keyboard)
            if event.type == pygame.KEYDOWN:
                if game.game_active:
                    if event.key == pygame.K_UP and game.snake.direction.y != 1:
                        game.snake.direction = Vector2(0, -1)
                    if event.key == pygame.K_DOWN and game.snake.direction.y != -1:
                        game.snake.direction = Vector2(0, 1)
                    if event.key == pygame.K_LEFT and game.snake.direction.x != 1:
                        game.snake.direction = Vector2(-1, 0)
                    if event.key == pygame.K_RIGHT and game.snake.direction.x != -1:
                        game.snake.direction = Vector2(1, 0)
                else:
                    if event.key == pygame.K_SPACE:
                        game.reset_game()
        
        if game.game_active:
            game.update()
        
        game.draw_elements()
        game.clock.tick(FPS)

if __name__ == "__main__":
    main()