import tkinter as tk
from tkinter import messagebox
import random

# -------- Setup --------
root = tk.Tk()
root.title("Rock, Paper, Scissors")
root.geometry("350x300")

choices = ["Rock", "Paper", "Scissors"]
player_score = 0
computer_score = 0

# -------- Functions --------
def play(choice):
    global player_score, computer_score
    comp_choice = random.choice(choices)
    result = ""

    if choice == comp_choice:
        result = "It's a Draw!"
    elif (choice == "Rock" and comp_choice == "Scissors") or \
         (choice == "Paper" and comp_choice == "Rock") or \
         (choice == "Scissors" and comp_choice == "Paper"):
        result = "You Win!"
        player_score += 1
    else:
        result = "Computer Wins!"
        computer_score += 1

    result_label.config(text=f"You: {choice} | Computer: {comp_choice}\n{result}")
    score_label.config(text=f"Score - You: {player_score} | Computer: {computer_score}")

def reset_game():
    global player_score, computer_score
    player_score = 0
    computer_score = 0
    result_label.config(text="Choose Rock, Paper, or Scissors")
    score_label.config(text="Score - You: 0 | Computer: 0")

def exit_game():
    root.quit()

# -------- Widgets --------
tk.Label(root, text="Rock, Paper, Scissors", font=("Arial", 16)).pack(pady=10)

btn_frame = tk.Frame(root)
btn_frame.pack()

for choice in choices:
    tk.Button(btn_frame, text=choice, font=("Arial", 12), width=10,
              command=lambda c=choice: play(c)).pack(side=tk.LEFT, padx=5)

result_label = tk.Label(root, text="Choose Rock, Paper, or Scissors", font=("Arial", 12))
result_label.pack(pady=20)

score_label = tk.Label(root, text="Score - You: 0 | Computer: 0", font=("Arial", 12))
score_label.pack(pady=5)

# -------- Menu --------
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

game_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Game", menu=game_menu)
game_menu.add_command(label="Restart", command=reset_game)
game_menu.add_separator()
game_menu.add_command(label="Exit", command=exit_game)

root.mainloop()
