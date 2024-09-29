from string import ascii_lowercase
import random
from itertools import combinations
import numpy as np

print("Enter the number of clauses: ")
m = int(input())
print("Enter the number of variables in each clause: ")
k = int(input())
print("Enter the total number of variables: ")
n = int(input())

def gen_prob(m, k, n):
    pos_vars = list(ascii_lowercase)[:n]
    neg_vars = [v.upper() for v in pos_vars]
    all_vars = pos_vars + neg_vars
    
    max_attempts = 10
    unique_probs = []
    all_combs = list(combinations(all_vars, k))
    attempts = 0

    while attempts < max_attempts:
        sel_clauses = random.sample(all_combs, m)
        if sel_clauses not in unique_probs:
            attempts += 1
            unique_probs.append(list(sel_clauses))
    
    return all_vars, unique_probs

vars, probs = gen_prob(m, k, n)

def create_assign(vars, n):
    pos_assign = list(np.random.choice(2, n))
    neg_assign = [1 - i for i in pos_assign]
    combined_assign = pos_assign + neg_assign
    return dict(zip(vars, combined_assign))

assign = create_assign(vars, n)
print(assign)
print(probs[0])

def eval_sol(prob, assign):
    count = 0
    for clause in prob:
        literals = [assign[v] for v in clause]
        count += any(literals)
    return count

def hill_climb(prob, assign, best_score, steps, iter_count):
    best_assign = assign.copy()
    vals = list(assign.values())
    keys = list(assign.keys())

    max_score = best_score
    max_assign = assign.copy()
    
    for i in range(len(vals)):
        iter_count += 1
        assign[keys[i]] = 1 - vals[i]
        score = eval_sol(prob, assign)
        
        if score > max_score:
            steps = iter_count
            max_score = score
            max_assign = assign.copy()
    
    if max_score == best_score:
        return best_assign, max_score, f"{steps}/{iter_count - len(vals)}"
    else:
        best_score = max_score
        best_assign = max_assign.copy()
        return hill_climb(prob, best_assign, best_score, steps, iter_count)

def beam_search(prob, assign, b, steps):
    best_assign = assign.copy()
    vals = list(assign.values())
    keys = list(assign.keys())
    possible_assigns = []
    possible_scores = []

    init_score = eval_sol(prob, assign)
    if init_score == len(prob):
        return assign, f"{steps}/{steps}"

    for i in range(len(vals)):
        steps += 1
        assign[keys[i]] = 1 - vals[i]
        score = eval_sol(prob, assign)
        possible_assigns.append(assign.copy())
        possible_scores.append(score)
    
    best_indices = np.argsort(possible_scores)[-b:]
    
    if len(prob) in possible_scores:
        success_index = [i for i, score in enumerate(possible_scores) if score == len(prob)]
        return possible_assigns[success_index[0]], f"{steps}/{steps}"

    selected_assigns = [possible_assigns[i] for i in best_indices]
    for a in selected_assigns:
        return beam_search(prob, a, b, steps)

def var_neigh_search(prob, assign, b, steps):
    best_assign = assign.copy()
    vals = list(assign.values())
    keys = list(assign.keys())
    possible_assigns = []
    possible_scores = []

    init_score = eval_sol(prob, assign)
    if init_score == len(prob):
        return assign, f"{steps}/{steps}", b

    for i in range(len(vals)):
        steps += 1
        assign[keys[i]] = 1 - vals[i]
        score = eval_sol(prob, assign)
        possible_assigns.append(assign.copy())
        possible_scores.append(score)
    
    best_indices = np.argsort(possible_scores)[-b:]

    if len(prob) in possible_scores:
        success_index = [i for i, score in enumerate(possible_scores) if score == len(prob)]
        return possible_assigns[success_index[0]], f"{steps}/{steps}", b
    
    selected_assigns = [possible_assigns[i] for i in best_indices]
    for a in selected_assigns:
        return var_neigh_search(prob, a, b + 1, steps)

hill_assigns = []
init_assigns = []
hill_scores = []
init_scores = []
hill_pen = []
beam_pen = []
var_pen = []
var_assigns = []
beam_assigns = []

for idx, prob in enumerate(probs, start=1):
    init_assign = create_assign(vars, n)
    init_score = eval_sol(prob, init_assign)
    
    best_assign, best_score, hill_pen_info = hill_climb(prob, init_assign, init_score, 1, 1)
    hill_assigns.append(best_assign)
    init_assigns.append(init_assign)
    hill_scores.append(best_score)
    init_scores.append(init_score)
    hill_pen.append(hill_pen_info)

    beam_assign_3, beam_pen_info_3 = beam_search(prob, init_assign, 3, 1)
    beam_assigns.append(beam_assign_3)
    beam_pen.append(beam_pen_info_3)

    beam_assign_4, beam_pen_info_4 = beam_search(prob, init_assign, 4, 1)
    
    var_assign, var_pen_info, var_width = var_neigh_search(prob, init_assign, 1, 1)
    var_pen.append(var_pen_info)
    var_assigns.append(var_assign)
    
    print(f'Problem {idx}: {prob}')
    print(f'Hill Climbing: {best_assign}, Penetration: {hill_pen_info}')
    print(f'Beam Search (3): {beam_assign_3}, Penetration: {beam_pen_info_3}')
    print(f'Beam Search (4): {beam_assign_4}, Penetration: {beam_pen_info_4}')
    print(f'Variable Neighborhood Search: {var_assign}, Penetration: {var_pen_info}')
    print()
