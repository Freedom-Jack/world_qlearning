import random

import numpy as np
import world
import threading
import time
import pprint
import matplotlib.pyplot as plt

# Global variables
actions = world.actions
states = []
q_function = {}

# Parameters
discount_rate = 0.5
alpha = 1
randomly_move_rate = 0.1

# Basic setup for the Q function
# Number of states is same as the grids in the world
for i in range(world.x):
    for j in range(world.y):
        states.append((i, j))

# Initial reward for all grids, all actions is default to 0.1
for state in states:
    temp = {}
    for action in actions:
        temp[action] = 0.1
        world.set_cell_score(state, action, temp[action])

    q_function[state] = temp

# Initialize the reward for the goal states
for (i, j, c, w) in world.goals:
    for action in actions:
        q_function[(i, j)][action] = w
        world.set_cell_score((i, j), action, w)


# Perform one of the actions{up, down, left, right}, and return the new position and reward
# i.e. {s, a, s', R(s, a, s')}
def do_action(act):
    # State before
    s = world.player
    r = -world.score

    # Down
    if act == actions[0]:
        world.try_move(0, -1)
    # Right
    elif act == actions[1]:
        world.try_move(1, 0)
    # Up
    elif act == actions[2]:
        world.try_move(0, 1)
    # Left
    elif act == actions[3]:
        world.try_move(-1, 0)
    else:
        return

    # State after and reward
    s2 = world.player
    r += world.score

    return s, act, r, s2


# Find the max Q value and the associated action of a given state
def best_q(s):
    val = None
    act = None

    for a, q in q_function[s].items():
        if val is None or (q > val):
            val = q
            act = a

    return act, val


# Update the q value
def update_q(s, a, alp, reward):
    # Formula:
    # Q(s, a) = Q(s, a) + α[R(s) + maxQ(s, a0) − Q(s, a)]
    #         = (1 - α)Q(s, a) + α[R(s) + maxQ(s, a0)]
    q_function[s][a] *= 1 - alp
    q_function[s][a] += alp * reward

    world.set_cell_score(s, a, q_function[s][a])


def run():
    global discount_rate, alpha
    time.sleep(1)
    t = 1

    while True:
        # Pick the right action
        s = world.player
        max_act, max_val = best_q(s)
        if random.random() < randomly_move_rate:
            (s, a, r, s2) = do_action(random.choice(actions))
        else:
            (s, a, r, s2) = do_action(max_act)

        # Update Q
        max_act, max_val = best_q(s2)
        update_q(s, a, alpha, r + discount_rate * max_val)

        # Check if the game has restarted
        t += 1.0
        if world.has_restarted():
            world.restart_game()
            time.sleep(0.01)
            t = 1.0

        # Update the learning rate
        alpha = pow(t, -0.1)

        # Modify the refresh rate of the game
        time.sleep(0.05)


t = threading.Thread(target=run)
t.daemon = True

t.start()
world.start_game()

# Print the learned Q function
pprint.pprint(q_function)

# Visualization of the Q function
x, y = np.meshgrid(np.arange(0, world.x, 1), np.arange(0, world.y, 1))
u, v = np.meshgrid(np.ones((world.x,)), np.ones((world.y,)))
for pos in q_function.keys():
    h_value = q_function[pos]['right'] - q_function[pos]['left']
    v_value = q_function[pos]['up'] - q_function[pos]['down']

    temp1 = world.y - pos[1] - 1

    u[temp1][pos[0]] = h_value
    v[temp1][pos[0]] = v_value

# Normalize the quiver
u = u / np.sqrt(u**2 + v**2)
v = v / np.sqrt(u**2 + v**2)

fig, ax = plt.subplots()
ax.quiver(x, y, u, v, units="xy")

plt.axis('equal')
plt.xticks(range(0, world.x + 3))
plt.yticks(range(0, world.y + 3))
plt.grid()
plt.show()
