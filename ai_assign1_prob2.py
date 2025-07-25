import copy

class BridgeState:
    def __init__(self, people, torch_side, total_time):
        self.people = people
        self.torch_side = torch_side
        self.total_time = total_time

    def is_goal(self):
        return (
            self.people[0][1] == self.people[1][1] ==
            self.people[2][1] == self.people[3][1] == 'r'
            and self.total_time <= 65
        )

    def generate_moves(self):
        next_states = []
        if self.torch_side == 'l':
            for i in range(len(self.people) - 1):
                for j in range(i + 1, len(self.people)):
                    person1 = self.people[i]
                    person2 = self.people[j]
                    if person1[1] == person2[1] == 'l':
                        updated_people = copy.deepcopy(self.people)
                        updated_people[i][1] = 'r'
                        updated_people[j][1] = 'r'
                        crossing_time = max(person1[2], person2[2])
                        next_states.append(
                            BridgeState(updated_people, 'r', self.total_time + crossing_time)
                        )
        else:
            for i in range(len(self.people)):
                if self.people[i][1] == 'r':
                    updated_people = copy.deepcopy(self.people)
                    updated_people[i][1] = 'l'
                    next_states.append(
                        BridgeState(updated_people, 'l', self.total_time + updated_people[i][2])
                    )
        return next_states

    def filter_unseen(self, frontier, explored, children):
        frontier_states = [state for state, _ in frontier]
        explored_states = [state for state, _ in explored]
        return [child for child in children if child not in frontier_states and child not in explored_states]

    def build_path(self, explored, goal_pair):
        path = []
        parent_map = {}
        for node, parent in explored:
            parent_map[node] = parent
        node, parent = goal_pair
        parent_map[node] = parent
        while node:
            path.append(node)
            node = parent_map[node]
        path.reverse()
        return path

    def bfs(self):
        frontier = [(self, None)]
        explored = []
        while frontier:
            current_pair = frontier.pop(0)
            current_state, parent = current_pair
            if current_state.is_goal():
                return (self.build_path(explored, current_pair), current_state.total_time)
            explored.append(current_pair)
            children = current_state.generate_moves()
            unseen = self.filter_unseen(frontier, explored, children)
            new_pairs = [(child, current_state) for child in unseen]
            frontier.extend(new_pairs)

    def __eq__(self, other):
        return self.torch_side == other.torch_side and all(
            p1 == p2 for p1, p2 in zip(self.people, other.people)
        )

    def __hash__(self):
        return hash(tuple(tuple(person) for person in self.people))

    def __str__(self):
        return (
            "ayansh:" + self.people[0][1] + " "
            "ananya:" + self.people[1][1] + " "
            "grandma:" + self.people[2][1] + " "
            "grandpa:" + self.people[3][1]
        )

initial_state = BridgeState(
    [["ayansh", 'l', 5], ["ananya", 'l', 10], ["grandma", 'l', 20], ["grandpa", 'l', 25]],
    'l',
    0
)

result = initial_state.bfs()
for step in result[0]:
    print(step)
    print()

print("the required time to cross the bridge is:", result[1])
