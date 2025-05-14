import tkinter as tk
from tkinter import messagebox
import numpy as np
from math import atan2

class Point:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __eq__(self, other):
        return isinstance(other, Point) and abs(self.x - other.x) < 1e-6 and abs(self.y - other.y) < 1e-6

    def __repr__(self):
        return f"Точка({self.x}, {self.y})"

class Edge:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __repr__(self):
        return f"Ребро({self.p1}, {self.p2})"

class PolygonModel:
    def __init__(self):
        self.points = []
        self.edges = []

    def add_point(self, x, y):
        point = Point(x, y)
        self.points.append(point)
        if len(self.points) > 1:
            self.edges.append(Edge(self.points[-2], self.points[-1]))
        return point

    def close_polygon(self):
        if len(self.points) < 3:
            raise ValueError("Для замыкания полигона нужно не менее 3 точек")
        self.edges.append(Edge(self.points[-1], self.points[0]))

    def clear(self):
        self.points.clear()
        self.edges.clear()

    def check_self_intersection(self):
        n = len(self.points)
        for i in range(n):
            for j in range(i + 2, n):
                if i == 0 and j == n - 1:
                    continue
                p1, p2 = self.points[i], self.points[(i + 1) % n]
                q1, q2 = self.points[j], self.points[(j + 1) % n]
                def ccw(A, B, C):
                    return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)
                if (ccw(p1, q1, q2) != ccw(p2, q1, q2) and
                    ccw(p1, p2, q1) != ccw(p1, p2, q2)):
                    return True
        return False

    def check_convexity(self):
        if len(self.points) < 3:
            raise ValueError("Слишком мало точек для проверки выпуклости")
        if self.check_self_intersection():
            return False
        is_convex = True
        n = len(self.points)
        for i in range(n):
            p1 = self.points[i]
            p2 = self.points[(i + 1) % n]
            p3 = self.points[(i + 2) % n]
            cross_product = (p2.x - p1.x) * (p3.y - p2.y) - (p2.y - p1.y) * (p3.x - p2.x)
            if i == 0:
                sign = np.sign(cross_product)
            elif np.sign(cross_product) != sign and cross_product != 0:
                is_convex = False
                break
        return is_convex

    def build_hull_graham(self):
        if len(self.points) < 3:
            raise ValueError("Недостаточно точек для построения выпуклой оболочки")
        def cross(o, a, b):
            return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x)
        pts = self.points[:]
        bottom = min(range(len(pts)), key=lambda i: (pts[i].y, pts[i].x))
        pts[0], pts[bottom] = pts[bottom], pts[0]
        pivot = pts[0]
        pts = pts[1:]
        pts.sort(key=lambda p: (atan2(p.y - pivot.y, p.x - pivot.x), (p.x - pivot.x)**2 + (p.y - pivot.y)**2))
        stack = [pivot, pts[0]]
        for p in pts[1:]:
            while len(stack) > 1 and cross(stack[-2], stack[-1], p) <= 0:
                stack.pop()
            stack.append(p)
        return stack

    def build_hull_jarvis(self):
        if len(self.points) < 3:
            raise ValueError("Недостаточно точек для построения выпуклой оболочки")
        pts = self.points[:]
        n = len(pts)
        bottom = min(range(n), key=lambda i: (pts[i].y, pts[i].x))
        hull = []
        p = bottom
        while True:
            hull.append(pts[p])
            endpoint = (p + 1) % n
            for j in range(n):
                if j == p:
                    continue
                cross = (pts[endpoint].x - pts[p].x) * (pts[j].y - pts[p].y) - (pts[endpoint].y - pts[p].y) * (pts[j].x - pts[p].x)
                if cross < 0:
                    endpoint = j
            p = endpoint
            if p == bottom:
                break
        return hull

    def find_intersections(self, line_p1, line_p2):
        if not self.edges:
            raise ValueError("Недостаточно ребер для поиска пересечений")
        normals = []
        n = len(self.points)
        for i in range(n):
            p1, p2 = self.points[i], self.points[(i + 1) % n]
            dx, dy = p2.x - p1.x, p2.y - p1.y
            normal = (-dy, dx)
            p3 = self.points[(i + 2) % n]
            cross = (p2.x - p1.x) * (p3.y - p2.y) - (p2.y - p1.y) * (p3.x - p2.x)
            if cross < 0:
                normal = (dy, -dx)
            normals.append(normal)
        intersections = []
        l1_p1, l1_p2 = line_p1, line_p2
        for side_idx in range(n):
            p1, p2 = self.points[side_idx], self.points[(side_idx + 1) % n]
            normal = normals[side_idx]
            D = (l1_p2.x - l1_p1.x, l1_p2.y - l1_p1.y)
            W = (l1_p1.x - p1.x, l1_p1.y - p1.y)
            denom = normal[0] * D[0] + normal[1] * D[1]
            if abs(denom) < 1e-6:
                continue
            t = -(normal[0] * W[0] + normal[1] * W[1]) / denom
            if 0 <= t <= 1:
                x = l1_p1.x + t * D[0]
                y = l1_p1.y + t * D[1]
                if (min(p1.x, p2.x) <= x <= max(p1.x, p2.x) and
                        min(p1.y, p2.y) <= y <= max(p1.y, p2.y)):
                    intersections.append(Point(x, y))
        return intersections

    def get_normals(self):
        if not self.edges:
            raise ValueError("Недостаточно ребер для вычисления нормалей")
        normals = []
        n = len(self.points)
        for i in range(n):
            p1, p2 = self.points[i], self.points[(i + 1) % n]
            dx, dy = p2.x - p1.x, p2.y - p1.y
            normal = (-dy, dx)
            p3 = self.points[(i + 2) % n]
            cross = (p2.x - p1.x) * (p3.y - p2.y) - (p2.y - p1.y) * (p3.x - p2.x)
            if cross < 0:
                normal = (dy, -dx)
            length = np.sqrt(normal[0]**2 + normal[1]**2)
            if length > 0:
                normal = (normal[0] / length * 20, normal[1] / length * 20)
            normals.append(normal)
        return normals

    def is_inside(self, x, y):
        point = Point(x, y)
        inside = False
        n = len(self.points)
        for i in range(n):
            p1, p2 = self.points[i], self.points[(i + 1) % n]
            if p1.y == p2.y:
                continue
            if min(p1.y, p2.y) < point.y <= max(p1.y, p2.y):
                if p1.y != p2.y:
                    x_intersect = p1.x + (point.y - p1.y) * (p2.x - p1.x) / (p2.y - p1.y)
                    if x_intersect == point.x and point.y == min(p1.y, p2.y):
                        return False
                    if x_intersect > point.x:
                        inside = not inside
        return inside

    def ordered_edge_list_fill(self, debug=False):
        if len(self.points) < 3:
            raise ValueError("Нужно 3+ точки для заполнения")
        min_y = min(p.y for p in self.points)
        max_y = max(p.y for p in self.points)
        edge_list = []
        n = len(self.points)
        for i in range(n):
            p1, p2 = self.points[i], self.points[(i + 1) % n]
            if p1.y == p2.y:
                continue
            y_start = min(p1.y, p2.y)
            y_end = max(p1.y, p2.y)
            x_start = p1.x if p1.y < p2.y else p2.x
            dx = (p2.x - p1.x) / (p2.y - p1.y) if p1.y != p2.y else 0
            for y in range(int(y_start), int(y_end)):
                x = x_start + dx * (y - y_start)
                edge_list.append((x, y))
        edge_list.sort(key=lambda p: (p[1], p[0]))
        pixels = []
        debug_steps = []
        i = 0
        while i < len(edge_list):
            if i + 1 >= len(edge_list):
                break
            x1, y1 = edge_list[i]
            x2, y2 = edge_list[i + 1]
            if y1 != y2:
                i += 1
                continue
            step_pixels = []
            for x in range(int(x1), int(x2) + 1):
                step_pixels.append(Point(x, y1))
            pixels.extend(step_pixels)
            if debug:
                debug_steps.append(step_pixels)
            i += 2
        return debug_steps if debug else pixels

    def active_edge_list_fill(self, debug=False):
        if len(self.points) < 3:
            raise ValueError("Нужно 3+ точки для заполнения")
        min_y = min(p.y for p in self.points)
        max_y = max(p.y for p in self.points)
        n = len(self.points)
        y_groups = {}
        for i in range(n):
            p1, p2 = self.points[i], self.points[(i + 1) % n]
            if p1.y == p2.y:
                continue
            y_start = min(p1.y, p2.y)
            y_end = max(p1.y, p2.y)
            x_start = p1.x if p1.y < p2.y else p2.x
            dx = (p2.x - p1.x) / (p2.y - p1.y) if p1.y != p2.y else 0
            edge = (x_start, dx, y_end)
            if y_start not in y_groups:
                y_groups[y_start] = []
            y_groups[y_start].append(edge)
        active_edges = []
        debug_steps = []
        pixels = []
        for y in range(int(min_y), int(max_y) + 1):
            if y in y_groups:
                active_edges.extend(y_groups[y])
            active_edges = [e for e in active_edges if e[2] > y]
            active_edges.sort(key=lambda e: e[0])
            step_pixels = []
            i = 0
            while i < len(active_edges) - 1:
                x1, dx1, y_max1 = active_edges[i]
                x2, dx2, y_max2 = active_edges[i + 1]
                for x in range(int(x1), int(x2) + 1):
                    step_pixels.append(Point(x, y))
                i += 2
            active_edges = [(x + dx, dx, y_max) for x, dx, y_max in active_edges]
            if step_pixels:
                pixels.extend(step_pixels)
                if debug:
                    debug_steps.append(step_pixels)
        return debug_steps if debug else pixels

    def simple_seed_fill(self, seed_point, debug=False):
        if not self.is_inside(seed_point.x, seed_point.y):
            raise ValueError("Затравочная точка должна быть внутри полигона")
        stack = [seed_point]
        filled_pixels = set()
        debug_steps = []
        while stack:
            current_step = []
            point = stack.pop()
            x, y = point.x, point.y
            if (x, y) in filled_pixels:
                continue
            filled_pixels.add((x, y))
            current_step.append(Point(x, y))
            neighbors = [Point(x+1, y), Point(x-1, y), Point(x, y+1), Point(x, y-1)]
            for neighbor in neighbors:
                if self.is_inside(neighbor.x, neighbor.y) and (neighbor.x, neighbor.y) not in filled_pixels:
                    stack.append(neighbor)
            if current_step and debug:
                debug_steps.append(current_step)
        return debug_steps if debug else [Point(x, y) for x, y in filled_pixels]

    def scanline_seed_fill(self, seed_point, debug=False):
        if not self.is_inside(seed_point.x, seed_point.y):
            raise ValueError("Затравочная точка должна быть внутри полигона")
        stack = [seed_point]
        filled_pixels = set()
        debug_steps = []
        while stack:
            current_step = []
            point = stack.pop()
            x, y = point.x, point.y
            if (x, y) in filled_pixels:
                continue
            x_left = x
            while self.is_inside(x_left, y) and (x_left, y) not in filled_pixels:
                filled_pixels.add((x_left, y))
                current_step.append(Point(x_left, y))
                x_left -= 1
            x_left += 1
            x_right = x + 1
            while self.is_inside(x_right, y) and (x_right, y) not in filled_pixels:
                filled_pixels.add((x_right, y))
                current_step.append(Point(x_right, y))
                x_right += 1
            x_right -= 1
            for scan_y in [y-1, y+1]:
                scan_x = x_left
                while scan_x <= x_right:
                    if self.is_inside(scan_x, scan_y) and (scan_x, scan_y) not in filled_pixels:
                        stack.append(Point(scan_x, scan_y))
                        break
                    scan_x += 1
                scan_x = x_right
                while scan_x >= x_left:
                    if self.is_inside(scan_x, scan_y) and (scan_x, scan_y) not in filled_pixels:
                        stack.append(Point(scan_x, scan_y))
                        break
                    scan_x -= 1
            if current_step and debug:
                debug_steps.append(current_step)
        return debug_steps if debug else [Point(x, y) for x, y in filled_pixels]

class PolygonEditor:
    CANVAS_WIDTH = 600
    CANVAS_HEIGHT = 500
    POINT_SIZE = 3
    COLORS = {
        'point': 'black',
        'line': 'black',
        'hull': 'blue',
        'intersection': 'green',
        'fill': 'red',
        'seed': 'red',
        'normal': 'purple',
        'inside_point': 'blue',
        'outside_point': 'orange'
    }

    def __init__(self, root, status_var=None):
        self.root = root
        self.model = PolygonModel()
        self.is_drawing = True
        self.line_points = []
        self.line_mode = False
        self.status_var = status_var
        self.setup_ui()

    def setup_ui(self):
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        hull_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Выпуклая оболочка", menu=hull_menu)
        hull_menu.add_command(label="Метод Грэхема", command=self.build_hull_graham)
        hull_menu.add_command(label="Метод Джарвиса", command=self.build_hull_jarvis)

        fill_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Алгоритмы заполнения", menu=fill_menu)
        fill_menu.add_command(label="Растровая развертка с упорядоченным списком ребер", command=lambda: self.set_fill_mode("ordered_edge"))
        fill_menu.add_command(label="Растровая развертка с активным списком ребер", command=lambda: self.set_fill_mode("active_edge"))
        fill_menu.add_command(label="Заполнение с затравкой (простое)", command=lambda: self.set_fill_mode("simple_seed"))
        fill_menu.add_command(label="Заполнение с затравкой (построчное)", command=lambda: self.set_fill_mode("scanline_seed"))

        self.canvas = tk.Canvas(self.root, bg="white", width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT)
        self.canvas.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.control_frame = tk.Frame(self.root, bg='lavenderblush2')
        self.control_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ns")

        self.canvas.bind("<Button-1>", self.add_point)
        self.canvas.bind("<Button-3>", self.close_polygon)

        tk.Button(self.control_frame, text="Очистить", width=20, font=("Segoe UI", 10), 
                 command=self.clear).grid(row=0, column=0, pady=5)
        tk.Button(self.control_frame, text="Проверить выпуклость", width=20, font=("Segoe UI", 10), 
                 command=self.check_convexity).grid(row=1, column=0, pady=5)
        tk.Button(self.control_frame, text="Рисовать отрезок", width=20, font=("Segoe UI", 10), 
                 command=self.start_line_mode).grid(row=2, column=0, pady=5)
        tk.Button(self.control_frame, text="Найти пересечения", width=20, font=("Segoe UI", 10), 
                 command=self.find_intersections).grid(row=3, column=0, pady=5)
        tk.Button(self.control_frame, text="Показать нормали", width=20, font=("Segoe UI", 10), 
                 command=self.render_normals).grid(row=4, column=0, pady=5)
        tk.Button(self.control_frame, text="Проверить точку", width=20, font=("Segoe UI", 10), 
                 command=self.start_point_check_mode).grid(row=5, column=0, pady=5)
        self.debug_button = tk.Button(self.control_frame, text="Режим отладки", width=20, font=("Segoe UI", 10), 
                                     command=self.toggle_debug_mode)
        self.debug_button.grid(row=6, column=0, pady=5)
        tk.Button(self.control_frame, text="Предыдущий шаг", width=20, font=("Segoe UI", 10), 
                 command=self.prev_debug_step).grid(row=7, column=0, pady=5)
        tk.Button(self.control_frame, text="Следующий шаг", width=20, font=("Segoe UI", 10), 
                 command=self.next_debug_step).grid(row=8, column=0, pady=5)
        tk.Button(self.control_frame, text="Установить затравку", width=20, font=("Segoe UI", 10), 
                 command=self.start_seed_mode).grid(row=9, column=0, pady=5)

        self.fill_mode_var = tk.StringVar(value="Режим заполнения: не выбран")
        tk.Label(self.control_frame, textvariable=self.fill_mode_var, bg='lavenderblush2', 
                 font=("Segoe UI", 10)).grid(row=10, column=0, pady=10)

    def add_point(self, event):
        if self.is_drawing and not self.line_mode and not self.point_check_mode:
            point = self.model.add_point(event.x, event.y)
            self.canvas.create_oval(
                point.x - self.POINT_SIZE, point.y - self.POINT_SIZE,
                point.x + self.POINT_SIZE, point.y + self.POINT_SIZE,
                fill=self.COLORS['point']
            )
            if len(self.model.points) > 1:
                prev_point = self.model.points[-2]
                self.canvas.create_line(
                    prev_point.x, prev_point.y, point.x, point.y,
                    fill=self.COLORS['line'], tags="line"
                )
            if self.status_var:
                self.status_var.set(f"Добавлена точка ({event.x}, {event.y})")
        elif self.line_mode:
            self.line_points.append(Point(event.x, event.y))
            self.canvas.create_oval(
                event.x - self.POINT_SIZE, event.y - self.POINT_SIZE,
                event.x + self.POINT_SIZE, event.y + self.POINT_SIZE,
                fill=self.COLORS['point'], tags="line_point"
            )
            if self.status_var:
                self.status_var.set(f"Точка отрезка {len(self.line_points)}: ({event.x}, {event.y})")
            if len(self.line_points) == 2:
                self.canvas.create_line(
                    self.line_points[0].x, self.line_points[0].y,
                    self.line_points[1].x, self.line_points[1].y,
                    fill=self.COLORS['line'], tags="test_line"
                )
                self.line_mode = False
                self.canvas.bind("<Button-1>", self.add_point)
                if self.status_var:
                    self.status_var.set("Отрезок нарисован. Нажмите 'Найти пересечения'")
        elif self.point_check_mode:
            self.check_point(event)

    def close_polygon(self, event):
        try:
            self.model.close_polygon()
            last_point = self.model.points[-1]
            first_point = self.model.points[0]
            self.canvas.create_line(
                last_point.x, last_point.y, first_point.x, first_point.y,
                fill=self.COLORS['line'], tags="line"
            )
            self.is_drawing = False
            if self.status_var:
                self.status_var.set("Полигон замкнут")
        except ValueError as e:
            messagebox.showinfo("Ошибка", str(e))

    def clear(self):
        self.canvas.delete("all")
        self.model.clear()
        self.is_drawing = True
        self.line_points.clear()
        self.line_mode = False
        self.fill_mode = None
        self.fill_mode_var.set("Режим заполнения: не выбран")
        self.debug_mode = False
        self.debug_button.config(bg='SystemButtonFace')
        self.debug_step = 0
        self.debug_data = []
        self.seed_point = None
        self.seed_mode = False
        self.point_check_mode = False
        if self.status_var:
            self.status_var.set("Холст очищен")

    def check_convexity(self):
        try:
            is_convex = self.model.check_convexity()
            messagebox.showinfo("Результат", "Полигон выпуклый" if is_convex else "Полигон вогнутый")
            if self.status_var:
                self.status_var.set("Полигон " + ("выпуклый" if is_convex else "вогнутый"))
        except ValueError as e:
            messagebox.showinfo("Ошибка", str(e))

    def build_hull_graham(self):
        try:
            hull = self.model.build_hull_graham()
            self.render_hull(hull)
            if self.status_var:
                self.status_var.set("Выпуклая оболочка построена (Грэхем)")
        except ValueError as e:
            messagebox.showinfo("Ошибка", str(e))

    def build_hull_jarvis(self):
        try:
            hull = self.model.build_hull_jarvis()
            self.render_hull(hull)
            if self.status_var:
                self.status_var.set("Выпуклая оболочка построена (Джарвис)")
        except ValueError as e:
            messagebox.showinfo("Ошибка", str(e))

    def render_hull(self, hull):
        self.canvas.delete("hull")
        for i in range(len(hull)):
            p1 = hull[i]
            p2 = hull[(i + 1) % len(hull)]
            self.canvas.create_line(
                p1.x, p1.y, p2.x, p2.y,
                fill=self.COLORS['hull'], tags="hull"
            )

    def start_line_mode(self):
        if len(self.model.points) < 3:
            messagebox.showinfo("Ошибка", "Сначала нарисуйте полигон с минимум 3 точками")
            return
        if self.is_drawing:
            messagebox.showinfo("Ошибка", "Замкните полигон перед рисованием отрезка")
            return
        self.line_mode = True
        self.line_points.clear()
        self.canvas.delete("test_line")
        self.canvas.delete("line_point")
        self.canvas.bind("<Button-1>", self.add_point)
        if self.status_var:
            self.status_var.set("Режим рисования отрезка: выберите первую точку")

    def find_intersections(self):
        try:
            if len(self.line_points) != 2:
                raise ValueError("Нужно выбрать ровно две точки для отрезка")
            intersections = self.model.find_intersections(self.line_points[0], self.line_points[1])
            self.canvas.delete("intersection")
            for point in intersections:
                self.canvas.create_oval(
                    point.x - self.POINT_SIZE, point.y - self.POINT_SIZE,
                    point.x + self.POINT_SIZE, point.y + self.POINT_SIZE,
                    fill=self.COLORS['intersection'], tags="intersection"
                )
            messagebox.showinfo("Результат", f"Найдено пересечений: {len(intersections)}")
            if self.status_var:
                self.status_var.set(f"Найдено пересечений: {len(intersections)}")
        except ValueError as e:
            messagebox.showinfo("Ошибка", str(e))

    def render_normals(self):
        try:
            if len(self.model.points) < 3 or self.is_drawing:
                raise ValueError("Замкните полигон перед отображением нормалей")
            self.canvas.delete("normal")
            normals = self.model.get_normals()
            n = len(self.model.points)
            for i in range(n):
                p1 = self.model.points[i]
                p2 = self.model.points[(i + 1) % n]
                mid_x = (p1.x + p2.x) / 2
                mid_y = (p1.y + p2.y) / 2
                normal = normals[i]
                end_x = mid_x + normal[0]
                end_y = mid_y + normal[1]
                self.canvas.create_line(
                    mid_x, mid_y, end_x, end_y,
                    fill=self.COLORS['normal'], arrow=tk.LAST, tags="normal"
                )
            if self.status_var:
                self.status_var.set("Внутренние нормали отображены")
        except ValueError as e:
            messagebox.showinfo("Ошибка", str(e))

    def start_point_check_mode(self):
        if len(self.model.points) < 3:
            messagebox.showinfo("Ошибка", "Сначала нарисуйте полигон с минимум 3 точками")
            return
        if self.is_drawing:
            messagebox.showinfo("Ошибка", "Замкните полигон перед проверкой точки")
            return
        self.point_check_mode = True
        self.canvas.delete("check_point")
        self.canvas.bind("<Button-1>", self.add_point)
        if self.status_var:
            self.status_var.set("Режим проверки точки: выберите точку")

    def check_point(self, event):
        if self.point_check_mode:
            point = Point(event.x, event.y)
            is_inside = self.model.is_inside(point.x, point.y)
            color = self.COLORS['inside_point'] if is_inside else self.COLORS['outside_point']
            self.canvas.create_oval(
                point.x - 5, point.y - 5,
                point.x + 5, point.y + 5,
                fill=color, tags="check_point"
            )
            messagebox.showinfo("Результат", f"Точка ({point.x}, {point.y}) " + 
                               ("внутри полигона" if is_inside else "снаружи полигона"))
            if self.status_var:
                self.status_var.set(f"Точка ({point.x}, {point.y}) " + 
                                   ("внутри" if is_inside else "снаружи"))
            self.point_check_mode = False
            self.canvas.bind("<Button-1>", self.add_point)

class PolygonFiller(PolygonEditor):
    def __init__(self, root, status_var=None):
        super().__init__(root, status_var)
        self.fill_mode = None
        self.debug_mode = False
        self.debug_step = 0
        self.debug_data = []
        self.seed_point = None
        self.seed_mode = False
        self.point_check_mode = False

    def start_seed_mode(self):
        if self.is_drawing:
            messagebox.showinfo("Ошибка", "Замкните полигон перед установкой затравки")
            return
        self.seed_mode = True
        self.seed_point = None
        self.canvas.delete("seed")
        self.canvas.bind("<Button-1>", self.set_seed_point)
        if self.status_var:
            self.status_var.set("Режим установки затравки: выберите точку внутри полигона")

    def set_seed_point(self, event):
        if self.seed_mode:
            self.seed_point = Point(event.x, event.y)
            if not self.model.is_inside(self.seed_point.x, self.seed_point.y):
                messagebox.showinfo("Ошибка", "Затравочная точка должна быть внутри полигона")
                self.seed_point = None
                if self.status_var:
                    self.status_var.set("Затравка не установлена: точка вне полигона")
                return
            self.canvas.create_oval(
                self.seed_point.x - 5, self.seed_point.y - 5,
                self.seed_point.x + 5, self.seed_point.y + 5,
                fill=self.COLORS['seed'], tags="seed"
            )
            self.seed_mode = False
            self.canvas.bind("<Button-1>", self.add_point)
            if self.status_var:
                self.status_var.set(f"Затравка установлена в ({self.seed_point.x}, {self.seed_point.y})")

    def set_fill_mode(self, mode):
        if self.is_drawing:
            messagebox.showinfo("Ошибка", "Замкните полигон перед заполнением")
            return
        self.fill_mode = mode
        self.canvas.delete("fill")
        self.debug_data = []
        self.debug_step = 0
        if mode in ["simple_seed", "scanline_seed"] and not self.seed_point:
            messagebox.showinfo("Ошибка", "Сначала установите затравочную точку!")
            self.fill_mode = None
            if self.status_var:
                self.status_var.set("Ошибка: затравка не установлена")
            return
        mode_names = {
            "ordered_edge": "Растровая развертка с упорядоченным списком ребер",
            "active_edge": "Растровая развертка с активным списком ребер",
            "simple_seed": "Заполнение с затравкой (простое)",
            "scanline_seed": "Заполнение с затравкой (построчное)"
        }
        self.fill_mode_var.set(f"Режим заполнения: {mode_names[mode]}")
        if self.status_var:
            self.status_var.set(f"Заполнение: {mode_names[mode]}")
        self.fill_polygon()

    def toggle_debug_mode(self):
        self.debug_mode = not self.debug_mode
        self.debug_step = 0
        self.debug_data = []
        self.canvas.delete("fill")
        self.debug_button.config(bg='lightgreen' if self.debug_mode else 'SystemButtonFace')
        messagebox.showinfo("Отладка", f"Режим {'включен' if self.debug_mode else 'выключен'}")
        if self.status_var:
            self.status_var.set(f"Режим отладки {'включен' if self.debug_mode else 'выключен'}")
        if self.fill_mode and self.debug_mode:
            self.fill_polygon()

    def prev_debug_step(self):
        if not self.debug_mode or not self.debug_data:
            messagebox.showinfo("Отладка", "Нет данных для отладки")
            if self.status_var:
                self.status_var.set("Отладка: нет данных")
            return
        self.debug_step -= 1
        if self.debug_step < 0:
            self.debug_step = 0
            messagebox.showinfo("Отладка", "Начало шагов")
            if self.status_var:
                self.status_var.set("Отладка: начало шагов")
        self.canvas.delete("fill")
        for i in range(self.debug_step + 1):
            pixels = self.debug_data[i]
            for point in pixels:
                self.canvas.create_rectangle(
                    point.x, point.y, point.x + 1, point.y + 1,
                    fill=self.COLORS['fill'], outline="", tags="fill"
                )
        if self.status_var:
            self.status_var.set(f"Отладка: шаг {self.debug_step + 1} из {len(self.debug_data)}")

    def next_debug_step(self):
        if not self.debug_mode or not self.debug_data:
            messagebox.showinfo("Отладка", "Нет данных для отладки")
            if self.status_var:
                self.status_var.set("Отладка: нет данных")
            return
        self.debug_step += 1
        if self.debug_step >= len(self.debug_data):
            self.debug_step = len(self.debug_data) - 1
            messagebox.showinfo("Отладка", "Конец шагов")
            if self.status_var:
                self.status_var.set("Отладка: конец шагов")
        self.canvas.delete("fill")
        for i in range(self.debug_step + 1):
            pixels = self.debug_data[i]
            for point in pixels:
                self.canvas.create_rectangle(
                    point.x, point.y, point.x + 1, point.y + 1,
                    fill=self.COLORS['fill'], outline="", tags="fill"
                )
        if self.status_var:
            self.status_var.set(f"Отладка: шаг {self.debug_step + 1} из {len(self.debug_data)}")

    def fill_polygon(self):
        try:
            if not self.fill_mode:
                raise ValueError("Выберите режим заполнения")
            pixels = []
            if self.fill_mode == "ordered_edge":
                pixels = self.model.ordered_edge_list_fill(self.debug_mode)
            elif self.fill_mode == "active_edge":
                pixels = self.model.active_edge_list_fill(self.debug_mode)
            elif self.fill_mode == "simple_seed":
                pixels = self.model.simple_seed_fill(self.seed_point, self.debug_mode)
            elif self.fill_mode == "scanline_seed":
                pixels = self.model.scanline_seed_fill(self.seed_point, self.debug_mode)
            if self.debug_mode:
                self.debug_data = pixels
                self.next_debug_step()
            else:
                for point in pixels:
                    self.canvas.create_rectangle(
                        point.x, point.y, point.x + 1, point.y + 1,
                        fill=self.COLORS['fill'], outline="", tags="fill"
                    )
                if self.status_var:
                    self.status_var.set("Полигон заполнен")
        except ValueError as e:
            messagebox.showinfo("Ошибка", str(e))
            if self.status_var:
                self.status_var.set(f"Ошибка заполнения: {str(e)}")