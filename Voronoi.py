import math
import heapq
import itertools


class Coordinate:
    def __init__(self, x_coord, y_coord):
        self.x = x_coord
        self.y = y_coord


class VoronoiEvent:
    def __init__(self, x_val, point, arc_ref=None):
        self.x = x_val
        self.point = point
        self.arc = arc_ref
        self.is_valid = True


class ParabolaArc:
    def __init__(self, focal_point, prev_arc=None, next_arc=None):
        self.focus = focal_point
        self.prev = prev_arc
        self.next = next_arc
        self.event = None
        self.segment_left = None
        self.segment_right = None


class VoronoiSegment:
    def __init__(self, start_point):
        self.start = start_point
        self.end = None
        self.completed = False

    def complete(self, end_point):
        if not self.completed:
            self.end = end_point
            self.completed = True


class EventQueue:
    def __init__(self):
        self.queue = []
        self.entries = {}
        self.counter = itertools.count()

    def add(self, event):
        if event in self.entries:
            return
        count = next(self.counter)
        entry = [event.x, count, event]
        self.entries[event] = entry
        heapq.heappush(self.queue, entry)

    def remove(self, event):
        if event in self.entries:
            entry = self.entries.pop(event)
            entry[-1] = None

    def get_next(self):
        while self.queue:
            _, count, event = heapq.heappop(self.queue)
            if event is not None:
                del self.entries[event]
                return event
        raise KeyError("Attempt to pop from an empty queue")

    def peek(self):
        while self.queue:
            _, count, event = heapq.heappop(self.queue)
            if event is not None:
                del self.entries[event]
                self.add(event)
                return event
        raise KeyError("Attempt to peek an empty queue")

    def is_empty(self):
        return len(self.queue) == 0


class VoronoiDiagram:
    def __init__(self, input_points):
        self.segments = []
        self.beach_line = None
        self.site_queue = EventQueue()
        self.circle_queue = EventQueue()
        self.bounds = {'left': float('inf'), 'right': float('-inf'), 'top': float('inf'), 'bottom': float('-inf')}
        for x, y in input_points:
            point = Coordinate(x, y)
            self.site_queue.add(VoronoiEvent(x, point))
            self.bounds['left'] = min(self.bounds['left'], x)
            self.bounds['right'] = max(self.bounds['right'], x)
            self.bounds['top'] = min(self.bounds['top'], y)
            self.bounds['bottom'] = max(self.bounds['bottom'], y)
        width = self.bounds['right'] - self.bounds['left'] + 1
        height = self.bounds['bottom'] - self.bounds['top'] + 1
        self.bounds['left'] -= width / 5
        self.bounds['right'] += width / 5
        self.bounds['top'] -= height / 5
        self.bounds['bottom'] += height / 5

    def construct(self):
        while not self.site_queue.is_empty():
            if not self.circle_queue.is_empty() and self.circle_queue.peek().x <= self.site_queue.peek().x:
                self._handle_circle_event()
            else:
                self._handle_site_event()
        while not self.circle_queue.is_empty():
            self._handle_circle_event()
        self._finalize_segments()

    def _handle_site_event(self):
        event = self.site_queue.get_next()
        self._insert_arc(event.point)

    def _handle_circle_event(self):
        event = self.circle_queue.get_next()
        if event.is_valid:
            segment = VoronoiSegment(event.point)
            self.segments.append(segment)
            arc = event.arc
            if arc.prev:
                arc.prev.next = arc.next
                arc.prev.segment_right = segment
            if arc.next:
                arc.next.prev = arc.prev
                arc.next.segment_left = segment
            if arc.segment_left:
                arc.segment_left.complete(event.point)
            if arc.segment_right:
                arc.segment_right.complete(event.point)
            if arc.prev:
                self._check_for_circle_event(arc.prev, event.x)
            if arc.next:
                self._check_for_circle_event(arc.next, event.x)

    def _insert_arc(self, point):
        if not self.beach_line:
            self.beach_line = ParabolaArc(point)
            return
        current = self.beach_line
        while current:
            intersects, intersection_point = self._find_intersection(point, current)
            if intersects:
                if current.next and not self._find_intersection(point, current.next)[0]:
                    current.next.prev = ParabolaArc(current.focus, current, current.next)
                    current.next = current.next.prev
                else:
                    current.next = ParabolaArc(current.focus, current)
                current.next.segment_right = current.segment_right
                current.next.prev = ParabolaArc(point, current, current.next)
                current.next = current.next.prev
                current = current.next
                segment = VoronoiSegment(intersection_point)
                self.segments.append(segment)
                current.prev.segment_right = current.segment_left = segment
                segment = VoronoiSegment(intersection_point)
                self.segments.append(segment)
                current.next.segment_left = current.segment_right = segment
                self._check_for_circle_event(current, point.x)
                self._check_for_circle_event(current.prev, point.x)
                self._check_for_circle_event(current.next, point.x)
                return
            current = current.next
        current = self.beach_line
        while current.next:
            current = current.next
        current.next = ParabolaArc(point, current)
        x = self.bounds['left']
        y = (current.next.focus.y + current.focus.y) / 2
        start = Coordinate(x, y)
        segment = VoronoiSegment(start)
        current.segment_right = current.next.segment_left = segment
        self.segments.append(segment)

    def _check_for_circle_event(self, arc, x_val):
        if arc.event and arc.event.x != self.bounds['left']:
            arc.event.is_valid = False
        arc.event = None
        if not arc.prev or not arc.next:
            return
        valid, x, center = self._compute_circle(arc.prev.focus, arc.focus, arc.next.focus)
        if valid and x > self.bounds['left']:
            arc.event = VoronoiEvent(x, center, arc)
            self.circle_queue.add(arc.event)

    def _compute_circle(self, a, b, c):
        if (b.x - a.x) * (c.y - a.y) - (c.x - a.x) * (b.y - a.y) > 0:
            return False, None, None
        A = b.x - a.x
        B = b.y - a.y
        C = c.x - a.x
        D = c.y - a.y
        E = A * (a.x + b.x) + B * (a.y + b.y)
        F = C * (a.x + c.x) + D * (a.y + c.y)
        G = 2 * (A * (c.y - b.y) - B * (c.x - b.x))
        if G == 0:
            return False, None, None
        ox = (D * E - B * F) / G
        oy = (A * F - C * E) / G
        x = ox + math.sqrt((a.x - ox) ** 2 + (a.y - oy) ** 2)
        return True, x, Coordinate(ox, oy)

    def _find_intersection(self, point, arc):
        if not arc or arc.focus.x == point.x:
            return False, None
        a = b = 0
        if arc.prev:
            a = self._parabola_intersection(arc.prev.focus, arc.focus, point.x).y
        if arc.next:
            b = self._parabola_intersection(arc.focus, arc.next.focus, point.x).y
        if (not arc.prev or a <= point.y) and (not arc.next or point.y <= b):
            py = point.y
            px = ((arc.focus.x ** 2 + (arc.focus.y - py) ** 2 - point.x ** 2) / (2 * arc.focus.x - 2 * point.x))
            return True, Coordinate(px, py)
        return False, None

    def _parabola_intersection(self, p0, p1, l):
        p = p0
        if p0.x == p1.x:
            py = (p0.y + p1.y) / 2
        elif p1.x == l:
            py = p1.y
        elif p0.x == l:
            py = p0.y
            p = p1
        else:
            z0 = 2 * (p0.x - l)
            z1 = 2 * (p1.x - l)
            a = 1 / z0 - 1 / z1
            b = -2 * (p0.y / z0 - p1.y / z1)
            c = (p0.y ** 2 + p0.x ** 2 - l ** 2) / z0 - (p1.y ** 2 + p1.x ** 2 - l ** 2) / z1
            py = (-b - math.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
        px = (p.x ** 2 + (p.y - py) ** 2 - l ** 2) / (2 * p.x - 2 * l)
        return Coordinate(px, py)

    def _finalize_segments(self):
        l = self.bounds['right'] + (self.bounds['right'] - self.bounds['left']) + (self.bounds['bottom'] - self.bounds['top'])
        current = self.beach_line
        while current and current.next:
            if current.segment_right:
                point = self._parabola_intersection(current.focus, current.next.focus, l * 2)
                current.segment_right.complete(point)
            current = current.next

    def get_segments(self):
        return [(seg.start.x, seg.start.y, seg.end.x, seg.end.y) for seg in self.segments if seg.completed]