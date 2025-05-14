import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import time

class CurveRenderer:
    def __init__(self, curve_type, params):
        self.curve_type = curve_type
        self.params = params
        self.cell_size = 1
        self.fig = None
        self.ax = None

    def setup_canvas(self):
        if self.fig is None or self.ax is None:
            self.fig, self.ax = plt.subplots()
            self.ax.set_aspect('equal')
            self.ax.set_xlim(-20, 20)
            self.ax.set_ylim(-20, 20)
            self.ax.set_xticks(np.arange(-20, 21, self.cell_size))
            self.ax.set_yticks(np.arange(-20, 21, self.cell_size))
            self.ax.set_xticklabels(np.arange(-20, 21, self.cell_size))
            self.ax.set_yticklabels(np.arange(-20, 21, self.cell_size))
            for x in range(-20, 21, self.cell_size):
                for y in range(-20, 21, self.cell_size):
                    rect = patches.Rectangle((x, y), self.cell_size, self.cell_size, fill=False, edgecolor='gray')
                    self.ax.add_patch(rect)
            self.ax.grid(True)
        else:
            self.ax.clear()
            self.ax.set_aspect('equal')
            self.ax.set_xlim(-20, 20)
            self.ax.set_ylim(-20, 20)
            self.ax.set_xticks(np.arange(-20, 21, self.cell_size))
            self.ax.set_yticks(np.arange(-20, 21, self.cell_size))
            self.ax.set_xticklabels(np.arange(-20, 21, self.cell_size))
            self.ax.set_yticklabels(np.arange(-20, 21, self.cell_size))
            for x in range(-20, 21, self.cell_size):
                for y in range(-20, 21, self.cell_size):
                    rect = patches.Rectangle((x, y), self.cell_size, self.cell_size, fill=False, edgecolor='gray')
                    self.ax.add_patch(rect)
            self.ax.grid(True)

    def plot_pixel(self, x, y, color=(0, 0, 0)):
        rect = patches.Rectangle((x * self.cell_size, y * self.cell_size), self.cell_size, self.cell_size, color=color)
        self.ax.add_patch(rect)

    def plot_circle_pixels(self, x, y):
        self.plot_pixel(x, y)
        self.plot_pixel(-x, y)
        self.plot_pixel(x, -y)
        self.plot_pixel(-x, -y)
        self.plot_pixel(y, x)
        self.plot_pixel(-y, x)
        self.plot_pixel(y, -x)
        self.plot_pixel(-y, -x)

    def plot_ellipse_pixels(self, x, y):
        self.plot_pixel(x, y)
        self.plot_pixel(-x, y)
        self.plot_pixel(x, -y)
        self.plot_pixel(-x, -y)

    def plot_hyperbola_pixels(self, x, y):
        self.plot_pixel(x, y)
        self.plot_pixel(-x, y)
        self.plot_pixel(x, -y)
        self.plot_pixel(-x, -y)

    def plot_parabola_pixels(self, x, y):
        self.plot_pixel(x, y)
        self.plot_pixel(-x, y)

    def draw_circle(self, debug=False):
        R = self.params['R']
        x, y = 0, R
        delta = 1 - R
        self.setup_canvas()
        self.plot_circle_pixels(x, y)
        while y >= x:
            if debug:
                self.fig.canvas.draw()
                self.fig.canvas.flush_events()
                time.sleep(0.05)
            if delta <= 0:
                x += 1
                delta += 2 * x + 1
            else:
                x += 1
                y -= 1
                delta += 2 * (x - y) + 1
            self.plot_circle_pixels(x, y)
        if not debug:
            plt.show()

    def draw_ellipse(self, debug=False):
        a, b = self.params['a'], self.params['b']
        x, y = 0, b
        a2, b2 = a * a, b * b
        delta = b2 - a2 * (b - 0.25)
        self.setup_canvas()
        self.plot_ellipse_pixels(x, y)
        while b2 * x <= a2 * y:
            if debug:
                self.fig.canvas.draw()
                self.fig.canvas.flush_events()
                time.sleep(0.05)
            if delta <= 0:
                x += 1
                delta += b2 * (2 * x + 1)
            else:
                x += 1
                y -= 1
                delta += b2 * (2 * x + 1) - a2 * (2 * y - 1)
            self.plot_ellipse_pixels(x, y)
        delta = b2 * (x + 0.5) ** 2 + a2 * (y - 1) ** 2 - a2 * b2
        while y >= 0:
            if debug:
                self.fig.canvas.draw()
                self.fig.canvas.flush_events()
                time.sleep(0.05)
            if delta <= 0:
                x += 1
                y -= 1
                delta += b2 * (2 * x + 1) - a2 * (2 * y - 1)
            else:
                y -= 1
                delta -= a2 * (2 * y - 1)
            self.plot_ellipse_pixels(x, y)
        if not debug:
            plt.show()

    def draw_hyperbola(self, debug=False):
        a, b = self.params['a'], self.params['b']
        a2, b2 = a * a, b * b
        x, y = a, 0
        delta = b2 * a2 - b2 * (a + 0.5) ** 2
        self.setup_canvas()
        self.plot_hyperbola_pixels(x, y)
        while b2 * (x + 1) <= a2 * (y + 0.5):
            if debug:
                self.fig.canvas.draw()
                self.fig.canvas.flush_events()
                time.sleep(0.05)
            if delta <= 0:
                x += 1
                delta += b2 * (2 * x + 1)
            else:
                x += 1
                y += 1
                delta += b2 * (2 * x + 1) - a2 * (2 * y + 1)
            self.plot_hyperbola_pixels(x, y)
        delta = b2 * (x + 1) ** 2 - a2 * (y + 0.5) ** 2 - a2 * b2
        while x < 20:
            if debug:
                self.fig.canvas.draw()
                self.fig.canvas.flush_events()
                time.sleep(0.05)
            if delta <= 0:
                x += 1
                y += 1
                delta += b2 * (2 * x + 1) - a2 * (2 * y + 1)
            else:
                y += 1
                delta -= a2 * (2 * y + 1)
            self.plot_hyperbola_pixels(x, y)
        if not debug:
            plt.show()

    def draw_parabola(self, debug=False):
        p = self.params['p']
        x, y = 0, 0
        delta = -p
        self.setup_canvas()
        self.plot_parabola_pixels(x, y)
        while y < 20:
            if debug:
                self.fig.canvas.draw()
                self.fig.canvas.flush_events()
                time.sleep(0.05)
            if delta <= 0:
                x += 1
                delta += 2 * x + 1
            else:
                y += 1
                delta -= 2 * p
            self.plot_parabola_pixels(x, y)
        if not debug:
            plt.show()

    def draw(self, debug=False):
        if self.curve_type == 'circle':
            self.draw_circle(debug)
        elif self.curve_type == 'ellipse':
            self.draw_ellipse(debug)
        elif self.curve_type == 'hyperbola':
            self.draw_hyperbola(debug)
        elif self.curve_type == 'parabola':
            self.draw_parabola(debug)

    def start_debug(self):
        plt.ion()
        self.draw(debug=True)
        plt.ioff()
        plt.show()