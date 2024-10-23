import numpy as np
import matplotlib.pyplot as plt

# Function to simulate bandit action
def bandit(action):
    # Normally distributed rewards with mean = 0 and std dev = 0.01
    return np.random.normal(0, 0.01)

# Parameters
steps = 10000
total_value = np.zeros((steps, 3))
rewards = np.zeros((steps, 2, 3))
cnt_actions = np.zeros((10, 3))

epsilons = [0.01, 0.1, 0.3]

for i, e in enumerate(epsilons):
    step = 1
    while step <= steps:
        # Exploration
        if np.random.rand() < e or step == 1:
            action = np.random.randint(0, 10)  # Random action between 0 and 9
            value = bandit(action)
            total_value[step - 1, i] = value
            if step > 1:
                total_value[step - 1, i] += total_value[step - 2, i]
            rewards[step - 1, :, i] = [value, action]

        # Exploitation
        else:
            actions = np.zeros((10, 2))  # For storing total rewards and counts of actions
            for s in range(step - 1):
                actions[int(rewards[s, 1, i]), 0] += rewards[s, 0, i]  # Sum of rewards
                actions[int(rewards[s, 1, i]), 1] += 1  # Count of actions taken

            # Find action with maximum expected return
            exp_return = -np.inf
            for a in range(10):
                if actions[a, 1] > 0:  # To avoid division by zero
                    temp = actions[a, 0] / actions[a, 1]
                    if temp > exp_return:
                        exp_return = temp
                        action = a

            value = bandit(action)
            total_value[step - 1, i] = value + total_value[step - 2, i]
            rewards[step - 1, :, i] = [value, action]
            cnt_actions[:, i] = actions[:, 1]

        step += 1

# Calculate average rewards
avg_reward = np.zeros(steps)
for i in range(steps):
    avg_reward[i] = total_value[i, 1] / (i + 1)

# Plotting average reward over time for epsilon = 0.1
plt.figure(1)
plt.plot(avg_reward)
plt.xlabel('Time Steps')
plt.ylabel('Average Reward')
plt.title('10 armed Bandit - (epsilon = 0.1)')
plt.show()

