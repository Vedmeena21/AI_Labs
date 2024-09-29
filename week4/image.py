import random
import math

def cost_function(puzzle):
    cost = 0
    for i in range(512):
        for j in range(512):
            if j + 1 != 512 and (j + 1) % 128 == 0:
                cost += abs(int(puzzle[(512*i) + j]) - int(puzzle[(512*i) + j + 1]))
            if i + 1 != 512 and (i + 1) % 128 == 0:
                cost += abs(int(puzzle[(512*i) + j]) - int(puzzle[(512*(i+1)) + j]))
    # print(cost)
    return cost

def swap_pieces(puzzle):
    i, j= random.sample(range(16), 2)
    r1 = int(i/4)
    r2 = int(j/4)
    c1 = int(i%4)
    c2 = int(j%4)
    rn1 = int(128 * r1)
    rn2 = int(128 * r2)
    cn1 = int(128 * c1)
    cn2 = int(128 * c2)
    piece1 = []
    piece2 = []
    for i in range(128):
        for j in range(128):
            if((512*(rn1 + i)) + (cn1 + j) >= 262144):
                print(i, j, rn1, cn1)
            piece1.append(puzzle[(512*(rn1 + i)) + (cn1 + j)])
    for i in range(128):
        for j in range(128):
            piece2.append(puzzle[(512*(rn2 + i)) + (cn2 + j)])
    for i in range(128):
        for j in range(128):
            puzzle[(512*(rn1 + i)) + (cn1 + j)] = piece2[(i * 128) + j]
    for i in range(128):
        for j in range(128):
            puzzle[(512*(rn2 + i)) + (cn2 + j)] = piece1[(i * 128) + j]

    return puzzle

def simulated_annealing(puzzle, T_initial, alpha, stopping_temp):
    minCost = 100000000
    minState = []
    c = 0
    T = T_initial
    current_state = puzzle
    current_cost = cost_function(current_state)
    
    while T > stopping_temp:
        c = c + 1
        new_state = swap_pieces(current_state.copy())
        new_cost = cost_function(new_state)
        # print(c, current_cost)
        if new_cost < current_cost:
            current_state = new_state
            current_cost = new_cost
            if(current_cost < minCost):
                minCost = current_cost
                minState = current_state.copy()
        else:
            if random.uniform(0, 1) < math.exp((current_cost - new_cost) / T):
                current_state = new_state
                current_cost = new_cost
        
        T *= alpha 
    
    return minState, minCost

puzzle = []
with open('scrambled_lena.mat', 'r') as file:
    for _ in range(5):  
        next(file)
    
    for line in file:
        puzzle.append(line)

ans = []
minCost = 1000000
for i in range(5):
    T_initial = 1000
    alpha = 0.99
    stopping_temp = 0.1
    solved_puzzle, cost = simulated_annealing(puzzle, T_initial, alpha, stopping_temp)
    if(cost < minCost):
        minCost = cost
        puzzle = solved_puzzle.copy()
        ans = puzzle
    print(cost)
with open('answer.mat', 'w') as file:
    for item in ans:
        file.write(f"{item}")