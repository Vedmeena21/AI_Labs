import numpy as np
import matplotlib.pyplot as plt

BOARD_SIZE = 8
N = BOARD_SIZE * BOARD_SIZE

def create_weight_matrix():
    W = np.zeros((N, N))
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            for k in range(BOARD_SIZE):
                W[i * BOARD_SIZE + j, i * BOARD_SIZE + k] = -1
                W[i * BOARD_SIZE + j, k * BOARD_SIZE + j] = -1
            for m in range(BOARD_SIZE):
                for n in range(BOARD_SIZE):
                    if m != i and n != j:
                        W[i * BOARD_SIZE + j, m * BOARD_SIZE + n] = 1
    np.fill_diagonal(W, 0)
    return W

def hopfield_update(W, x):
    for i in range(len(x)):
        s = np.dot(W[i], x)
        x[i] = 1 if s > 0 else -1
    return x

def initialize_state():
    return np.random.choice([-1, 1], size=N)

def convert_to_board(state):
    return state.reshape((BOARD_SIZE, BOARD_SIZE))

def visualize_board(board):
    plt.imshow(board, cmap='binary', interpolation='nearest')
    plt.title("Current Configuration of Rooks")
    plt.show()

def solve_eight_rook():
    W = create_weight_matrix()
    x = initialize_state()
    
    print("Starting the Hopfield network with an initial random configuration...\n")
    
    for iteration in range(100):
        x = hopfield_update(W, x)
        board = convert_to_board(x)
        visualize_board(board)
        
        if np.sum(np.abs(board)) == 8:
            print(f"Converged in {iteration + 1} iterations.\nFinal configuration:")
            visualize_board(board)
            break

def main():
    print("Welcome to the Eight-Rook Problem Solver using Hopfield Network!")
    solve_eight_rook()

if __name__ == "__main__":
    main()
