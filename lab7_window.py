import tkinter as tk
from Delaunay import Delaunay
from Voronoi import VoronoiDiagram


class Lab7Window:
    RADIUS = 3
    LOCK_FLAG = False

    def __init__(self, master):
        self.master = master
        self.master.title("Лабораторная работа 7: Delaunay и Voronoi")
        self.master.geometry("1000x800")

        self.canvas = tk.Canvas(self.master, width=800, height=600, bg="white")
        self.canvas.pack()

        self.points = []
        self.mode = "both"  
        self.delaunay_edges = []
        self.voronoi_lines = []

        self.canvas.bind("<Button-1>", self.add_point)
        self.canvas.bind("<Button-3>", self.clear_points)

        button_frame = tk.Frame(self.master)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Режим Делоне", command=self.set_delaunay_mode, width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Режим Ворони", command=self.set_voronoi_mode, width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Оба результата", command=self.set_both_mode, width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Рассчитать", command=self.calculate, width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Очистить", command=self.clear_points, width=15).pack(side=tk.LEFT, padx=5)

        self.draw()

    def set_delaunay_mode(self):
        self.mode = "delaunay"
        self.draw()

    def set_voronoi_mode(self):
        self.mode = "voronoi"
        self.draw()

    def set_both_mode(self):
        self.mode = "both"
        self.draw()

    def add_point(self, event):
        if not self.LOCK_FLAG and event.x >= 0 and event.x <= 800 and event.y >= 0 and event.y <= 600:
            self.points.append((event.x, event.y))
            self.draw()

    def clear_points(self, event=None):
        self.LOCK_FLAG = False
        self.points = []
        self.delaunay_edges = []
        self.voronoi_lines = []
        self.draw()

    def calculate(self):
        if not self.LOCK_FLAG and len(self.points) >= 3:
            self.LOCK_FLAG = True
            delaunay = Delaunay(self.points)
            self.delaunay_edges = delaunay.compute()
            voronoi = VoronoiDiagram(self.points)
            voronoi.construct()
            self.voronoi_lines = voronoi.get_segments()
            self.draw()

    def draw(self):
        self.canvas.delete("all")
        for x, y in self.points:
            self.canvas.create_oval(x - self.RADIUS, y - self.RADIUS, x + self.RADIUS, y + self.RADIUS, fill="black")

        if self.mode in ["delaunay", "both"] and self.delaunay_edges:
            for (p1, p2) in self.delaunay_edges:
                self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill="blue")

        if self.mode in ["voronoi", "both"] and self.voronoi_lines:
            for line in self.voronoi_lines:
                self.canvas.create_line(line[0], line[1], line[2], line[3], fill="red")