import tkinter as tk
from tkinter import ttk, messagebox
from ParametricHermite import HermiteProcessor

class HermiteRenderer:
    """Class to render Hermite curves with interactive UI for points and tangents."""
    
    def __init__(self, root):
        """Initialize Hermite curve renderer with Tkinter UI."""
        self.root = root
        self.root.title("Hermite Curve Renderer")
        self.root.configure(bg='lightblue')
        self.curve_processor = HermiteProcessor()
        self.tangent_mode = False
        self.selected_node = None
        self.draw_surface = None
        self.setup_interface()

    def setup_interface(self):
        """Set up the Tkinter UI with canvas and control buttons."""
        self.draw_surface = tk.Canvas(self.root, width=650, height=450, bg='white')
        self.draw_surface.pack(padx=10, pady=10)
        self.draw_surface.bind("<Button-1>", self.handle_click)

        control_panel = tk.Frame(self.root, bg='lightblue')
        control_panel.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(control_panel, text="Clear Canvas", command=self.reset).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_panel, text="Render Curve", command=self.render_curve).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_panel, text="Toggle Tangent Edit", command=self.switch_mode).pack(side=tk.LEFT, padx=5)

        self.debug_label = tk.Label(self.root, text="", bg='lightblue', font=("Arial", 10), anchor="w", justify="left")
        self.debug_label.pack(fill=tk.X, padx=10)

    def switch_mode(self):
        """Toggle between point addition and tangent editing modes."""
        self.tangent_mode = not self.tangent_mode
        self.selected_node = None
        self.draw_surface.delete("temp_line")
        if self.tangent_mode:
            self.render_tangent_lines()
            self.show_debug_info()
        else:
            self.draw_surface.delete("derivative_line")
            self.debug_label.config(text="")

    def handle_click(self, event):
        """Handle canvas click events for adding points or editing tangents."""
        x, y = event.x, event.y
        if not self.tangent_mode:
            if len(self.curve_processor.control_nodes) >= 8:
                messagebox.showwarning("Warning", "Maximum 8 control points allowed.")
                return
            self.curve_processor.add_node(x, y)
            self.draw_surface.create_oval(x - 4, y - 4, x + 4, y + 4, fill='blue', tags="node")
            self.render_control_lines()
        else:
            closest_idx, min_dist = None, float('inf')
            for i, node in enumerate(self.curve_processor.control_nodes):
                dist = ((node[0] - x) ** 2 + (node[1] - y) ** 2) ** 0.5
                if dist < min_dist and dist < 25:
                    min_dist, closest_idx = dist, i
            if closest_idx is not None:
                self.selected_node = closest_idx
                node = self.curve_processor.control_nodes[closest_idx]
                self.curve_processor.set_tangent(closest_idx, x - node[0], y - node[1])
                self.render_tangent_lines()
                self.show_debug_info()
            else:
                messagebox.showinfo("Info", "Click closer to a control point to set tangent.")

    def render_control_lines(self):
        """Draw lines connecting consecutive control points."""
        self.draw_surface.delete("control_line")
        for line in self.curve_processor.get_control_edges():
            p1, p2 = line
            self.draw_surface.create_line(p1[0], p1[1], p2[0], p2[1], fill='gray', dash=(3, 3), tags="control_line")

    def render_tangent_lines(self):
        """Draw lines representing tangent vectors."""
        self.draw_surface.delete("derivative_line")
        for line in self.curve_processor.get_tangent_lines():
            p1, p2 = line
            self.draw_surface.create_line(p1[0], p1[1], p2[0], p2[1], fill='green', tags="derivative_line")

    def render_curve(self):
        """Render the Hermite curve on the canvas."""
        self.draw_surface.delete("curve")
        if len(self.curve_processor.control_nodes) < 2:
            messagebox.showerror("Error", "At least 2 control points are required.")
            return
        try:
            curve = self.curve_processor.generate_curve()
            for i in range(len(curve) - 1):
                x1, y1 = curve[i]
                x2, y2 = curve[i + 1]
                self.draw_surface.create_line(x1, y1, x2, y2, fill='black', width=2, tags="curve")
            if self.tangent_mode:
                self.show_debug_info()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def show_debug_info(self):
        """Display debug information for curve interpolation."""
        debug_data = self.curve_processor.get_debug_data()
        if not debug_data:
            self.debug_label.config(text="No debug data available.")
            return
        debug_text = "Debug Info:\n" + "\n".join(
            f"Segment {seg}: t={t:.2f}, x={x:.1f}, y={y:.1f}" for seg, _, t, x, y in debug_data
        )
        self.debug_label.config(text=debug_text)

    def reset(self):
        """Clear the canvas and reset the curve processor."""
        self.draw_surface.delete("all")
        self.curve_processor.clear_nodes()
        self.tangent_mode = False
        self.selected_node = None
        self.debug_label.config(text="")