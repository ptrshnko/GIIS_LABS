import tkinter as tk
from tkinter import ttk, messagebox
from polygon_filler import PolygonFiller

class Lab56Window:
    def __init__(self, root):
        self.root = root
        self.root.title("Лабораторная работа 5: Работа с полигонами")
        self.root.geometry("900x600")
        self.root.configure(bg='lavenderblush2')

        # Input Frame
        input_frame = tk.Frame(self.root, bg='lavenderblush2')
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Title
        tk.Label(input_frame, text="Работа с полигонами", bg='lavenderblush2', font=("Segoe UI", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        # Description
        tk.Label(input_frame, text="Редактирование и заполнение полигонов", bg='lavenderblush2', wraplength=250).grid(row=1, column=0, columnspan=2, pady=5)

        # Status Bar
        self.status_var = tk.StringVar()
        self.status_var.set("Готов к работе")
        tk.Label(self.root, textvariable=self.status_var, bg='lavenderblush2', relief=tk.SUNKEN, anchor=tk.W).grid(row=1, column=0, columnspan=2, sticky='ew', pady=5)

        # Initialize PolygonFiller
        self.editor = PolygonFiller(self.root, self.status_var)
        self.status_var.set("Редактор полигонов активен")