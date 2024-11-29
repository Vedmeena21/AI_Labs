import numpy as np
import matplotlib.pyplot as plt

num_cities = 10

def generate_distances(num_cities):
    distances = np.random.rand(num_cities, num_cities) * 100
    np.fill_diagonal(distances, 0)
    return (distances + distances.T) / 2

distances = generate_distances(num_cities)

print("Distance Matrix:")
print(distances)

A = 500
B = 500
C = 10

num_neurons = num_cities ** 2
weights = np.zeros((num_neurons, num_neurons))

def city_index(city, position):
    return city * num_cities + position

for i in range(num_cities):
    for j in range(num_cities):
        for k in range(num_cities):
            for l in range(num_cities):
                neuron_1 = city_index(i, j)
                neuron_2 = city_index(k, l)

                if i == k and j != l:
                    weights[neuron_1, neuron_2] -= A
                if j == l and i != k:
                    weights[neuron_1, neuron_2] -= A

                if j == l and k == (i + 1) % num_cities:
                    weights[neuron_1, neuron_2] -= C * distances[i, k]

state = np.zeros(num_neurons)
initial_cities = np.random.choice(num_cities, num_cities, replace=False)
for i in range(num_cities):
    state[city_index(initial_cities[i], i)] = 1

def hopfield_dynamics(state, weights, iterations=100):
    for _ in range(iterations):
        state_input = np.dot(weights, state)
        new_state = np.zeros_like(state)
        for i in range(num_cities):
            max_idx = np.argmax(state_input[i * num_cities:(i + 1) * num_cities])
            new_state[i * num_cities + max_idx] = 1
        state = new_state
    return state

final_state = hopfield_dynamics(state, weights)

final_state_matrix = final_state.reshape(num_cities, num_cities)

def extract_solution(state):
    state = state.reshape((num_cities, num_cities))
    solution = []
    for position in range(num_cities):
        city = np.argmax(state[:, position])
        solution.append(city)
    return solution

solution = extract_solution(final_state)

print("Extracted Solution (City indices in tour order):")
print(solution)

def calculate_total_distance(solution, distances):
    total_distance = 0
    for i in range(len(solution)):
        total_distance += distances[solution[i], solution[(i + 1) % len(solution)]]
    return total_distance

total_distance = calculate_total_distance(solution, distances)
print("Total Distance:", total_distance)
