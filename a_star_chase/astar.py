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

    def search(self, start, goal):
        """
        Perform the search. If given a new graph, replace the current one with it, and start fresh.
        Also, if specified, start fresh with the current graph. This is non-recursive and can therefore
        run infinitely until memory is exhausted.
        :param start: The node to start from
        :param goal: The node to go to
        :return:
        """
        # start with a Priority Queue to hold the nodes to visit.
        # A priority queue means we'll visit the most promising nodes first
        # because they'll get higher priority
        to_visit = PriorityQueue()
        # But for now, we need to start by only knowing where we're at. It has lowest
        # priority because when you're trying to catch someone, (in this case) it's
        # best to keep moving
        to_visit.put(start, 0)
        # Yay hash tables! This will store the path we took while visiting nodes. Sorta kinda
        # like a linked list, but not (almost)
        visited = dict()
        # Woo hash tables! Here we'll store hashes of the nodes (tuples) we visit
        # and their costs
        costs = dict()
        # We've visited where we're starting from. It's nice and all, but the scenery is
        # kinda bland. Oh and we didn't arrive here from anywhere, so the previous node
        # is nothing.
        visited[start] = None
        # It didn't cost us anything to get here, which is nice since I'm pretty broke
        costs[start] = 0

        # While we have things in the queue to visit, check out the neighbors
        # and see if they're worth visiting. I mean, I'm sure they're lovely people
        # and all, but if they can't get us to our destination, then we don't need to
        # waste our time. It's the capitalist way! Also, they're weird and have electric
        # lawnmowers.
        while not to_visit.is_empty:
            # Travel to the next best node
            current = to_visit.get()
            # Hey! We got to where we needed to go!
            if current == goal:
                break
            # Here's where we figure out if we're gonna be neighborly and visit nodes
            # surrounding us. Reasons for not visiting our neighbors:
            #  1) They're a wall. It'd look weird to visit a wall
            #  2) It'd be more costly to visit them than others.
            #  3) They support Trump
            #  4) They use electric lawnmowers
            #  5) They're clingy
            #  6) They always ask for a cup of sugar but when you try to reciprocate,
            #     they're always suddenly out
            #  7) They listen to Insane Clown Posse
            for next in self.board.nodes_to_visit(current):
                new_cost = costs[current] + self.board.cost(next)
                # See item two in the above list
                if next not in costs or new_cost < costs.get(next, Infinity):
                    # Oh hey, it's cheaper to visit them than not. Cool!
                    # Record the cost of visiting the neighbor
                    costs[next] = new_cost
                    # Figure out where they stand on your priorities list
                    # and put them in the Queue. Hermes would be proud
                    to_visit.put(next, new_cost + AStar.heuristic(goal, next))
                    # Mark down how you got to them
                    visited[next] = current
        # Okay, we've figured out a path. It's... somewhere in here. Hrm...
        return visited, costs

    def get_path(self, came_from, start, goal):
        """
        Given a list of visited nodes, find the quickest path to get from start
        to goal
        :param came_from: a list of paths that contains a path from start to goal
        :param start: Where we're starting
        :param goal: Where we're going
        :return:
        """
        # just like solving a maze on paper, it's actually easier to
        # go backwards than it is to go forwards. Also, because of how
        # we're storing visited nodes, we kinda have to do this (since getting
        # a node points backwards to the previous node, closing in on the
        # starting point)
        current = goal
        # start the path with the goal
        path = [current]
        # While we're not at the start, follow the breadcrumbs
        # until we get there
        while current != start:
            # Get the next previous node... I know, that's confusing. Just trust me
            current = came_from[current]
            # add it to our path
            path.append(current)
        # since we started from the end and made our way to the beginning, reverse it
        # before we return it so we can just follow it like normal people
        path.reverse()
        return path
