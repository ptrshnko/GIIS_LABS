import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from transform3d import Transform3DRenderer

class Lab4Window:
    def __init__(self, root):
        self.root = root
        self.root.title("Лабораторная работа 4: Преобразования 3D")
        self.root.geometry("900x600")
        self.root.configure(bg='lavenderblush2')

        self.renderer = None
        self.canvas_width = 600
        self.canvas_height = 500

        # Параметры преобразований
        self.trans_x_val = tk.DoubleVar(value=0)
        self.trans_y_val = tk.DoubleVar(value=0)
        self.trans_z_val = tk.DoubleVar(value=0)
        self.rot_x_val = tk.DoubleVar(value=0)
        self.rot_y_val = tk.DoubleVar(value=0)
        self.rot_z_val = tk.DoubleVar(value=0)
        self.scale_val = tk.DoubleVar(value=1)
        self.persp_dist_val = tk.DoubleVar(value=5)
        self.reflect = False

        # Фрейм ввода
        input_frame = tk.Frame(self.root, bg='lavenderblush2')
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Заголовок
        tk.Label(input_frame, text="3D Object Transformations", bg='lavenderblush2', font=("Segoe UI", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        # Ввод файла
        ttk.Button(input_frame, text="Загрузить объект", command=self.load_object).grid(row=1, column=0, columnspan=2, pady=5)
        ttk.Button(input_frame, text="Сбросить", command=self.reset_object).grid(row=2, column=0, columnspan=2, pady=5)

        # Ползунки для преобразований
        tk.Label(input_frame, text="Смещение", bg='lavenderblush2').grid(row=3, column=0, columnspan=2, pady=5)
        self.trans_x = self.create_slider(input_frame, "X", -2, 2, self.trans_x_val, 4)
        self.trans_y = self.create_slider(input_frame, "Y", -2, 2, self.trans_y_val, 5)
        self.trans_z = self.create_slider(input_frame, "Z", -2, 2, self.trans_z_val, 6)

        tk.Label(input_frame, text="Вращение (°)", bg='lavenderblush2').grid(row=7, column=0, columnspan=2, pady=5)
        self.rot_x = self.create_slider(input_frame, "X", -180, 180, self.rot_x_val, 8)
        self.rot_y = self.create_slider(input_frame, "Y", -180, 180, self.rot_y_val, 9)
        self.rot_z = self.create_slider(input_frame, "Z", -180, 180, self.rot_z_val, 10)

        tk.Label(input_frame, text="Масштаб", bg='lavenderblush2').grid(row=11, column=0, columnspan=2, pady=5)
        self.scale = self.create_slider(input_frame, "Коэффициент", 0.1, 2, self.scale_val, 12, resolution=0.1)

        tk.Label(input_frame, text="Перспектива", bg='lavenderblush2').grid(row=13, column=0, columnspan=2, pady=5)
        self.persp_dist = self.create_slider(input_frame, "Дистанция", 1, 10, self.persp_dist_val, 14, resolution=0.1)

        # Флажок отражения
        self.reflect_var = tk.BooleanVar(value=False)
        tk.Checkbutton(input_frame, text="Отражение (YZ)", variable=self.reflect_var, bg='lavenderblush2', command=self.update_display).grid(row=15, column=0, columnspan=2, pady=5)

        # Холст
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg='white')
        self.canvas.grid(row=0, column=1, padx=10, pady=10)

        # Привязка событий клавиатуры
        self.root.bind('<KeyPress>', self.handle_keypress)

        # Обновление отображения изначально
        self.update_display()

    def create_slider(self, parent, label, min_val, max_val, var, row, resolution=1):
        tk.Label(parent, text=f"{label}:", bg='lavenderblush2').grid(row=row, column=0, padx=5, pady=2, sticky='e')
        slider = ttk.Scale(parent, from_=min_val, to=max_val, orient='horizontal', variable=var, command=lambda x: self.update_display())
        slider.grid(row=row, column=1, padx=5, pady=2, sticky='w')
        return slider

    def handle_keypress(self, event):
        step = 0.1  # Шаг для перемещения
        angle_step = 5  # Шаг для поворота в градусах
        scale_step = 0.1  # Шаг для масштабирования
        persp_step = 0.5  # Шаг для расстояния перспективы

        if event.keysym == 'Right':
            self.trans_x_val.set(self.trans_x_val.get() + step)
        elif event.keysym == 'Left':
            self.trans_x_val.set(self.trans_x_val.get() - step)
        elif event.keysym == 'Up':
            self.trans_y_val.set(self.trans_y_val.get() + step)
        elif event.keysym == 'Down':
            self.trans_y_val.set(self.trans_y_val.get() - step)
        elif event.keysym == 'w':
            self.trans_z_val.set(self.trans_z_val.get() + step)
        elif event.keysym == 's':
            self.trans_z_val.set(self.trans_z_val.get() - step)
        elif event.keysym == 'q':
            self.rot_x_val.set(self.rot_x_val.get() + angle_step)
        elif event.keysym == 'e':
            self.rot_x_val.set(self.rot_x_val.get() - angle_step)
        elif event.keysym == 'a':
            self.rot_y_val.set(self.rot_y_val.get() + angle_step)
        elif event.keysym == 'd':
            self.rot_y_val.set(self.rot_y_val.get() - angle_step)
        elif event.keysym == 'z':
            self.rot_z_val.set(self.rot_z_val.get() + angle_step)
        elif event.keysym == 'c':
            self.rot_z_val.set(self.rot_z_val.get() - angle_step)
        elif event.keysym == 't':
            self.scale_val.set(min(self.scale_val.get() + scale_step, 2))
        elif event.keysym == 'g':
            self.scale_val.set(max(self.scale_val.get() - scale_step, 0.1))
        elif event.keysym == 'r':
            self.reflect = not self.reflect
            self.reflect_var.set(self.reflect)
        elif event.keysym == 'p':
            self.persp_dist_val.set(min(self.persp_dist_val.get() + persp_step, 10))
        elif event.keysym == 'o':
            self.persp_dist_val.set(max(self.persp_dist_val.get() - persp_step, 1))
        elif event.keysym == 'space':
            self.reset_object()
            return

        self.update_display()

    def load_object(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not file_path:
            return
        try:
            self.renderer = Transform3DRenderer.from_file(file_path)
            self.reset_object()
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {str(e)}")

    def reset_object(self):
        if self.renderer:
            self.renderer.reset()
        self.trans_x_val.set(0)
        self.trans_y_val.set(0)
        self.trans_z_val.set(0)
        self.rot_x_val.set(0)
        self.rot_y_val.set(0)
        self.rot_z_val.set(0)
        self.scale_val.set(1)
        self.persp_dist_val.set(5)
        self.reflect = False
        self.reflect_var.set(False)
        self.update_display()

    def update_display(self, *args):
        if not self.renderer:
            return
        self.renderer.reset()

        # Применение преобразований
        self.renderer.scale_object(self.scale_val.get(), self.scale_val.get(), self.scale_val.get())
        self.renderer.rotate_x(self.rot_x_val.get())
        self.renderer.rotate_y(self.rot_y_val.get())
        self.renderer.rotate_z(self.rot_z_val.get())
        self.renderer.shift(self.trans_x_val.get(), self.trans_y_val.get(), self.trans_z_val.get())
        if self.reflect:
            self.renderer.mirror_yz()
        self.renderer.apply_perspective(self.persp_dist_val.get())

        self.render_canvas()

    def render_canvas(self):
        self.canvas.delete('all')
        if not self.renderer:
            return
        points = self.renderer.project_to_2d(self.canvas_width, self.canvas_height)
        for edge in self.renderer.get_edges():
            x0, y0 = points[edge[0]]
            x1, y1 = points[edge[1]]
            self.canvas.create_line(x0, y0, x1, y1, fill='black', width=2)