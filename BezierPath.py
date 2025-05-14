import numpy as np

class BezierGenerator:
    """Class to generate a cubic Bézier curve with four control points."""
    
    def __init__(self):
        """Initialize Bézier curve generator with empty nodes and basis matrix."""
        self.path_nodes = []
        self.basis_matrix = np.array([
            [-1, 3, -3, 1],
            [3, -6, 3, 0],
            [-3, 3, 0, 0],
            [1, 0, 0, 0]
        ])
        self.point_density = 120

    def insert_node(self, x, y):
        """Add a control point to the curve."""
        self.path_nodes.append([x, y])

    def reset_nodes(self):
        """Clear all control points."""
        self.path_nodes = []

    def compute_t_matrix(self):
        """Generate the parameter matrix for t values."""
        t_values = np.linspace(0, 1, self.point_density)
        return np.column_stack([t_values**3, t_values**2, t_values, np.ones_like(t_values)])

    def generate_curve(self):
        """Compute points for the cubic Bézier curve."""
        if len(self.path_nodes) != 4:
            raise ValueError("Exactly 4 control points are required")
        
        T = self.compute_t_matrix()
        nodes_array = np.array(self.path_nodes)
        curve_points = np.dot(T, np.dot(self.basis_matrix, nodes_array))
        return curve_points

    def get_connecting_lines(self):
        """Return lines connecting consecutive control points."""
        return [
            (self.path_nodes[i], self.path_nodes[i + 1])
            for i in range(len(self.path_nodes) - 1)
        ]

    def get_debug_info(self):
        """Generate debug data for step-by-step curve visualization."""
        if len(self.path_nodes) != 4:
            return []
        
        t_values = np.linspace(0, 1, min(10, self.point_density))
        T = np.column_stack([t_values**3, t_values**2, t_values, np.ones_like(t_values)])
        nodes_array = np.array(self.path_nodes)
        points = np.dot(T, np.dot(self.basis_matrix, nodes_array))
        return [(i, t, point[0], point[1]) for i, (t, point) in enumerate(zip(t_values, points))]