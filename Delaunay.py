import math
import tkinter as tk


class Delaunay:
    def __init__(self, input_points):
        self.coordinates = input_points
        self.triangles = []
        self.edges = set()

    def compute(self):
        if len(self.coordinates) < 3:
            return []

        super_tri = self._create_supertriangle()
        self.triangles = [super_tri]

        for point in self.coordinates:
            self._add_point(point)

        self._filter_supertriangle(super_tri)
        
        self._collect_edges()
        return list(self.edges)

    def _create_supertriangle(self):
        min_x = min(x for x, y in self.coordinates)
        max_x = max(x for x, y in self.coordinates)
        min_y = min(y for x, y in self.coordinates)
        max_y = max(y for x, y in self.coordinates)
        delta_x = max_x - min_x
        delta_y = max_y - min_y
        max_delta = max(delta_x, delta_y) * 3
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2
        return [
            (center_x - max_delta, center_y - max_delta),
            (center_x + max_delta, center_y - max_delta),
            (center_x, center_y + max_delta)
        ]

    def _in_circle(self, point, tri_a, tri_b, tri_c):
        ax, ay = tri_a[0] - point[0], tri_a[1] - point[1]
        bx, by = tri_b[0] - point[0], tri_b[1] - point[1]
        cx, cy = tri_c[0] - point[0], tri_c[1] - point[1]
        determinant = (
            (ax ** 2 + ay ** 2) * (bx * cy - by * cx) -
            (bx ** 2 + by ** 2) * (ax * cy - ay * cx) +
            (cx ** 2 + cy ** 2) * (ax * by - ay * bx)
        )
        return determinant > 0

    def _add_point(self, point):
        invalid_triangles = []
        for triangle in self.triangles:
            if self._in_circle(point, triangle[0], triangle[1], triangle[2]):
                invalid_triangles.append(triangle)

        cavity_edges = []
        for triangle in invalid_triangles:
            for i in range(3):
                edge = (triangle[i], triangle[(i + 1) % 3])
                is_shared = False
                for other_tri in invalid_triangles:
                    if other_tri != triangle and edge[0] in other_tri and edge[1] in other_tri:
                        is_shared = True
                        break
                if not is_shared:
                    cavity_edges.append(edge)

        self.triangles = [t for t in self.triangles if t not in invalid_triangles]
        for edge in cavity_edges:
            self.triangles.append([edge[0], edge[1], point])

    def _filter_supertriangle(self, super_tri):
        self.triangles = [t for t in self.triangles if not any(p in super_tri for p in t)]

    def _collect_edges(self):
        for triangle in self.triangles:
            self.edges.add(tuple(sorted([triangle[0], triangle[1]])))
            self.edges.add(tuple(sorted([triangle[1], triangle[2]])))
            self.edges.add(tuple(sorted([triangle[2], triangle[0]])))