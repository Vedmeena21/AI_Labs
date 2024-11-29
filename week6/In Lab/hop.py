import numpy as np
import matplotlib.pyplot as plt

class HopfieldNetwork:
    def __init__(self, size=10):
        self.size = size
        self.weights = np.zeros((size*size, size*size))
        
    def train(self, patterns):
        num_patterns = len(patterns)
        flattened_patterns = [p.flatten() for p in patterns]
        
        for pattern in flattened_patterns:
            self.weights += np.outer(pattern, pattern)
        
        self.weights /= self.size * self.size
        
        np.fill_diagonal(self.weights, 0)
        
        return num_patterns
    
    def energy(self, state):
        """
        Compute network energy
        
        E = -0.5 * Σ(w_ij * x_i * x_j)
        """
        return -0.5 * np.dot(state, np.dot(self.weights, state))
    
    def recall(self, pattern, max_iter=100):
        
        state = pattern.flatten()
        prev_state = state.copy()
        
        for _ in range(max_iter):
            # Randomly update neurons
            update_order = np.random.permutation(self.size * self.size)
            
            for idx in update_order:
                local_field = np.dot(self.weights[idx], state)
                
                # Update neuron
                state[idx] = 1 if local_field > 0 else -1
            
            if np.array_equal(state, prev_state):
                break
            
            prev_state = state.copy()
        
        return state.reshape((self.size, self.size))
    
    def capacity_analysis(self, max_patterns=50):
        
        results = {}
        
        for num_patterns in range(1, max_patterns + 1):
            # Generate random binary patterns
            patterns = [np.random.choice([-1, 1], size=(self.size, self.size)) 
                        for _ in range(num_patterns)]

            self.train(patterns)
        
            retrieval_success = 0
            for pattern in patterns:
                recalled = self.recall(pattern)
                if np.array_equal(recalled, pattern):
                    retrieval_success += 1
            
            results[num_patterns] = retrieval_success / num_patterns
        
        return results

np.random.seed(42)
network = HopfieldNetwork(size=10)
capacity_results = network.capacity_analysis()

plt.figure(figsize=(10, 6))
plt.plot(list(capacity_results.keys()), list(capacity_results.values()), marker='o')
plt.title('Hopfield Network Capacity Analysis')
plt.xlabel('Number of Stored Patterns')
plt.ylabel('Retrieval Success Rate')
plt.grid(True)
plt.show()