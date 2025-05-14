import numpy as np

class HermiteProcessor:
    """Class to handle Hermite curve interpolation with control points and tangents."""
    
    def __init__(self):
        """Initialize Hermite curve processor with empty nodes and tangents."""
        self.control_nodes = []
        self.tangents = []
        self.segment_count = 100
        self.hermite_matrix = np.array([
            [2, -2, 1, 1],
            [-3, 3, -2, -1],
            [0, 0, 1, 0],
            [1, 0, 0, 0]
        ])

    def add_node(self, x, y):
        """Add a control point to the curve."""
        self.control_nodes.append(np.array([x, y]))
        self.tangents.append(np.array([0, 0]))

    def clear_nodes(self):
        """Reset all control points and tangents."""
        self.control_nodes = []
        self.tangents = []

    def update_tangents(self):
        """Compute tangents for all control points."""
        if len(self.control_nodes) < 2:
            return
        self.tangents = [
            (self.control_nodes[1] - self.control_nodes[0]) * 0.5 if i == 0 else
            (self.control_nodes[-1] - self.control_nodes[-2]) * 0.5 if i == len(self.control_nodes) - 1 else
            (self.control_nodes[i + 1] - self.control_nodes[i - 1]) * 0.25
            for i in range(len(self.control_nodes))
        ]

    def set_tangent(self, index, dx, dy):
        """Set tangent vector for a specific control point."""
        if 0 <= index < len(self.tangents):
            self.tangents[index] = np.array([dx, dy])

    def compute_segment(self, node1, node2, tangent1, tangent2):
        """Compute points for a single Hermite curve segment using matrix method."""
        t_values = np.linspace(0, 1, self.segment_count)
        T = np.column_stack([t_values**3, t_values**2, t_values, np.ones_like(t_values)])
        geometry = np.array([node1, node2, tangent1, tangent2])
        return T @ self.hermite_matrix @ geometry

    def generate_curve(self):
        """Generate all points for the Hermite curve across all segments."""
        if len(self.control_nodes) < 2:
            return np.array([])
        self.update_tangents()
        curve_points = []
        for i in range(len(self.control_nodes) - 1):
            segment = self.compute_segment(
                self.control_nodes[i], 
                self.control_nodes[i + 1], 
                self.tangents[i], 
                self.tangents[i + 1]
            )
            curve_points.append(segment)
        return np.vstack(curve_points) if curve_points else np.array([])

    def get_control_edges(self):
        """Return lines connecting consecutive control points."""
        return [
            (self.control_nodes[i], self.control_nodes[i + 1])
            for i in range(len(self.control_nodes) - 1)
        ]

    def get_tangent_lines(self):
        """Return lines representing tangent vectors at control points."""
        return [
            (self.control_nodes[i], self.control_nodes[i] + self.tangents[i] * 0.2)
            for i in range(len(self.control_nodes))
        ]

    def get_debug_data(self):
        """Generate debug data for step-by-step visualization."""
        if len(self.control_nodes) < 2:
            return []
        self.update_tangents()
        debug_info = []
        for i in range(len(self.control_nodes) - 1):
            t_values = np.linspace(0, 1, min(10, self.segment_count))
            segment = self.compute_segment(
                self.control_nodes[i], 
                self.control_nodes[i + 1], 
                self.tangents[i], 
                self.tangents[i + 1]
            )
            for j, t in enumerate(t_values):
                idx = int(j * self.segment_count / min(10, self.segment_count))
                x, y = segment[idx]
                debug_info.append((i, t, x, y))
        return debug_info