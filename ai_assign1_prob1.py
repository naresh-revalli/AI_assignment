class PuzzleState:
    def __init__(self, board, empty_idx):
        self.board = board
        self.empty_idx = empty_idx

    def is_goal(self):
        return self.board == ['w', 'w', 'w', '_', 'e', 'e', 'e']

    def generate_moves(self):
        directions = [-2, -1, 1, 2]
        successors = []
        for step in directions:
            new_idx = self.empty_idx + step
            if 0 <= new_idx < len(self.board):
                if (self.board[new_idx] == 'e' and self.empty_idx > new_idx) or \
                   (self.board[new_idx] == 'w' and self.empty_idx < new_idx):
                    new_board = self.board[:new_idx] + ['_'] + self.board[new_idx + 1:]
                    new_board[self.empty_idx] = self.board[new_idx]
                    successors.append(PuzzleState(new_board, new_idx))
        return successors

    def filter_seen(self, successors, frontier, explored):
        seen_open = [n for n, _ in frontier]
        seen_closed = [n for n, _ in explored]
        return [s for s in successors if s not in seen_open and s not in seen_closed]

    def build_path(self, explored, target_pair):
        path = []
        parent_map = {}
        for node, parent in explored:
            parent_map[node] = parent
        node, parent = target_pair
        parent_map[node] = parent
        while node is not None:
            path.append(node)
            node = parent_map[node]
        path.reverse()
        return path

    def __str__(self):
        print(self.board)
        return ''

    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        return hash(tuple(self.board))

    def dfs(self):
        frontier = [(self, None)]
        explored = []
        while frontier:
            current_pair = frontier.pop(0)
            current, parent = current_pair
            if current.is_goal():
                return self.build_path(explored, current_pair)
            else:
                explored.append(current_pair)
                next_states = current.generate_moves()
                unseen = current.filter_seen(next_states, frontier, explored)
                frontier = [(n, current) for n in unseen] + frontier
        return []

start = PuzzleState(['e', 'e', 'e', '_', 'w', 'w', 'w'], 3)
solution_path = start.dfs()
for state in solution_path:
    print(state)
    print()
