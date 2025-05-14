import tkinter as tk
from tkinter import ttk, messagebox
from curve_renderer import CurveRenderer

class Lab2Window:
    def __init__(self, root):
        self.root = root
        self.root.title("Graphic Editor - Lab 2")
        self.root.geometry("400x400")
        self.root.configure(bg='lavenderblush2')

        # Main frame for controls
        self.control_frame = tk.Frame(self.root, bg='lavenderblush2')
        self.control_frame.place(relx=0.5, rely=0.1, anchor='n')

        # Title
        tk.Label(self.control_frame, text="Second-Order Curves\nGraphic Editor", 
                 bg="lavenderblush2", font=("Segoe UI", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        # Curve selection
        tk.Label(self.control_frame, text="Curve Type:", bg='lavenderblush2').grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.curve_var = tk.StringVar(value='circle')
        curve_options = ['circle', 'ellipse', 'hyperbola', 'parabola']
        self.curve_combobox = ttk.Combobox(self.control_frame, textvariable=self.curve_var, values=curve_options, state='readonly', width=15)
        self.curve_combobox.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.curve_combobox.bind('<<ComboboxSelected>>', self.update_param_fields)

        # Parameter input frame
        self.param_frame = tk.Frame(self.control_frame, bg='lavenderblush2')
        self.param_frame.grid(row=2, column=0, columnspan=2, pady=10)

        # Parameter fields (initialized later)
        self.param_entries = {}
        self.param_labels = {}
        self.update_param_fields()

        # Buttons
        ttk.Button(self.control_frame, text="Generate", command=self.generate_curve).grid(row=3, column=0, columnspan=2, pady=5)
        ttk.Button(self.control_frame, text="Generation Debug", command=lambda: self.generate_curve(debug=True)).grid(row=4, column=0, columnspan=2, pady=5)

    def update_param_fields(self, event=None):
        # Clear previous parameter fields
        for widget in self.param_frame.winfo_children():
            widget.destroy()
        self.param_entries.clear()
        self.param_labels.clear()

        # Define parameter requirements for each curve
        curve_params = {
            'circle': [('R', 'Radius')],
            'ellipse': [('a', 'Semi-major axis'), ('b', 'Semi-minor axis')],
            'hyperbola': [('a', 'Parameter a'), ('b', 'Parameter b')],
            'parabola': [('p', 'Parameter p')]
        }

        # Create input fields for the selected curve
        curve_type = self.curve_var.get()
        for i, (param, label) in enumerate(curve_params[curve_type]):
            tk.Label(self.param_frame, text=f"{label}:", bg='lavenderblush2').grid(row=i, column=0, padx=5, pady=5, sticky='e')
            entry = tk.Entry(self.param_frame, width=10)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky='w')
            self.param_labels[param] = label
            self.param_entries[param] = entry

    def validate_positive_int(self, value, field_name):
        try:
            val = int(value)
            if val <= 0:
                raise ValueError(f"{field_name} must be positive")
            return val
        except ValueError as e:
            messagebox.showerror("Invalid Input", f"Error: {field_name} must be a positive integer")
            raise

    def generate_curve(self, debug=False):
        try:
            curve_type = self.curve_var.get()
            params = {}
            for param, entry in self.param_entries.items():
                if not entry.get():
                    raise ValueError(f"{self.param_labels[param]} is required")
                params[param] = self.validate_positive_int(entry.get(), self.param_labels[param])
            
            renderer = CurveRenderer(curve_type, params)
            if debug:
                renderer.start_debug()
            else:
                renderer.draw()
        except ValueError:
            pass