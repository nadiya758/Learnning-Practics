import tkinter as tk

# Create the main window
root = tk.Tk()

# Set window title
root.title("Tkinter Introduction")

# Set window size (width x height)
root.geometry("300x200")


# Create a label widget
label = tk.Label(root, text="Hello, Tkinter!", font=("Arial", 16))
label.pack(pady=20)  # Pack the label with some padding

# Function to change the text on button click
def change_text():
    label.config(text="Button Clicked!")

# Create a button widget
button = tk.Button(root, text="Click Me", font=("Arial", 14), command=change_text)
button.pack(pady=10)  # Pack the button with some padding

# Start the Tkinter event loop (this keeps the window open)
root.mainloop()



























































































































