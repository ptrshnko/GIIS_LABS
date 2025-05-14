import tkinter as tk
from tkinter import ttk
from HermiteRenderer import HermiteRenderer
from BezierRenderer import BezierRenderer
from BSplineRenderer import BSplineRenderer

class Lab3Window:
    def __init__(self, root):
        self.root = root
        self.root.title("Лабораторная работа 3: Параметрические кривые")
        self.root.geometry("300x300")
        self.root.configure(bg='lavenderblush2')

        # Header
        header_frame = tk.Frame(self.root, bg="lavenderblush2")
        header_frame.pack(fill=tk.X, pady=10)
        header_canvas = tk.Canvas(header_frame, height=60, bg="lavenderblush2", highlightthickness=0)
        header_canvas.pack(fill=tk.X, padx=10)
        header_canvas.create_rectangle(0, 0, 300, 60, fill="#d8bfd8", outline="#d8bfd8")
        header_canvas.create_text(150, 30, text="Выберите кривую", font=("Arial", 14, "bold"), fill="#4b0082")

        # Curve selection buttons
        tk.Label(self.root, text="Пожалуйста, выберите метод:", bg='lavenderblush2').pack(anchor="c", pady=10)
        ttk.Button(self.root, text="Интерполяция Эрмита", command=self.open_hermite, width=28).pack(padx=50, pady=10, anchor="c")
        ttk.Button(self.root, text="Кривая Безье", command=self.open_bezier, width=28).pack(padx=50, pady=10, anchor="c")
        ttk.Button(self.root, text="B-сплайн", command=self.open_b_spline, width=28).pack(padx=50, pady=10, anchor="c")

    def open_hermite(self):
        window = tk.Toplevel(self.root)
        HermiteRenderer(window)

    def open_bezier(self):
        window = tk.Toplevel(self.root)
        BezierRenderer(window)

    def open_b_spline(self):
        window = tk.Toplevel(self.root)
        BSplineRenderer(window)