import pygame
import random
import sys
from enum import Enum
from typing import List, Tuple

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 800
GRID_SIZE = 20
GRID_COUNT = WINDOW_SIZE // GRID_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class PowerUpType(Enum):
    SPEED = 1
    DOUBLE_POINTS = 2
    INVINCIBILITY = 3

class PowerUp:
    def __init__(self, x: int, y: int, type: PowerUpType):
        self.x = x
        self.y = y
        self.type = type
        self.active = True
        self.duration = 5000  # 5 seconds

class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.length = 1
        self.positions = [(GRID_COUNT // 2, GRID_COUNT // 2)]
        self.direction = Direction.RIGHT
        self.score = 0
        self.speed = 10
        self.invincible = False
        self.double_points = False

    def get_head_position(self) -> Tuple[int, int]:
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = cur

        if self.direction == Direction.UP:
            y -= 1
        elif self.direction == Direction.DOWN:
            y += 1
        elif self.direction == Direction.LEFT:
            x -= 1
        elif self.direction == Direction.RIGHT:
            x += 1

        new_head = (x, y)
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def render(self, surface: pygame.Surface):
        for i, p in enumerate(self.positions):
            color = GREEN if i == 0 else (0, 200, 0)  # Head is slightly different color
            pygame.draw.rect(surface, color, 
                           (p[0] * GRID_SIZE, p[1] * GRID_SIZE, GRID_SIZE - 2, GRID_SIZE - 2))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption('Retro Snake')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.snake = Snake()
        self.food = self.generate_food()
        self.power_ups: List[PowerUp] = []
        self.game_over = False
        self.paused = False
        self.power_up_active = False
        self.power_up_timer = 0

    def generate_food(self) -> Tuple[int, int]:
        while True:
            x = random.randint(0, GRID_COUNT - 1)
            y = random.randint(0, GRID_COUNT - 1)
            if (x, y) not in self.snake.positions:
                return (x, y)

    def generate_power_up(self):
        if random.random() < 0.1 and not self.power_up_active:  # 10% chance
            x = random.randint(0, GRID_COUNT - 1)
            y = random.randint(0, GRID_COUNT - 1)
            if (x, y) not in self.snake.positions and (x, y) != self.food:
                power_type = random.choice(list(PowerUpType))
                self.power_ups.append(PowerUp(x, y, power_type))

    def handle_power_up(self, power_up: PowerUp):
        if power_up.type == PowerUpType.SPEED:
            self.snake.speed = min(20, self.snake.speed + 2)
        elif power_up.type == PowerUpType.DOUBLE_POINTS:
            self.snake.double_points = True
        elif power_up.type == PowerUpType.INVINCIBILITY:
            self.snake.invincible = True
        
        self.power_up_active = True
        self.power_up_timer = pygame.time.get_ticks()
        power_up.active = False

    def update_power_ups(self):
        current_time = pygame.time.get_ticks()
        if self.power_up_active and current_time - self.power_up_timer > 5000:
            self.snake.speed = 10
            self.snake.double_points = False
            self.snake.invincible = False
            self.power_up_active = False

        self.power_ups = [p for p in self.power_ups if p.active]

    def handle_collision(self) -> bool:
        head = self.snake.get_head_position()
        
        # Wall collision
        if not self.snake.invincible and (head[0] < 0 or head[0] >= GRID_COUNT or 
                                        head[1] < 0 or head[1] >= GRID_COUNT):
            return True

        # Self collision
        if not self.snake.invincible and head in self.snake.positions[1:]:
            return True

        return False

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.paused = not self.paused
                    elif event.key == pygame.K_r and self.game_over:
                        self.reset_game()
                    elif not self.paused and not self.game_over:
                        if event.key == pygame.K_UP and self.snake.direction != Direction.DOWN:
                            self.snake.direction = Direction.UP
                        elif event.key == pygame.K_DOWN and self.snake.direction != Direction.UP:
                            self.snake.direction = Direction.DOWN
                        elif event.key == pygame.K_LEFT and self.snake.direction != Direction.RIGHT:
                            self.snake.direction = Direction.LEFT
                        elif event.key == pygame.K_RIGHT and self.snake.direction != Direction.LEFT:
                            self.snake.direction = Direction.RIGHT

            if not self.paused and not self.game_over:
                self.snake.update()
                
                # Check for food collision
                if self.snake.get_head_position() == self.food:
                    self.snake.length += 1
                    points = 10 if self.snake.double_points else 5
                    self.snake.score += points
                    self.food = self.generate_food()
                    self.generate_power_up()

                # Check for power-up collision
                for power_up in self.power_ups:
                    if power_up.active and self.snake.get_head_position() == (power_up.x, power_up.y):
                        self.handle_power_up(power_up)

                # Check for game over
                if self.handle_collision():
                    self.game_over = True

                self.update_power_ups()

            self.draw()
            self.clock.tick(self.snake.speed)

    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw grid lines
        for x in range(0, WINDOW_SIZE, GRID_SIZE):
            pygame.draw.line(self.screen, (40, 40, 40), (x, 0), (x, WINDOW_SIZE))
        for y in range(0, WINDOW_SIZE, GRID_SIZE):
            pygame.draw.line(self.screen, (40, 40, 40), (0, y), (WINDOW_SIZE, y))

        # Draw snake
        self.snake.render(self.screen)

        # Draw food
        pygame.draw.rect(self.screen, RED, 
                        (self.food[0] * GRID_SIZE, self.food[1] * GRID_SIZE, 
                         GRID_SIZE - 2, GRID_SIZE - 2))

        # Draw power-ups
        for power_up in self.power_ups:
            if power_up.active:
                color = YELLOW if power_up.type == PowerUpType.SPEED else \
                        BLUE if power_up.type == PowerUpType.DOUBLE_POINTS else \
                        WHITE
                pygame.draw.rect(self.screen, color,
                               (power_up.x * GRID_SIZE, power_up.y * GRID_SIZE,
                                GRID_SIZE - 2, GRID_SIZE - 2))

        # Draw score
        score_text = self.font.render(f'Score: {self.snake.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))

        # Draw game over or pause message
        if self.game_over:
            text = self.font.render('GAME OVER! Press R to restart', True, WHITE)
        elif self.paused:
            text = self.font.render('PAUSED', True, WHITE)
        else:
            text = self.font.render('Press P to pause', True, WHITE)
        
        text_rect = text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))
        self.screen.blit(text, text_rect)

        pygame.display.flip()

    def reset_game(self):
        self.snake.reset()
        self.food = self.generate_food()
        self.power_ups.clear()
        self.game_over = False
        self.paused = False
        self.power_up_active = False
        self.power_up_timer = 0

if __name__ == '__main__':
    game = Game()
    game.run()
