import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import math

# --------- Functions ---------
def press(key):
    expression.set(expression.get() + str(key))

def clear():
    expression.set("")

def backspace():
    expression.set(expression.get()[:-1])

def calculate():
    try:
        expr = expression.get().replace('√', 'math.sqrt')
        expr = expr.replace('π', 'math.pi').replace('e', 'math.e')
        result = str(eval(expr, {'math': math, '__builtins__': None}, vars(math)))
        expression.set(result)
        history_box.insert(tk.END, f"{expr} = {result}\n")
        history_box.see(tk.END)
    except Exception as e:
        messagebox.showerror("Error", f"Invalid Expression\n{e}")

def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    bg = "#222" if dark_mode else "#fff"
    fg = "#eee" if dark_mode else "#000"
    entry.config(bg=bg, fg=fg, insertbackground=fg)
    history_box.config(bg=bg, fg=fg)
    for child in btn_frame.winfo_children():
        child.config(bg=bg, fg=fg)

def exit_app():
    root.quit()

# --------- Setup ---------
root = tk.Tk()
root.title("Scientific Calculator")
root.geometry("480x600")
root.resizable(False, False)

expression = tk.StringVar()
dark_mode = False

# --------- Entry ---------
entry = tk.Entry(root, textvariable=expression, font=("Consolas", 20), bd=5, relief="sunken", justify="right")
entry.pack(fill="x", padx=10, pady=10, ipady=10)

# --------- Button Grid ---------
btn_frame = tk.Frame(root)
btn_frame.pack()

buttons = [
    ['7', '8', '9', '/', 'C'],
    ['4', '5', '6', '*', '⌫'],
    ['1', '2', '3', '-', '('],
    ['0', '.', '%', '+', ')'],
    ['π', 'e', '√(', '**', '='],
    ['sin(', 'cos(', 'tan(', 'log(', 'exp('],
]

for r, row in enumerate(buttons):
    for c, char in enumerate(row):
        action = (lambda ch=char: press(ch)) if char not in ['C', '=', '⌫'] else \
                 (clear if char == 'C' else calculate if char == '=' else backspace)
        btn = tk.Button(btn_frame, text=char, width=7, height=2, font=("Consolas", 14), command=action)
        btn.grid(row=r, column=c, padx=3, pady=3)

# --------- History Box ---------
tk.Label(root, text="History", font=("Arial", 12)).pack(pady=5)
history_box = scrolledtext.ScrolledText(root, height=6, font=("Consolas", 12), state="normal")
history_box.pack(fill="both", padx=10, pady=5)

# --------- Menu Bar ---------
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Options", menu=menu)
menu.add_command(label="Clear", command=clear)
menu.add_command(label="Toggle Theme", command=toggle_theme)
menu.add_separator()
menu.add_command(label="Exit", command=exit_app)

root.mainloop()        