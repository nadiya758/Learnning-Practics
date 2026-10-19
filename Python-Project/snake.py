import tkinter as tk
import random
from tkinter import messagebox

# Game Constants
WIDTH = 500
HEIGHT = 500
CELL_SIZE = 20
UPDATE_DELAY = 100

# Colors
BG_COLOR = "#000"
SNAKE_COLOR = "#0f0"
FOOD_COLOR = "#f00"
TEXT_COLOR = "#fff"

DIRECTIONS = {
    "Up": (0, -1),
    "Down": (0, 1),
    "Left": (-1, 0),
    "Right": (1, 0)
}

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🐍 Snake Game - Score & Lives")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(root, bg=BG_COLOR, width=WIDTH, height=HEIGHT + 40)
        self.canvas.pack()

        self.menu_bar()

        self.root.bind("<Key>", self.change_direction)

        self.init_game()
        self.update()

    def init_game(self):
        self.direction = "Right"
        self.running = True
        self.snake = [(5, 5), (4, 5), (3, 5)]
        self.food = None
        self.score = 0
        self.lives = 3

        self.place_food()
        self.draw_all()

    def menu_bar(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        game_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="Restart", command=self.restart)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.root.quit)

    def draw_all(self):
        self.canvas.delete("all")
        self.draw_score()
        self.draw_snake()
        self.draw_food()

    def draw_score(self):
        self.canvas.create_text(
            10, HEIGHT + 20, text=f"Score: {self.score}   Lives: {self.lives}",
            anchor="w", fill=TEXT_COLOR, font=("Consolas", 14)
        )

    def draw_snake(self):
        for x, y in self.snake:
            self.canvas.create_rectangle(
                x * CELL_SIZE, y * CELL_SIZE,
                (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
                fill=SNAKE_COLOR, tags="snake"
            )

    def draw_food(self):
        x, y = self.food
        self.canvas.create_oval(
            x * CELL_SIZE, y * CELL_SIZE,
            (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
            fill=FOOD_COLOR, tags="food"
        )

    def place_food(self):
        while True:
            x = random.randint(0, (WIDTH // CELL_SIZE) - 1)
            y = random.randint(0, (HEIGHT // CELL_SIZE) - 1)
            if (x, y) not in self.snake:
                self.food = (x, y)
                return

    def move(self):
        if not self.running:
            return
        dx, dy = DIRECTIONS[self.direction]
        head = self.snake[0]
        new_head = (head[0] + dx, head[1] + dy)

        # Check for collision
        if (
            new_head in self.snake or
            not (0 <= new_head[0] < WIDTH // CELL_SIZE) or
            not (0 <= new_head[1] < HEIGHT // CELL_SIZE)
        ):
            self.lives -= 1
            if self.lives == 0:
                self.game_over()
                return
            else:
                messagebox.showwarning("Oops!", f"You lost a life! Lives remaining: {self.lives}")
                self.snake = [(5, 5), (4, 5), (3, 5)]
                self.direction = "Right"
                self.draw_all()
                return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.place_food()
        else:
            self.snake.pop()

        self.draw_all()

    def update(self):
        if self.running:
            self.move()
            self.root.after(UPDATE_DELAY, self.update)

    def change_direction(self, event):
        new_dir = event.keysym
        if new_dir in DIRECTIONS:
            opposite = {
                "Up": "Down", "Down": "Up",
                "Left": "Right", "Right": "Left"
            }
            if opposite[new_dir] != self.direction:
                self.direction = new_dir

    def game_over(self):
        self.running = False
        messagebox.showinfo("Game Over", f"Game Over!\nYour final score: {self.score}")

    def restart(self):
        self.init_game()


if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
