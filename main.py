import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
import os
import ast
import operator

# EVERYTHINGOS VERSION 1.0.0

root = tk.Tk()
root.title("EverythingOS 1.0.0")
root.geometry("1000x650")
root.minsize(700, 450)

desktop_color = "#1876ad"
root.configure(bg=desktop_color)

# Desktop
desktop = tk.Frame(root, bg=desktop_color)
desktop.pack(fill="both", expand=True)

title = tk.Label(
    desktop,
    text="EverythingOS",
    font=("Arial", 30, "bold"),
    fg="white",
    bg=desktop_color
)
title.pack(pady=25)

subtitle = tk.Label(
    desktop,
    text="Your world. Your operating system.",
    font=("Arial", 12),
    fg="white",
    bg=desktop_color
)
subtitle.pack()

def new_window(name, width=500, height=350):
    window = tk.Toplevel(root)
    window.title(name + " - EverythingOS")
    window.geometry(f"{width}x{height}")
    return window

# NOTEPAD
def notepad():
    window = new_window("Notepad", 600, 450)

    text = tk.Text(window, font=("Consolas", 12))
    text.pack(fill="both", expand=True)

    def save_file():
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")]
        )
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(text.get("1.0", "end-1c"))

    def open_file():
        path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"),
                       ("All files", "*.*")]
        )
        if path:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                text.delete("1.0", "end")
                text.insert("1.0", content)
            except Exception as error:
                messagebox.showerror("Error", str(error))

    menu = tk.Menu(window)
    file_menu = tk.Menu(menu, tearoff=0)
    file_menu.add_command(label="Open", command=open_file)
    file_menu.add_command(label="Save As", command=save_file)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=window.destroy)
    menu.add_cascade(label="File", menu=file_menu)
    window.config(menu=menu)

# CALCULATOR
def safe_calculate(expression):
    operations = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv
    }

    def evaluate(node):
        if isinstance(node, ast.Constant):
            if type(node.value) in (int, float):
                return node.value
        if isinstance(node, ast.BinOp):
            operation = operations.get(type(node.op))
            if operation:
                return operation(
                    evaluate(node.left),
                    evaluate(node.right)
                )
        if isinstance(node, ast.UnaryOp):
            if isinstance(node.op, ast.USub):
                return -evaluate(node.operand)
        raise ValueError("Invalid expression")

    if len(expression) > 100:
        raise ValueError("Expression too long")
    return evaluate(ast.parse(expression, mode="eval").body)

def calculator():
    window = new_window("Calculator", 300, 400)
    expression = tk.StringVar()

    entry = tk.Entry(
        window,
        textvariable=expression,
        font=("Arial", 22),
        justify="right"
    )
    entry.pack(fill="x", padx=10, pady=15)

    def press(value):
        if value == "C":
            expression.set("")
        elif value == "=":
            try:
                result = safe_calculate(expression.get())
                expression.set(str(result))
            except Exception:
                expression.set("Error")
        else:
            if expression.get() == "Error":
                expression.set("")
            expression.set(expression.get() + value)

    buttons = [
        ["7", "8", "9", "/"],
        ["4", "5", "6", "*"],
        ["1", "2", "3", "-"],
        ["C", "0", "=", "+"]
    ]

    frame = tk.Frame(window)
    frame.pack(fill="both", expand=True)

    for row_index, row in enumerate(buttons):
        frame.rowconfigure(row_index, weight=1)
        for col_index, value in enumerate(row):
            frame.columnconfigure(col_index, weight=1)
            tk.Button(
                frame,
                text=value,
                font=("Arial", 16),
                command=lambda v=value: press(v)
            ).grid(
                row=row_index,
                column=col_index,
                sticky="nsew",
                padx=3,
                pady=3
            )

# FILE EXPLORER
def explorer():
    window = new_window("File Explorer", 650, 450)

    path_label = tk.Label(window, text="", anchor="w")
    path_label.pack(fill="x")

    files = tk.Listbox(window, font=("Consolas", 11))
    files.pack(fill="both", expand=True)

    current_path = [os.path.expanduser("~")]

    def show_folder(path):
        try:
            names = sorted(os.listdir(path))
            files.delete(0, "end")
            files.insert("end", "[..] Parent Folder")
            for name in names:
                full_path = os.path.join(path, name)
                prefix = "[DIR] " if os.path.isdir(full_path) else "[FILE] "
                files.insert("end", prefix + name)
            current_path[0] = path
            path_label.config(text=path)
        except Exception as error:
            messagebox.showerror("Explorer", str(error))

    def open_selected(event=None):
        selection = files.curselection()
        if not selection:
            return

        index = selection[0]
        if index == 0:
            show_folder(os.path.dirname(current_path[0]))
            return

        name = files.get(index)[6:]
        path = os.path.join(current_path[0], name)

        if os.path.isdir(path):
            show_folder(path)
        else:
            messagebox.showinfo("File", path)

    files.bind("<Double-Button-1>", open_selected)
    show_folder(current_path[0])

# SETTINGS
def settings():
    window = new_window("Settings", 400, 350)

    tk.Label(
        window,
        text="EverythingOS Settings",
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    tk.Label(window, text="Desktop Background").pack(pady=10)

    colors = {
        "Blue": "#1876ad",
        "Purple": "#6941a5",
        "Green": "#16855b",
        "Dark": "#20242c",
        "Pink": "#ad4889"
    }

    def change_color(color):
        global desktop_color
        desktop_color = color
        desktop.config(bg=color)
        title.config(bg=color)
        subtitle.config(bg=color)

    for name, color in colors.items():
        tk.Button(
            window,
            text=name,
            command=lambda c=color: change_color(c)
        ).pack(fill="x", padx=40, pady=3)

# ABOUT
def about():
    messagebox.showinfo(
        "About EverythingOS",
        "EverythingOS v1.0.0\n"
        "Created by Heitor\n"
        "Made with Python\n\n"
        "Welcome to EverythingOS!"
    )

# START MENU
start_menu = None

def toggle_start():
    global start_menu

    if start_menu is not None and start_menu.winfo_exists():
        start_menu.destroy()
        start_menu = None
        return

    start_menu = tk.Toplevel(root)
    start_menu.title("Start")
    start_menu.geometry("270x390")
    start_menu.configure(bg="#242a38")

    tk.Label(
        start_menu,
        text="EverythingOS",
        bg="#242a38",
        fg="white",
        font=("Arial", 19, "bold")
    ).pack(pady=15)

    apps = [
        ("File Explorer", explorer),
        ("Notepad", notepad),
        ("Calculator", calculator),
        ("Settings", settings),
        ("About EverythingOS", about),
        ("Shutdown", root.destroy)
    ]

    for name, function in apps:
        def launch(action=function):
            global start_menu
            if start_menu and start_menu.winfo_exists():
                start_menu.destroy()
                start_menu = None
            action()

        tk.Button(
            start_menu,
            text=name,
            font=("Arial", 11),
            command=launch
        ).pack(fill="x", padx=15, pady=4)

# DESKTOP SHORTCUTS
shortcuts = tk.Frame(desktop, bg=desktop_color)
shortcuts.pack(pady=35)

tk.Button(
    shortcuts,
    text="File Explorer",
    width=16,
    height=3,
    command=explorer
).grid(row=0, column=0, padx=10, pady=10)

tk.Button(
    shortcuts,
    text="Notepad",
    width=16,
    height=3,
    command=notepad
).grid(row=0, column=1, padx=10, pady=10)

tk.Button(
    shortcuts,
    text="Calculator",
    width=16,
    height=3,
    command=calculator
).grid(row=1, column=0, padx=10, pady=10)

tk.Button(
    shortcuts,
    text="Settings",
    width=16,
    height=3,
    command=settings
).grid(row=1, column=1, padx=10, pady=10)

# TASKBAR
taskbar = tk.Frame(root, bg="#202633", height=50)
taskbar.pack(side="bottom", fill="x")
taskbar.pack_propagate(False)

tk.Button(
    taskbar,
    text="Start",
    font=("Arial", 12, "bold"),
    command=toggle_start
).pack(side="left", padx=10, pady=7)

clock = tk.Label(
    taskbar,
    fg="white",
    bg="#202633",
    font=("Arial", 12)
)
clock.pack(side="right", padx=15)

def update_clock():
    clock.config(
        text=datetime.now().strftime("%H:%M:%S")
    )
    root.after(1000, update_clock)

update_clock()

root.mainloop()
