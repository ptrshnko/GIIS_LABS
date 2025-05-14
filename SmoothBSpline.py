import numpy as np

class BSplineBuilder:
    """Class to build a B-spline curve with multiple control points."""
    
    def __init__(self):
        """Initialize B-spline builder with empty nodes and spline matrix."""
        self.spline_nodes = []
        self.spline_matrix = np.array([
            [-1, 3, -3, 1],
            [3, -6, 3, 0],
            [-3, 0, 3, 0],
            [1, 4, 1, 0]
        ]) / 6.0
        self.resolution = 60

    def insert_node(self, x, y):
        """Add a control point to the B-spline."""
        self.spline_nodes.append([x, y])

    def reset_nodes(self):
        """Clear all control points."""
        self.spline_nodes = []

    def compute_segment(self, segment_nodes):
        """Compute points for a single B-spline segment."""
        t_values = np.linspace(0, 1, self.resolution)
        T = np.column_stack([t_values**3, t_values**2, t_values, np.ones_like(t_values)])
        segment_array = np.array(segment_nodes)
        return np.dot(T, np.dot(self.spline_matrix, segment_array))

    def generate_curve(self):
        """Generate points for the entire B-spline curve."""
        if len(self.spline_nodes) < 4:
            return np.array([])
        
        curve_points = []
        for i in range(len(self.spline_nodes) - 3):
            segment_nodes = self.spline_nodes[i:i+4]
            segment_points = self.compute_segment(segment_nodes)
            curve_points.append(segment_points)
        
        return np.vstack(curve_points) if curve_points else np.array([])

    def get_connecting_lines(self):
        """Return lines connecting consecutive control points."""
        return [
            (self.spline_nodes[i], self.spline_nodes[i + 1])
            for i in range(len(self.spline_nodes) - 1)
        ]

    def get_debug_info(self):
        """Generate debug data for step-by-step B-spline visualization."""
        if len(self.spline_nodes) < 4:
            return []
        
        debug_info = []
        for i in range(len(self.spline_nodes) - 3):
            segment_nodes = self.spline_nodes[i:i+4]
            t_values = np.linspace(0, 1, min(10, self.resolution))
            T = np.column_stack([t_values**3, t_values**2, t_values, np.ones_like(t_values)])
            segment_points = np.dot(T, np.dot(self.spline_matrix, np.array(segment_nodes)))
            for j, (t, point) in enumerate(zip(t_values, segment_points)):
                debug_info.append((i, j, t, point[0], point[1]))
        return debug_info