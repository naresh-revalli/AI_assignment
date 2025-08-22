import math

class Node:
    def __init__(self, position, grid):
        self.position = position  
        self.grid = grid

    def isGoal(self):
        return self.position[0] == len(self.grid) - 1 and self.position[1] == len(self.grid[0]) - 1

    def generateMoves(self):
        moves = [(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1)]
        successors = []
        for dr, dc in moves:
            new_r, new_c = self.position[0] + dr, self.position[1] + dc
            if (0 <= new_r < len(self.grid) and 0 <= new_c < len(self.grid[0]) 
                and self.grid[new_r][new_c] == 0):
                successors.append(Node((new_r, new_c), self.grid))
        return successors

    def heuristic(self):
        goal_r, goal_c = len(self.grid) - 1, len(self.grid[0]) - 1
        return math.sqrt((goal_r - self.position[0])**2 + (goal_c - self.position[1])**2)

    def getMinNode(self, frontier):
        best_val = float('inf')
        best_pair = (None, None)
        for pair in frontier:
            if pair[0].heuristic() < best_val:
                best_val = pair[0].heuristic()
                best_pair = pair
        return best_pair

    def filterSeen(self, frontier, explored, successors):
        frontier_nodes = [n for n, p in frontier]
        explored_nodes = [n for n, p in explored]
        return [s for s in successors if s not in frontier_nodes and s not in explored_nodes]

    def buildPath(self, explored, goal_pair):
        path = []
        parent_map = {node: parent for node, parent in explored}
        current = goal_pair[0]

        while current is not None:
            path.append(current)
            current = parent_map.get(current)

        return list(reversed(path))

    def bestFirstSearch(self):
        frontier = [(self, None)]
        explored = []

        while frontier:
            node_pair = self.getMinNode(frontier)
            current, parent = node_pair
            frontier.remove(node_pair)

            if current.isGoal():
                return self.buildPath(explored, node_pair)

            explored.append(node_pair)
            successors = current.generateMoves()
            successors = self.filterSeen(frontier, explored, successors)
            successor_pairs = [(s, current) for s in successors]
            frontier.extend(successor_pairs)

        return None

    def __str__(self):
        return str(self.position)

    def __hash__(self):
        return hash(self.position)

    def __eq__(self, other):
        return isinstance(other, Node) and self.position == other.position



grid = [
    [0, 1, 0, 1],
    [1, 0, 1, 0],
    [0, 1, 0, 1],
    [1, 0, 0, 0]
]

start_pos = (0, 0)
start_node = Node(start_pos, grid)

result_path = start_node.bestFirstSearch()
if result_path:
    print("Path found:")
    for step in result_path:
        print(step)
    print("Path length:", len(result_path))
else:
    print("No path exists.")
    print("Path length: -1")
