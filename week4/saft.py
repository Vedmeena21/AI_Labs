# Import necessary libraries
import random
import math
import time

import copy
import matplotlib.pyplot as plt

# Define the tourist locations in Rajasthan
locations = [
    "Jaipur", "Udaipur", "Jodhpur", "Jaisalmer", "Pushkar",
    "Ajmer", "Bikaner", "Chittorgarh", "Mount Abu", "Ranthambore",
    "Bundi", "Kota", "Sawai Madhopur", "Neemrana", "Mandawa",
    "Sikar", "Alwar", "Osian", "Tanot", "Hindaun"
]

# Define the distance matrix (in kilometers) between these locations
distance_matrix = [
    [0, 395, 337, 558, 146, 135, 334, 300, 480, 180, 210, 242, 155, 122, 168, 114, 155, 362, 636, 158],
    [395, 0, 250, 490, 277, 289, 484, 117, 164, 388, 327, 269, 380, 521, 461, 451, 432, 276, 640, 470],
    [337, 250, 0, 284, 231, 217, 250, 222, 326, 460, 467, 430, 473, 451, 408, 398, 381, 68, 384, 424],
    [558, 490, 284, 0, 515, 482, 320, 485, 600, 625, 642, 605, 647, 540, 537, 527, 512, 330, 148, 627],
    [146, 277, 231, 515, 0, 15, 372, 420, 527, 241, 270, 301, 210, 260, 233, 223, 208, 199, 586, 217],
    [135, 289, 217, 482, 15, 0, 359, 408, 514, 229, 258, 289, 198, 247, 220, 210, 195, 185, 573, 205],
    [334, 484, 250, 320, 372, 359, 0, 499, 559, 508, 525, 488, 531, 295, 154, 258, 248, 318, 495, 522],
    [300, 117, 222, 485, 420, 408, 499, 0, 281, 474, 413, 355, 466, 540, 536, 526, 509, 195, 576, 543],
    [480, 164, 326, 600, 527, 514, 559, 281, 0, 606, 545, 487, 598, 670, 666, 656, 639, 299, 691, 673],
    [180, 388, 460, 625, 241, 229, 508, 474, 606, 0, 265, 275, 155, 155, 209, 199, 180, 471, 657, 183],
    [210, 327, 467, 642, 270, 258, 525, 413, 545, 265, 0, 40, 110, 245, 332, 250, 260, 459, 645, 104],
    [242, 269, 430, 605, 301, 289, 488, 355, 487, 275, 40, 0, 90, 217, 292, 202, 212, 421, 607, 85],
    [155, 380, 473, 647, 210, 198, 531, 466, 598, 155, 110, 90, 0, 175, 267, 180, 160, 452, 638, 85],
    [122, 521, 451, 540, 260, 247, 295, 540, 670, 155, 245, 217, 175, 0, 132, 122, 105, 410, 684, 150],
    [168, 461, 408, 537, 233, 220, 154, 536, 666, 209, 332, 292, 267, 132, 0, 101, 95, 370, 646, 285],
    [114, 451, 398, 527, 223, 210, 258, 526, 656, 199, 250, 202, 180, 122, 101, 0, 19, 360, 636, 176],
    [155, 432, 381, 512, 208, 195, 248, 509, 639, 180, 260, 212, 160, 105, 95, 19, 0, 341, 621, 158],
    [362, 276, 68, 330, 199, 185, 318, 195, 299, 471, 459, 421, 452, 410, 370, 360, 341, 0, 444, 444],
    [636, 640, 384, 148, 586, 573, 495, 576, 691, 657, 645, 607, 638, 684, 646, 636, 621, 444, 0, 700],
    [158, 470, 424, 627, 217, 205, 522, 543, 673, 183, 104, 85, 85, 150, 285, 176, 158, 444, 700, 0]
]

def get_cost(state):
    """Calculates the total distance for a given tour."""
    distance = 0
    for i in range(len(state)):
        from_city = state[i]
        to_city = state[(i + 1) % len(state)]  # Wrap around to the first city
        distance += distance_matrix[from_city][to_city]
    return distance

def annealing(initial_state):
    """Performs simulated annealing to find a near-optimal solution."""
    initial_temp = 5000
    alpha = 0.99
    current_temp = initial_temp
    solution = initial_state
    best_solution = solution
    best_cost = get_cost(solution)

    while current_temp > 1:
        # Generate a neighbor by swapping two cities
        neighbor = get_neighbor(solution)
        current_cost = get_cost(solution)
        neighbor_cost = get_cost(neighbor)

        # Check if we accept the new solution
        if neighbor_cost < current_cost or random.random() < math.exp((current_cost - neighbor_cost) / current_temp):
            solution = neighbor
            current_cost = neighbor_cost

        # Update the best solution found so far
        if current_cost < best_cost:
            best_solution = solution
            best_cost = current_cost

        # Cool down the temperature
        current_temp *= alpha

    return best_solution, best_cost

def get_neighbor(state):
    """Generates a neighbor by swapping two cities."""
    neighbor = state[:]
    i, j = random.sample(range(len(state)), 2)
    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
    return neighbor

if __name__ == "__main__":
    # Initialize the tour with a random shuffle of the cities
    initial_state = list(range(len(locations)))
    random.shuffle(initial_state)

    # Run simulated annealing
    start_time = time.time()
    best_solution, best_cost = annealing(initial_state)
    elapsed_time = time.time() - start_time

    # Print the best tour and its cost
    best_tour = " -> ".join([locations[i] for i in best_solution])
    print(f"Best Tour: {best_tour}")
    print(f"Total Distance: {best_cost} km")
    print(f"Time Elapsed: {elapsed_time:.2f} seconds")

    # Plot the best route
    xs = [i for i in range(len(locations))]
    ys = [distance_matrix[best_solution[i]][best_solution[(i + 1) % len(locations)]] for i in range(len(locations))]
    plt.plot(xs, ys, 'bo-')
    plt.xlabel('Location')
    plt.ylabel('Distance (km)')
    plt.title('Simulated Annealing - Best Route')
    plt.show()
