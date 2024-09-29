from string import ascii_lowercase
import random
from itertools import combinations

print("Enter the number of clauses: ")
num_clauses = int(input())
print("Enter the number of variables in a clause: ")
num_vars_in_clause = int(input())
print("Enter the total number of variables: ")
total_vars = int(input())

def generate_problem(num_clauses, num_vars_in_clause, total_vars):
    pos_vars = list(ascii_lowercase)[:total_vars]
    neg_vars = [var.upper() for var in pos_vars]
    all_vars = pos_vars + neg_vars
    
    max_attempts = 9
    unique_problems = []
    all_combinations = list(combinations(all_vars, num_vars_in_clause))
    attempts = 0

    while attempts < max_attempts:
        selected_clauses = random.sample(all_combinations, num_clauses)
        if selected_clauses not in unique_problems:
            attempts += 1
            unique_problems.append(list(selected_clauses))
    
    formatted_problems = []
    for clause_group in unique_problems:
        temp_group = []
        for clause in clause_group:
            temp_group.append(list(clause))
        formatted_problems.append(temp_group)
    
    return unique_problems

generated_problems = generate_problem(num_clauses, num_vars_in_clause, total_vars)

for problem in generated_problems:
    print(problem)
