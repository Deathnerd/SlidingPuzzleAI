from utils import PriorityQueue, Infinity


class AStar:
    """
    An implementation of the AStar algorithm that uses a Priority Queue for efficient prioritization
    of nodes to visit when computing the path.
    """

    def __init__(self, graph, board):
        self.graph = graph
        self.board = board

    @staticmethod
    def heuristic(start, stop):
        """
        This heuristic is a simple greedy one. It tries to determine the overall distance
        from where you are to where you want to go.
        :param start:
        :param stop:
        :return:
        """
        (x1, y1) = start
        (x2, y2) = stop
        return abs(x1 - x2) + abs(y1 - y2)

    def search(self, start, goal, graph=None):
        """
        Perform the search. If given a new graph, replace the current one with it, and start fresh.
        Also, if specified, start fresh with the current graph. This is non-recursive and can therefore
        run infinitely until memory is exhausted.
        :param start: The node to start from
        :param goal: The node to go to
        :param graph: A fresh graph to start at (if specified)
        :return:
        """
        if graph is not None:
            self.graph = graph
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = dict()
        cost_so_far = dict()
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.is_empty:
            current = frontier.get()
            if current == goal:
                break
            for next in self.board.nodes_to_visit(current):
                new_cost = cost_so_far[current] + self.board.cost(next)
                if next not in cost_so_far or new_cost < cost_so_far.get(next, Infinity):
                    cost_so_far[next] = new_cost
                    priority = new_cost + AStar.heuristic(goal, next)
                    frontier.put(next, priority)
                    came_from[next] = current
        return came_from, cost_so_far