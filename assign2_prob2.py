class State:
    def __init__(self, loc, parent=None, cost=0):
        self.loc = loc             
        self.parent = parent        
        self.cost = cost            

    def __eq__(self, other):
        return isinstance(other, State) and self.loc == other.loc

    def __hash__(self):
        return hash(self.loc)


class Problem:
    def __init__(self, grid, start, goal):
        self.grid = grid
        self.start = start
        self.goal = goal
        self.rows = len(grid)
        self.cols = len(grid[0])

    def get_children(self, state):
        directions = [(0,1),(1,0),(0,-1),(-1,0),(-1,-1),(-1,1),(1,-1),(1,1)]
        children = []
        for d in directions:
            new_r = state.loc[0] + d[0]
            new_c = state.loc[1] + d[1]
            if 0 <= new_r < self.rows and 0 <= new_c < self.cols:
                if self.grid[new_r][new_c] != 1:  
                    child = State((new_r,new_c), parent=state, cost=state.cost+1)
                    children.append(child)
        return children

    def heuristic(self, state):
        # Manhattan distance
        return abs(state.loc[0] - self.goal[0]) + abs(state.loc[1] - self.goal[1])

    def a_star_search(self):
        start_state = State(self.start, cost=0)
        frontier = [(self.heuristic(start_state), start_state)]
        visited = set()

        while frontier:
            # Pick node with smallest f
            f, current = min(frontier, key=lambda x: x[0])
            frontier.remove((f, current))

            if current.loc == self.goal:
                return self.reconstruct_path(current)

            if current in visited:
                continue
            visited.add(current)

            for child in self.get_children(current):
                if child not in visited:
                    g = child.cost
                    h = self.heuristic(child)
                    f = g + h
                    frontier.append((f, child))

        return None  

    def reconstruct_path(self, state):
        path = []
        while state:
            path.append(state.loc)
            state = state.parent
        path.reverse()
        return path




grid = [
    [0,0,0,1,0],
    [0,1,0,1,0],
    [0,1,0,0,0],
    [0,0,0,1,0],
    [1,1,0,0,0]
]
start = (0,0)
goal = (4,4)

problem = Problem(grid, start, goal)
path = problem.a_star_search()

if path:
    print("Path:", path)
    print("Path length:", len(path)-1)
else:
    print("No path found, length = -1")
