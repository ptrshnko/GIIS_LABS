import numpy as np
from math import cos, sin, radians

class Transform3DRenderer:
    def __init__(self, coordinates, links):
        self.coordinates = np.array(coordinates, dtype=float)
        self.links = links
        self.initial_coords = self.coordinates.copy()

    @classmethod
    def from_file(cls, filepath):
        coordinates = []
        links = []
        try:
            with open(filepath, 'r') as file:
                for line in file:
                    parts = line.strip().split()
                    if not parts or parts[0] == '#':
                        continue
                    if parts[0] == 'v':
                        coordinates.append([float(parts[1]) / 2.5, float(parts[2]) / 2.5, float(parts[3]) / 2.5])
                    elif parts[0] == 'e':
                        links.append((int(parts[1]), int(parts[2])))
            if not coordinates or not links:
                raise ValueError("File must contain vertices and edges")
            return cls(coordinates, links)
        except Exception as e:
            raise ValueError(f"Invalid file: {str(e)}")

    def reset(self):
        self.coordinates = self.initial_coords.copy()

    def shift(self, dx, dy, dz):
        matrix = np.array([[1, 0, 0, dx],
                          [0, 1, 0, dy],
                          [0, 0, 1, dz],
                          [0, 0, 0, 1]])
        self._transform(matrix)

    def rotate_x(self, angle):
        theta = radians(angle)
        matrix = np.array([[1, 0, 0, 0],
                          [0, cos(theta), sin(theta), 0],
                          [0, -sin(theta), cos(theta), 0],
                          [0, 0, 0, 1]])
        self._transform(matrix)

    def rotate_y(self, angle):
        theta = radians(angle)
        matrix = np.array([[cos(theta), 0, -sin(theta), 0],
                          [0, 1, 0, 0],
                          [sin(theta), 0, cos(theta), 0],
                          [0, 0, 0, 1]])
        self._transform(matrix)

    def rotate_z(self, angle):
        theta = radians(angle)
        matrix = np.array([[cos(theta), sin(theta), 0, 0],
                          [-sin(theta), cos(theta), 0, 0],
                          [0, 0, 1, 0],
                          [0, 0, 0, 1]])
        self._transform(matrix)

    def scale_object(self, sx, sy, sz):
        matrix = np.array([[sx, 0, 0, 0],
                          [0, sy, 0, 0],
                          [0, 0, sz, 0],
                          [0, 0, 0, 1]])
        self._transform(matrix)

    def mirror_yz(self):
        matrix = np.array([[-1, 0, 0, 0],
                          [0, 1, 0, 0],
                          [0, 0, 1, 0],
                          [0, 0, 0, 1]])
        self._transform(matrix)

    def apply_perspective(self, dist):
        if dist <= 0:
            dist = 0.01
        matrix = np.array([[1, 0, 0, 0],
                          [0, 1, 0, 0],
                          [0, 0, 1, 0],
                          [0, 0, -1/dist, 1]])
        self._transform(matrix)

    def _transform(self, matrix):
        homogeneous = np.column_stack((self.coordinates, np.ones(len(self.coordinates))))
        transformed = np.dot(matrix, homogeneous.T).T
        w = transformed[:, 3]
        w = np.where(w == 0, 1e-6, w)  # Avoid division by zero
        self.coordinates = (transformed[:, :3].T / w).T

    def project_to_2d(self, width, height):
        scale_factor = min(width, height) / 5
        projected = []
        for point in self.coordinates:
            px = point[0] * scale_factor + width / 2
            py = -point[1] * scale_factor + height / 2
            projected.append((px, py))
        return projected

    def get_edges(self):
        return self.links