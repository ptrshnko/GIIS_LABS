import tkinter as tk
from lab1_window import LineDrawingWindow
from lab2_window import Lab2Window
from lab3_window import Lab3Window
from lab4_window import Lab4Window
from lab5_window import Lab56Window
from lab7_window import Lab7Window

class GraphicEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Графический редактор")
        self.root.geometry("400x250")
        self.root.configure(bg='lavenderblush2')

        tk.Label(self.root, text="Выберите лабораторную работу:", bg="lavenderblush2", font=("Segoe UI", 14, "bold")).pack(pady=20)
        tk.Button(self.root, text="Лабораторная работа 1 ", command=self.open_lab1, width=30).pack(pady=10)
        tk.Button(self.root, text="Лабораторная работа 2 ", command=self.open_lab2, width=30).pack(pady=10)
        tk.Button(self.root, text="Лабораторная работа 3 ", command=self.open_lab3, width=30).pack(pady=10)
        tk.Button(self.root, text="Лабораторная работа 4 ", command=self.open_lab4, width=30).pack(pady=10)
        tk.Button(self.root, text="Лабораторные работы 5-6 ", command=self.open_lab56, width=30).pack(pady=10)
        tk.Button(self.root, text="Лабораторная работа 7 ", command=self.open_lab7, width=30).pack(pady=10)

    def open_lab1(self):
        window = tk.Toplevel(self.root)
        LineDrawingWindow(window)

    def open_lab2(self):
        window = tk.Toplevel(self.root)
        Lab2Window(window)

    def open_lab3(self):
        window = tk.Toplevel(self.root)
        Lab3Window(window)

    def open_lab4(self):
        window = tk.Toplevel(self.root)
        Lab4Window(window)

    def open_lab56(self):
        window = tk.Toplevel(self.root)
        Lab56Window(window)

    def open_lab7(self):
        window = tk.Toplevel(self.root)
        Lab7Window(window)

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphicEditorApp(root)
    root.mainloop()