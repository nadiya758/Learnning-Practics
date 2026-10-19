import tkinter as tk
from tkinter import messagebox
import random

# -------- Setup --------
root = tk.Tk()
root.title("Number Guessing Game")
root.geometry("350x250")

secret_number = random.randint(1, 100)
attempts = 0

# -------- Functions --------
def check_guess():
    global attempts
    try:
        guess = int(entry.get())
    except ValueError:
        messagebox.showwarning("Invalid", "Please enter a number!")
        return

    attempts += 1
    if guess == secret_number:
        messagebox.showinfo("Correct!", f"Congratulations! You guessed it in {attempts} tries.")
        disable_game()
        #reset_game()
    elif guess < secret_number:
        result_label.config(text="Too low! Try again.")
    else:
        result_label.config(text="Too high! Try again.")
    entry.delete(0, tk.END)

def reset_game():
    global secret_number, attempts
    secret_number = random.randint(1, 100)
    attempts = 0
    result_label.config(text="Guess a number between 1 and 100")
    entry.config(state="normal")
    submit_btn.config(state="normal")

def disable_game():
    entry.config(state="disabled")
    submit_btn.config(state="disabled")

def exit_game():
    root.quit()

# -------- Widgets --------
tk.Label(root, text="Guess the Number", font=("Arial", 16)).pack(pady=10)

entry = tk.Entry(root, font=("Arial", 14))
entry.pack(pady=5)

submit_btn = tk.Button(root, text="Submit Guess", font=("Arial", 12), command=check_guess)
submit_btn.pack(pady=5)

result_label = tk.Label(root, text="Guess a number between 1 and 100", font=("Arial", 12))
result_label.pack(pady=10)

# -------- Menu --------
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

game_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Game", menu=game_menu)
game_menu.add_command(label="Restart", command=reset_game)
game_menu.add_separator()
game_menu.add_command(label="Exit", command=exit_game)

root.mainloop()
