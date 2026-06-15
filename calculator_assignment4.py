import tkinter as tk
from tkinter import messagebox


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def calculate(operation):
    try:
        x = float(entry_a.get())
        y = float(entry_b.get())
    except ValueError:
        messagebox.showerror("Input error", "Please enter valid numbers.")
        return

    try:
        if operation == "add":
            result = add(x, y)
        elif operation == "subtract":
            result = subtract(x, y)
        elif operation == "multiply":
            result = multiply(x, y)
        elif operation == "divide":
            result = divide(x, y)
        else:
            result = ""

        label_result.config(text=f"Result: {result}")
    except Exception as e:
        messagebox.showerror("Calculation error", str(e))


root = tk.Tk()
root.title("Menu-Driven GUI Calculator")
root.geometry("320x180")
root.resizable(False, False)

menu_bar = tk.Menu(root)
calc_menu = tk.Menu(menu_bar, tearoff=0)
calc_menu.add_command(label="Add", command=lambda: calculate("add"))
calc_menu.add_command(label="Subtract", command=lambda: calculate("subtract"))
calc_menu.add_command(label="Multiply", command=lambda: calculate("multiply"))
calc_menu.add_command(label="Divide", command=lambda: calculate("divide"))
calc_menu.add_separator()
calc_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="Operations", menu=calc_menu)
root.config(menu=menu_bar)

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)

label_a = tk.Label(frame, text="Value A:")
label_a.grid(row=0, column=0, sticky="e", pady=5)
entry_a = tk.Entry(frame, width=20)
entry_a.grid(row=0, column=1, pady=5)

label_b = tk.Label(frame, text="Value B:")
label_b.grid(row=1, column=0, sticky="e", pady=5)
entry_b = tk.Entry(frame, width=20)
entry_b.grid(row=1, column=1, pady=5)

label_result = tk.Label(frame, text="Result: ", anchor="w")
label_result.grid(row=2, column=0, columnspan=2, sticky="w", pady=(10, 0))

button_frame = tk.Frame(frame)
button_frame.grid(row=3, column=0, columnspan=2, pady=10)

button_add = tk.Button(button_frame, text="Add", width=8, command=lambda: calculate("add"))
button_subtract = tk.Button(button_frame, text="Subtract", width=8, command=lambda: calculate("subtract"))
button_multiply = tk.Button(button_frame, text="Multiply", width=8, command=lambda: calculate("multiply"))
button_divide = tk.Button(button_frame, text="Divide", width=8, command=lambda: calculate("divide"))

button_add.grid(row=0, column=0, padx=2)
button_subtract.grid(row=0, column=1, padx=2)
button_multiply.grid(row=0, column=2, padx=2)
button_divide.grid(row=0, column=3, padx=2)

root.mainloop()
