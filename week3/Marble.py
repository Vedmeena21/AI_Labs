import heapq

class SolitaireState:
    def __init__(self, board, empty_pos, cost):
        self.board = tuple(board)
        self.empty_pos = empty_pos
        self.cost = cost

    def __lt__(self, other):
        return (self.cost + self.calculate_heuristic()) < (other.cost + other.calculate_heuristic())

    def calculate_heuristic(self):
        return sum(row.count('O') for row in self.board)

def is_move_valid(board, empty_pos, move):
    row, col = empty_pos

    if move == "up":
        return row >= 2 and board[row - 1][col] == 'O' and board[row - 2][col] == '.'
    elif move == "down":
        return row < len(board) - 2 and board[row + 1][col] == 'O' and board[row + 2][col] == '.'
    elif move == "left":
        return col >= 2 and board[row][col - 1] == 'O' and board[row][col - 2] == '.'
    elif move == "right":
        return col < len(board[0]) - 2 and board[row][col + 1] == 'O' and board[row][col + 2] == '.'

def make_move(board, empty_pos, move):
    row, col = empty_pos
    new_board = [list(r) for r in board]

    if move == "up":
        new_board[row - 1][col] = '.'
        new_board[row - 2][col] = 'O'
    elif move == "down":
        new_board[row + 1][col] = '.'
        new_board[row + 2][col] = 'O'
    elif move == "left":
        new_board[row][col - 1] = '.'
        new_board[row][col - 2] = 'O'
    elif move == "right":
        new_board[row][col + 1] = '.'
        new_board[row][col + 2] = 'O'

    return ["".join(r) for r in new_board]

def new_empty_position(empty_pos, move):
    row, col = empty_pos

    if move == "up":
        return (row - 2, col)
    elif move == "down":
        return (row + 2, col)
    elif move == "left":
        return (row, col - 2)
    elif move == "right":
        return (row, col + 2)

def is_goal_reached(state):
    center_row = len(state.board) // 2
    center_col = len(state.board[0]) // 2
    return state.board[center_row][center_col] == 'O' and sum(row.count('O') for row in state.board) == 1

def solve_marble_solitaire(initial_state):
    visited = set()
    priority_queue = [initial_state]

    while priority_queue:
        current_state = heapq.heappop(priority_queue)

        if current_state.board in visited:
            continue

        visited.add(current_state.board)

        if is_goal_reached(current_state):
            return current_state

        for move in available_moves:
            if is_move_valid(current_state.board, current_state.empty_pos, move):
                new_board = make_move(current_state.board, current_state.empty_pos, move)
                new_empty_pos = new_empty_position(current_state.empty_pos, move)
                new_cost = current_state.cost + 1

                new_state = SolitaireState(new_board, new_empty_pos, new_cost)
                heapq.heappush(priority_queue, new_state)

    return None

initial_board_config = [
    "    OOO    ",
    "    OOO    ",
    "OOOOOOOOOOO",
    "OOOOO.OOOOO",
    "OOOOOOOOOOO",
    "    OOO    ",
    "    OOO    "
]
initial_empty_pos = (3, 4)

initial_state = SolitaireState(initial_board_config, initial_empty_pos, 0)

available_moves = ["up", "down", "left", "right"]

solution_state = solve_marble_solitaire(initial_state)

if solution_state:
    print("Solution found!")
    print("Path cost:", solution_state.cost)
    print("Final board:")
    for row in solution_state.board:
        print(row)
else:
    print("No solution found.")
