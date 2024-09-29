from collections import deque

def print_state(state):
    print(" ".join(state))

def move_rabbit(state, from_pos, to_pos):
    state[to_pos], state[from_pos] = state[from_pos], state[to_pos]

def bfs_solve_rabbit_leap(initial_state):
    goal_state = ['W', 'W', 'W', '_', 'E', 'E', 'E']
    queue = deque([(initial_state, [])])
    visited = set()
    visited.add(tuple(initial_state))

    while queue:
        current_state, path = queue.popleft()
        print_state(current_state)
        if current_state == goal_state:
            return path

        empty_pos = current_state.index('_')
        possible_moves = []

        # Left moves
        if empty_pos - 1 >= 0 and current_state[empty_pos - 1] == 'E':
            possible_moves.append((empty_pos - 1, empty_pos))
        if empty_pos - 2 >= 0 and current_state[empty_pos - 2] == 'E' and current_state[empty_pos - 1] == 'W':
            possible_moves.append((empty_pos - 2, empty_pos))

        # Right moves
        if empty_pos + 1 < len(current_state) and current_state[empty_pos + 1] == 'W':
            possible_moves.append((empty_pos + 1, empty_pos))
        if empty_pos + 2 < len(current_state) and current_state[empty_pos + 2] == 'W' and current_state[empty_pos + 1] == 'E':
            possible_moves.append((empty_pos + 2, empty_pos))

        for pos, new_pos in possible_moves:
            new_state = current_state[:]
            move_rabbit(new_state, pos, new_pos)
            if tuple(new_state) not in visited:
                visited.add(tuple(new_state))
                queue.append((new_state, path + [(pos, new_pos)]))

    return None

def dfs_solve_rabbit_leap(initial_state):
    goal_state = ['W', 'W', 'W', '_', 'E', 'E', 'E']
    stack = [(initial_state, [])]
    visited = set()
    visited.add(tuple(initial_state))

    while stack:
        current_state, path = stack.pop()
        print_state(current_state)
        if current_state == goal_state:
            return path

        empty_pos = current_state.index('_')
        possible_moves = []

        # Left moves
        if empty_pos - 1 >= 0 and current_state[empty_pos - 1] == 'E':
            possible_moves.append((empty_pos - 1, empty_pos))
        if empty_pos - 2 >= 0 and current_state[empty_pos - 2] == 'E' and current_state[empty_pos - 1] == 'W':
            possible_moves.append((empty_pos - 2, empty_pos))

        # Right moves
        if empty_pos + 1 < len(current_state) and current_state[empty_pos + 1] == 'W':
            possible_moves.append((empty_pos + 1, empty_pos))
        if empty_pos + 2 < len(current_state) and current_state[empty_pos + 2] == 'W' and current_state[empty_pos + 1] == 'E':
            possible_moves.append((empty_pos + 2, empty_pos))

        for pos, new_pos in possible_moves:
            new_state = current_state[:]
            move_rabbit(new_state, pos, new_pos)
            if tuple(new_state) not in visited:
                visited.add(tuple(new_state))
                stack.append((new_state, path + [(pos, new_pos)]))

    return None

if __name__ == "__main__":
    initial_state = ['E', 'E', 'E', '_', 'W', 'W', 'W']
    
    print("BFS Initial State:")
    print_state(initial_state)
    print("\nBFS Solving...\n")
    bfs_moves = bfs_solve_rabbit_leap(initial_state)
    
    if bfs_moves:
        print("\nBFS Solution found!")
        print(f"Moves: {bfs_moves}")
    else:
        print("No solution found with BFS.")

    print("\nDFS Initial State:")
    print_state(initial_state)
    print("\nDFS Solving...\n")
    dfs_moves = dfs_solve_rabbit_leap(initial_state)
    
    if dfs_moves:
        print("\nDFS Solution found!")
        print(f"Moves: {dfs_moves}")
    else:
        print("No solution found with DFS.")
