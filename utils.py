from __future__ import print_function
import os
import heapq

project_root = os.path.dirname(os.path.realpath(__file__))
resource_root = os.path.join(project_root, "resources")
DIFFICULTY_EASY = 3
DIFFICULTY_MEDIUM = 5
DIFFICULTY_HARD = 8
Infinity = float('inf')


class PriorityQueue:
    def __init__(self):
        self.elements = []

    @property
    def is_empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


def draw_tile(graph, tile, start, end, path=list(), width=3):
    r = ""
    if tile == end:
        r = "P"
    if tile == start:
        r = "E"
    if tile in path:
        r = "@"
    if tile in graph.walls:
        r = "#" * width
    return r


def get_path(came_from, start, goal):
    current = goal
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def draw_grid(graph, start, end, width=2, path=list()):
    for y in range(graph.height):
        for x in range(graph.width):
            print("%%-%ds" % width % draw_tile(graph, (x, y), start, end, path, width), end="")
        print()


def range_check(val, max=2, min=0):
    return min <= val < max
