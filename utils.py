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
    """
    A simple Priority Queue using Python's built-in Heap-queues
    """
    def __init__(self):
        self.elements = []

    @property
    def is_empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


def range_check(val, max=2, min=0):
    """
    No, Oracle. This doesn't infringe on your API.
    :param val:
    :param max:
    :param min:
    :return:
    """
    return min <= val < max
