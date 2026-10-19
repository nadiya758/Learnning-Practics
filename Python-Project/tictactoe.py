import tkinter as tk
from tkinter import messagebox

# ---------- Game Setup ----------
root = tk.Tk()
root.title("Tic Tac Toe")
root.geometry("350x400")
root.resizable(False, False)

current_player = "X"
board = [["" for _ in range(3)] for _ in range(3)]
buttons = [[None for _ in range(3)] for _ in range(3)]

# ---------- Game Functions ----------
def play_move(row, col):
    global current_player
    if board[row][col] == "":
        board[row][col] = current_player
        buttons[row][col].config(text=current_player, state="disabled")
        if check_winner(current_player):
            messagebox.showinfo("Game Over", f"Player {current_player} wins!")
            disable_all_buttons()
        elif is_draw():
            messagebox.showinfo("Game Over", "It's a draw!")
            disable_all_buttons()
        else:
            current_player = "O" if current_player == "X" else "X"

def check_winner(player):
    # Rows & Columns
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or \
           all(board[j][i] == player for j in range(3)):
            return True
    # Diagonals
    if all(board[i][i] == player for i in range(3)) or \
       all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def is_draw():
    return all(board[i][j] != "" for i in range(3) for j in range(3))

def disable_all_buttons():
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(state="disabled")

def reset_game():
    global current_player, board
    current_player = "X"
    board = [["" for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text="", state="normal")

def exit_game():
    root.quit()

# ---------- GUI Layout ----------
frame = tk.Frame(root)
frame.pack(pady=20)

for i in range(3):
    for j in range(3):
        btn = tk.Button(frame, text="", font=("Arial", 20), width=5, height=2,
                        command=lambda row=i, col=j: play_move(row, col))
        btn.grid(row=i, column=j, padx=5, pady=5)
        buttons[i][j] = btn

# ---------- Menu ----------
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

game_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Game", menu=game_menu)
game_menu.add_command(label="Play / Restart", command=reset_game)
game_menu.add_separator()
game_menu.add_command(label="Exit", command=exit_game)

# ---------- Mainloop ----------
root.mainloop()
