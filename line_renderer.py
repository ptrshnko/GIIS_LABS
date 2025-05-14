import numpy as np

class LineRenderer:
    def render_line(self, x0, y0, x1, y1, debug=False):
        raise NotImplementedError

class DDALineRenderer(LineRenderer):
    def render_line(self, x0, y0, x1, y1, debug=False):
        height = 100
        width = 100
        grid = np.zeros((height, width))
        grid_x0 = int(x0)
        grid_y0 = int(y0)
        grid_x1 = int(x1)
        grid_y1 = int(y1)

        dx = grid_x1 - grid_x0
        dy = grid_y1 - grid_y0
        steps = max(abs(dx), abs(dy))

        if steps == 0:
            if 0 <= grid_y0 < height and 0 <= grid_x0 < width:
                grid[grid_y0][grid_x0] = 1
                return [np.copy(grid)] if debug else grid
            return [] if debug else grid

        step_x = dx / steps if steps > 0 else 0
        step_y = dy / steps if steps > 0 else 0

        intermediate_grids = []
        for i in range(steps + 1):
            x = grid_x0 + i * step_x
            y = grid_y0 + i * step_y
            gx = int(round(x))
            gy = int(round(y))
            if 0 <= gy < height and 0 <= gx < width:
                grid[gy][gx] = 1
                if debug:
                    intermediate_grids.append(np.copy(grid))

        return intermediate_grids if debug else grid

class BresenhamLineRenderer(LineRenderer):
    def render_line(self, x0, y0, x1, y1, debug=False):
        height = 100
        width = 100
        grid = np.zeros((height, width))
        grid_x0 = int(x0)
        grid_y0 = int(y0)
        grid_x1 = int(x1)
        grid_y1 = int(y1)

        dx = abs(grid_x1 - grid_x0)
        dy = abs(grid_y1 - grid_y0)
        sx = 1 if grid_x0 < grid_x1 else -1
        sy = 1 if grid_y0 < grid_y1 else -1
        err = dx - dy

        intermediate_grids = []
        while True:
            if 0 <= grid_y0 < height and 0 <= grid_x0 < width:
                grid[grid_y0][grid_x0] = 1
                if debug:
                    intermediate_grids.append(np.copy(grid))
            if grid_x0 == grid_x1 and grid_y0 == grid_y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                grid_x0 += sx
            if e2 < dx:
                err += dx
                grid_y0 += sy

        return intermediate_grids if debug else grid

class WuLineRenderer(LineRenderer):
    def render_line(self, x0, y0, x1, y1, debug=False):
        height = 100
        width = 100
        grid = np.zeros((height, width))
        grid_x0 = x0
        grid_y0 = y0
        grid_x1 = x1
        grid_y1 = y1

        steep = abs(grid_y1 - grid_y0) > abs(grid_x1 - grid_x0)
        if steep:
            grid_x0, grid_y0 = grid_y0, grid_x0
            grid_x1, grid_y1 = grid_y1, grid_x1
        if grid_x0 > grid_x1:
            grid_x0, grid_x1 = grid_x1, grid_x0
            grid_y0, grid_y1 = grid_y1, grid_y0

        dx = grid_x1 - grid_x0
        dy = grid_y1 - grid_y0
        gradient = dy / dx if dx != 0 else 0

        intermediate_grids = []

        xpxl1 = round(grid_x0)
        ypxl1 = grid_y0
        if steep:
            if 0 <= xpxl1 < height and 0 <= ypxl1 < width:
                grid[xpxl1][int(ypxl1)] = 1
        else:
            if 0 <= ypxl1 < height and 0 <= xpxl1 < width:
                grid[int(ypxl1)][xpxl1] = 1
        if debug:
            intermediate_grids.append(np.copy(grid))

        xpxl2 = round(grid_x1)
        ypxl2 = grid_y1
        if steep:
            if 0 <= xpxl2 < height and 0 <= ypxl2 < width:
                grid[xpxl2][int(ypxl2)] = 1
        else:
            if 0 <= ypxl2 < height and 0 <= xpxl2 < width:
                grid[int(ypxl2)][xpxl2] = 1
        if debug:
            intermediate_grids.append(np.copy(grid))

        if dx == 0:
            if steep:
                start_y = min(int(grid_y0), int(grid_y1))
                end_y = max(int(grid_y0), int(grid_y1))
                x = int(grid_x0)
                for y in range(start_y, end_y + 1):
                    if 0 <= x < height and 0 <= y < width:
                        grid[x][y] = 1
                        if debug:
                            intermediate_grids.append(np.copy(grid))
            return intermediate_grids if debug else grid

        intery = grid_y0 + gradient
        for x in range(xpxl1 + 1, xpxl2):
            if steep:
                y_floor = int(intery)
                frac = intery - y_floor
                if 0 <= x < height and 0 <= y_floor < width:
                    grid[x][y_floor] = 1 - frac
                if 0 <= x < height and 0 <= y_floor + 1 < width:
                    grid[x][y_floor + 1] = frac
            else:
                y_floor = int(intery)
                frac = intery - y_floor
                if 0 <= y_floor < height and 0 <= x < width:
                    grid[y_floor][x] = 1 - frac
                if 0 <= y_floor + 1 < height and 0 <= x < width:
                    grid[y_floor + 1][x] = frac
            if debug:
                intermediate_grids.append(np.copy(grid))
            intery += gradient

        return intermediate_grids if debug else grid