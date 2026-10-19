
import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Window Setup
WIDTH, HEIGHT = 500, 540  
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = (HEIGHT - 40) // CELL_SIZE
FPS = 10

# Color Palettes for Snake 
SNAKE_PALETTES = [
    {"head": (46, 125, 50), "body": (76, 175, 80)},    
    {"head": (21, 101, 192), "body": (66, 165, 245)}, 
    {"head": (106, 27, 154), "body": (171, 71, 188)},  
    {"head": (230, 81, 0), "body": (255, 152, 0)},     
    {"head": (0, 131, 143), "body": (38, 198, 218)}    
]

# Random Foods with Different Points
FOOD_TYPES = [
    {"color": (229, 57, 53), "points": 10, "name": "Red Berry"},     
    {"color": (255, 215, 0), "points": 30, "name": "Golden Fruit"}, # 
    {"color": (156, 39, 176), "points": 20, "name": "Magic Grape"},  
    {"color": (118, 255, 3), "points": 15, "name": "Super Apple"}   
]

# UI Colors
BG_COLOR = (18, 18, 18)
BAR_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)
EYE_COLOR = (255, 255, 255)
PUPIL_COLOR = (0, 0, 0)
TONGUE_COLOR = (255, 23, 68)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐍 Realistic Pygame Snake - 3 Lives & Dynamic Colors")
clock = pygame.time.Clock()

class SnakeGame:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.snake = [(6, 5), (5, 5), (4, 5), (3, 5)]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.score = 0
        self.lives = 3              
        self.game_over = False
        self.show_life_lost_screen = False
        self.current_palette = SNAKE_PALETTES[0]
        
        self.spawn_food()

    def reset_snake_position(self):
    
        self.snake = [(6, 5), (5, 5), (4, 5), (3, 5)]
        self.direction = RIGHT
        self.next_direction = RIGHT

    def spawn_food(self):
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if pos not in self.snake:
                self.food = pos
                self.food_type = random.choices(FOOD_TYPES, weights=[60, 10, 15, 15])[0]
                return

    def change_snake_color(self):
        self.current_palette = random.choice(SNAKE_PALETTES)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                
                if self.show_life_lost_screen:
                    if event.key == pygame.K_SPACE:
                        self.show_life_lost_screen = False
                    return
                if self.game_over:
                    if event.key == pygame.K_r:
                        self.reset_game()
                    return

            
                if event.key == pygame.K_UP and self.direction != DOWN:
                    self.next_direction = UP
                elif event.key == pygame.K_DOWN and self.direction != UP:
                    self.next_direction = DOWN
                elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                    self.next_direction = LEFT
                elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                    self.next_direction = RIGHT

    def update(self):
        if self.game_over or self.show_life_lost_screen:
            return

        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        
        if not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT) or new_head in self.snake:
            self.lives -= 1  
            
            if self.lives == 0:
                self.game_over = True
            else:
                self.show_life_lost_screen = True
                self.reset_snake_position()
            return

        self.snake.insert(0, new_head)

        
        if new_head == self.food:
            self.score += self.food_type["points"]
            self.change_snake_color()  
            self.spawn_food()     
        else:
            self.snake.pop()

    def draw_snake(self):
        total_segments = len(self.snake)
        head_color = self.current_palette["head"]
        body_color = self.current_palette["body"]

        
        for i in range(len(self.snake) - 1):
            p1, p2 = self.snake[i], self.snake[i + 1]
            cx1 = p1[0] * CELL_SIZE + CELL_SIZE // 2
            cy1 = p1[1] * CELL_SIZE + CELL_SIZE // 2
            cx2 = p2[0] * CELL_SIZE + CELL_SIZE // 2
            cy2 = p2[1] * CELL_SIZE + CELL_SIZE // 2

            factor = 1.0 - (i / total_segments) * 0.5
            width = int((CELL_SIZE - 4) * factor)
            pygame.draw.line(screen, body_color, (cx1, cy1), (cx2, cy2), width)

    
        for i, (x, y) in enumerate(reversed(self.snake)):
            idx = total_segments - 1 - i
            cx = x * CELL_SIZE + CELL_SIZE // 2
            cy = y * CELL_SIZE + CELL_SIZE // 2
            factor = 1.0 - (idx / total_segments) * 0.5
            radius = int((CELL_SIZE // 2 - 2) * factor)

            if idx == 0:
                
                pygame.draw.circle(screen, head_color, (cx, cy), CELL_SIZE // 2 + 1)

                
                dx, dy = self.direction
                eye_off_x = 5 if dy != 0 else 0
                eye_off_y = 5 if dx != 0 else 0

                for sign in [-1, 1]:
                    ex = cx + dx * 5 + sign * eye_off_x
                    ey = cy + dy * 5 + sign * eye_off_y
                    pygame.draw.circle(screen, EYE_COLOR, (ex, ey), 3)
                    pygame.draw.circle(screen, PUPIL_COLOR, (ex + dx * 1, ey + dy * 1), 1.5)

            
                tx = cx + dx * 14
                ty = cy + dy * 14
                pygame.draw.line(screen, TONGUE_COLOR, (cx + dx * 6, cy + dy * 6), (tx, ty), 2)
            else:
            
                pygame.draw.circle(screen, body_color, (cx, cy), radius)

    def draw_food(self):
        fx, fy = self.food
        cx = fx * CELL_SIZE + CELL_SIZE // 2
        cy = fy * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(screen, self.food_type["color"], (cx, cy), CELL_SIZE // 2 - 2)
        pygame.draw.circle(screen, (118, 255, 3), (cx + 2, cy - CELL_SIZE // 2 + 2), 2)

    def draw_ui(self):

        pygame.draw.rect(screen, BAR_COLOR, (0, HEIGHT - 40, WIDTH, 40))
        font = pygame.font.SysFont("Consolas", 15, bold=True)
        
        
        lives_str = "LIVES: " + "❤️ " * self.lives
        score_text = font.render(f"SCORE: {self.score}", True, TEXT_COLOR)
        lives_text = font.render(lives_str, True, (255, 82, 82))
        food_text = font.render(f"[{self.food_type['name']}]", True, self.food_type["color"])

        screen.blit(score_text, (10, HEIGHT - 28))
        screen.blit(lives_text, (150, HEIGHT - 28))
        screen.blit(food_text, (350, HEIGHT - 28))

    def draw(self):
        screen.fill(BG_COLOR)
        self.draw_food()
        self.draw_snake()
        self.draw_ui()

        font = pygame.font.SysFont("Consolas", 18, bold=True)

        
        if self.show_life_lost_screen:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

            warn_font = pygame.font.SysFont("Consolas", 28, bold=True)
            msg1 = warn_font.render("OOPS! LIFE LOST!", True, (255, 179, 0))
            msg2 = font.render(f"Lives Remaining: {self.lives}", True, TEXT_COLOR)
            msg3 = font.render("Press 'SPACE' to Continue", True, (200, 200, 200))

            screen.blit(msg1, (WIDTH // 2 - msg1.get_width() // 2, HEIGHT // 2 - 50))
            screen.blit(msg2, (WIDTH // 2 - msg2.get_width() // 2, HEIGHT // 2))
            screen.blit(msg3, (WIDTH // 2 - msg3.get_width() // 2, HEIGHT // 2 + 40))

        
        elif self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            screen.blit(overlay, (0, 0))

            over_font = pygame.font.SysFont("Consolas", 36, bold=True)
            text = over_font.render("GAME OVER", True, (255, 82, 82))
            final_score = font.render(f"Final Score: {self.score}", True, TEXT_COLOR)
            restart_text = font.render("Press 'R' to Restart Game", True, (200, 200, 200))

            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))
            screen.blit(final_score, (WIDTH // 2 - final_score.get_width() // 2, HEIGHT // 2))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 40))

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_input()
            self.update()
            self.draw()
            clock.tick(FPS)

if __name__ == "__main__":
    game = SnakeGame()
    game.run()