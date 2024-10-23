import numpy as np
import matplotlib.pyplot as plt

def bandit(action):
    return np.random.normal(0, 0.01)

steps = 10000
total_value = np.zeros((steps, 3))
rewards = np.zeros((steps, 2, 3))
cnt_actions = np.zeros((10, 3))

epsilons = [0.01, 0.1, 0.3]

for i, e in enumerate(epsilons):
    step = 1
    while step <= steps:
        if np.random.rand() < e or step == 1:
            action = np.random.randint(0, 10)
            value = bandit(action)
            total_value[step - 1, i] = value
            if step > 1:
                total_value[step - 1, i] += total_value[step - 2, i]
            rewards[step - 1, :, i] = [value, action]
        else:
            actions = np.zeros((10, 2))
            for s in range(step - 1):
                actions[int(rewards[s, 1, i]), 0] += rewards[s, 0, i]
                actions[int(rewards[s, 1, i]), 1] += 1
            
            exp_return = -np.inf
            for a in range(10):
                if actions[a, 1] > 0:
                    temp = actions[a, 0] / actions[a, 1]
                    if temp > exp_return:
                        exp_return = temp
                        action = a
            
            value = bandit(action)
            total_value[step - 1, i] = value + total_value[step - 2, i]
            rewards[step - 1, :, i] = [value, action]
            cnt_actions[:, i] = actions[:, 1]

        step += 1

avg_reward = np.zeros(steps)
for i in range(steps):
    avg_reward[i] = total_value[i, 1] / (i + 1)

plt.figure(1)
plt.plot(avg_reward)
plt.xlabel('Time Steps')
plt.ylabel('Average Reward')
plt.title('10 armed Bandit - (epsilon = 0.1)')
plt.show()
