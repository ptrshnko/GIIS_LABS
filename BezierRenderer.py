import tkinter as tk
from tkinter import ttk, messagebox
from BezierPath import BezierGenerator

class BezierRenderer:
    """Class to render a cubic Bézier curve with interactive UI."""
    
    def __init__(self, root):
        """Initialize Bézier curve renderer with Tkinter UI."""
        self.root = root
        self.root.title("Bézier Curve Renderer")
        self.root.configure(bg='lightgray')
        self.path_generator = BezierGenerator()
        self.control_points = []
        self.render_canvas = None
        self.setup_ui()

    def setup_ui(self):
        """Set up the Tkinter UI with canvas and control buttons."""
        self.render_canvas = tk.Canvas(self.root, width=700, height=500, bg='white')
        self.render_canvas.pack(padx=10, pady=10)
        self.render_canvas.bind("<Button-1>", self.handle_click)

        control_frame = tk.Frame(self.root, bg='lightgray')
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(control_frame, text="Clear Canvas", command=self.reset).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Render Curve", command=self.draw_curve).pack(side=tk.LEFT, padx=5)

        self.debug_display = tk.Label(self.root, text="", bg='lightgray', font=("Arial", 10), anchor="w", justify="left")
        self.debug_display.pack(fill=tk.X, padx=10)

    def handle_click(self, event):
        """Handle canvas click events to add control points."""
        x, y = event.x, event.y
        if len(self.control_points) >= 4:
            messagebox.showwarning("Warning", "Exactly 4 control points are required.")
            return
        self.control_points.append((x, y))
        self.path_generator.insert_node(x, y)
        self.render_canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill='purple', tags="point")
        self.draw_control_lines()

    def draw_control_lines(self):
        """Draw lines connecting consecutive control points."""
        self.render_canvas.delete("control_line")
        for line in self.path_generator.get_connecting_lines():
            p1, p2 = line
            self.render_canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill='gray', dash=(4, 4), tags="control_line")

    def draw_curve(self):
        """Render the Bézier curve on the canvas."""
        self.render_canvas.delete("curve")
        if len(self.control_points) != 4:
            messagebox.showerror("Error", "Exactly 4 control points are required.")
            return
        try:
            curve = self.path_generator.generate_curve()
            for i in range(len(curve) - 1):
                x1, y1 = curve[i]
                x2, y2 = curve[i + 1]
                self.render_canvas.create_line(x1, y1, x2, y2, fill='black', width=2, tags="curve")
            self.show_debug_info()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def show_debug_info(self):
        """Display debug information for curve interpolation."""
        debug_data = self.path_generator.get_debug_info()
        if not debug_data:
            self.debug_display.config(text="No debug data available.")
            return
        debug_text = "Debug Info:\n" + "\n".join(
            f"Step {i}: t={t:.2f}, x={x:.1f}, y={y:.1f}" for i, t, x, y in debug_data
        )
        self.debug_display.config(text=debug_text)

    def reset(self):
        """Clear the canvas and reset the curve generator."""
        self.render_canvas.delete("all")
        self.path_generator.reset_nodes()
        self.control_points = []
        self.debug_display.config(text="")