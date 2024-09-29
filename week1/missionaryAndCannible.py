from collections import deque

class State:
    def __init__(self, missionaries, cannibals, boat):
        self.missionaries = missionaries
        self.cannibals = cannibals
        self.boat = boat

    def is_valid(self):
        if self.missionaries < 0 or self.cannibals < 0 or self.missionaries > 3 or self.cannibals > 3:
            return False
        if self.missionaries > 0 and self.missionaries < self.cannibals:
            return False
        if self.missionaries < 3 and (3 - self.missionaries) < (3 - self.cannibals):
            return False
        return True

    def is_goal(self):
        return self.missionaries == 0 and self.cannibals == 0 and self.boat == 0

    def __eq__(self, other):
        return (self.missionaries, self.cannibals, self.boat) == (other.missionaries, other.cannibals, other.boat)

    def __hash__(self):
        return hash((self.missionaries, self.cannibals, self.boat))

    def __repr__(self):
        return f"({self.missionaries}, {self.cannibals}, {self.boat})"

def bfs()->int:
    start = State(3, 3, 1)
    queue = deque([(start, [start])])
    visited = set()
    visited.add(start)
    stateTraversed = 0;

    moves = [(1, 0), (0, 1), (1, 1), (2, 0), (0, 2)]

    while queue:
        current, path = queue.popleft()
        stateTraversed = stateTraversed + 1
        if current.is_goal():
            print("BFS Solution found!")
            print("Total Number of state Traversed in BFS solution are :", stateTraversed);
            for state in path:
                print(state)
            return stateTraversed

        for move in moves:
            next_state = State(
                current.missionaries - move[0] * current.boat,
                current.cannibals - move[1] * current.boat,
                1 - current.boat
            )

            if next_state.is_valid() and next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, path + [next_state]))

    print("No solution found with BFS.")
    return -1;

def dfs()->int:
    start = State(3, 3, 1)
    stack = [(start, [start])]
    visited = set()
    visited.add(start)
    stateTraversed = 0

    moves = [(1, 0), (0, 1), (1, 1), (2, 0), (0, 2)]

    while stack:
        current, path = stack.pop()
        stateTraversed = stateTraversed + 1
        if current.is_goal():
            print("DFS Solution found!")
            print("Total Number of state Traversed in BFS solution are :", stateTraversed);
            for state in path:
                print(state)
            return stateTraversed

        for move in moves:
            next_state = State(
                current.missionaries - move[0] * current.boat,
                current.cannibals - move[1] * current.boat,
                1 - current.boat
            )

            if next_state.is_valid() and next_state not in visited:
                visited.add(next_state)
                stack.append((next_state, path + [next_state]))

    print("No solution found with DFS.")
    return -1

if __name__ == "__main__":
    print("Running BFS:")
    bfsStates = bfs()
    print("\nRunning DFS:")
    dfsStates = dfs()

    if(bfsStates < dfsStates):
        print("BFS traversal Solution is good")
    
    else:
        print("DFS traversal solution is good");
    
