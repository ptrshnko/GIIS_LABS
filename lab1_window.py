import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from line_renderer import DDALineRenderer, BresenhamLineRenderer, WuLineRenderer

class LineDrawingWindow:
    def __init__(self, window):
        self.window = window
        self.window.title("Рисование отрезка")
        self.window.geometry("800x600")
        self.window.configure(bg='lavenderblush2')
        self.is_drawing = tk.BooleanVar(value=False)

        # Input fields
        tk.Label(self.window, text="x0 (0–100)", bg='lavenderblush2').grid(row=0, column=0, padx=5, pady=5)
        self.entry_x0 = tk.Entry(self.window)
        self.entry_x0.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.window, text="y0 (0–100)", bg='lavenderblush2').grid(row=1, column=0, padx=5, pady=5)
        self.entry_y0 = tk.Entry(self.window)
        self.entry_y0.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.window, text="x1 (0–100)", bg='lavenderblush2').grid(row=2, column=0, padx=5, pady=5)
        self.entry_x1 = tk.Entry(self.window)
        self.entry_x1.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.window, text="y1 (0–100)", bg='lavenderblush2').grid(row=3, column=0, padx=5, pady=5)
        self.entry_y1 = tk.Entry(self.window)
        self.entry_y1.grid(row=3, column=1, padx=5, pady=5)

        # Method selection
        self.method_var = tk.StringVar(value="DDA")
        tk.Label(self.window, text="Метод:", bg='lavenderblush2').grid(row=4, column=0, columnspan=2, pady=10)
        tk.Radiobutton(self.window, text="ЦДА", variable=self.method_var, value="DDA", bg='lavenderblush2').grid(row=5, column=0, columnspan=2, sticky="w")
        tk.Radiobutton(self.window, text="Брезенхэм", variable=self.method_var, value="Bresenham", bg='lavenderblush2').grid(row=6, column=0, columnspan=2, sticky="w")
        tk.Radiobutton(self.window, text="Ву", variable=self.method_var, value="Wu", bg='lavenderblush2').grid(row=7, column=0, columnspan=2, sticky="w")

        # Debug mode
        self.debug_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self.window, text="Режим отладки", variable=self.debug_var, bg='lavenderblush2').grid(row=8, column=0, columnspan=2, pady=10)

        # Buttons
        self.draw_button = ttk.Button(self.window, text="Нарисовать", command=self.draw_line)
        self.draw_button.grid(row=9, column=0, columnspan=2, pady=10)
        ttk.Button(self.window, text="Очистить холст", command=self.clear_canvas).grid(row=10, column=0, columnspan=2, pady=10)

        # Canvas
        fig, ax = plt.subplots(figsize=(5, 5))
        self.canvas = FigureCanvasTkAgg(fig, master=self.window)
        self.canvas.get_tk_widget().grid(row=0, column=2, rowspan=11, padx=10, pady=10)
        self.window.fig, self.window.ax, self.window.canvas = fig, ax, self.canvas
        self.clear_canvas()

    def clear_canvas(self):
        self.window.ax.clear()
        self.window.ax.set_xticks(np.arange(0, 101, 10))
        self.window.ax.set_yticks(np.arange(0, 101, 10))
        self.window.ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        self.window.canvas.draw()

    def draw_line(self):
        if self.is_drawing.get():
            messagebox.showinfo("Информация", "Рисование уже в процессе")
            return
        self.is_drawing.set(True)
        self.draw_button.config(state='disabled')
        try:
            if not all([self.entry_x0.get(), self.entry_y0.get(), self.entry_x1.get(), self.entry_y1.get()]):
                raise ValueError("Все поля должны быть заполнены")

            x0, y0 = float(self.entry_x0.get()), float(self.entry_y0.get())
            x1, y1 = float(self.entry_x1.get()), float(self.entry_y1.get())

            if not (0 <= x0 <= 100 and 0 <= y0 <= 100 and 0 <= x1 <= 100 and 0 <= y1 <= 100):
                raise ValueError("Координаты должны быть от 0 до 100")

            renderers = {"DDA": DDALineRenderer, "Bresenham": BresenhamLineRenderer, "Wu": WuLineRenderer}
            renderer = renderers[self.method_var.get()]()
            result = renderer.render_line(x0, y0, x1, y1, self.debug_var.get())

            self.clear_canvas()
            if self.debug_var.get():
                for grid in result:
                    self.window.ax.imshow(grid, extent=[0, 100, 0, 100], origin='lower', cmap='gray_r', vmin=0, vmax=1)
                    self.window.canvas.draw()
                    self.window.update()
                    self.window.after(500)
            else:
                self.window.ax.imshow(result, extent=[0, 100, 0, 100], origin='lower', cmap='gray_r', vmin=0, vmax=1)
                self.window.canvas.draw()
        except ValueError as e:
            messagebox.showerror("Ошибка ввода", str(e))
        finally:
            self.is_drawing.set(False)
            self.draw_button.config(state='normal')