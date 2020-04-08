import random
from tkinter import *
master = Tk()

cell_score_min = -0.2
cell_score_max = 0.2

# Game setup
walk_reward = -0.04     # Penalty for each step you make
(x, y) = (6, 5)     # World dimension, x axis and y axis
start_pos = (0, y - 1)     # Initial position starts at the bottom left corner
goals = [(x - 1, 1, "red", -1), (x - 1, 0, "green", 1)]     # Goal states' coordinates
# Randomly generated obstacles' coordinates
obstacles = []
for numberO in range(random.randint(int(x * y / 8), int(x * y / 2))):
    generated_pos = (random.randint(0, x), random.randint(0, y))
    restricted_pos = [(0, y - 1), (x - 1, 1), (x - 1, 0)]
    if generated_pos not in obstacles and generated_pos not in restricted_pos:
        obstacles.append(generated_pos)

Width = 100
board = Canvas(master, width=x * Width, height=y * Width)
score = 1
restart = False
cell_scores = {}
actions = ["up", "right", "down", "left"]
player = start_pos


# Render the world: grids, obstacles and goals
def render_grid():
    global goals, obstacles, Width, x, y, player

    for i in range(x):
        for j in range(y):
            board.create_rectangle(i * Width, j * Width, (i + 1) * Width, (j + 1) * Width, fill="white", width=1)
            cell_scores[(i, j)] = {}

    for (i, j, c, w) in goals:
        board.create_rectangle(i * Width, j * Width, (i + 1) * Width, (j + 1) * Width, fill=c, width=1)

    for (i, j) in obstacles:
        board.create_rectangle(i * Width, j * Width, (i + 1) * Width, (j + 1) * Width, fill="black", width=1)


render_grid()


def set_cell_score(state, action, val):
    global cell_score_min, cell_score_max


def try_move(dx, dy):
    global player, x, y, score, walk_reward, me, restart

    if restart:
        restart_game()

    new_x = player[0] + dx
    new_y = player[1] + dy
    score += walk_reward

    if (new_x >= 0) and (new_x < x) and (new_y >= 0) and (new_y < y) and not ((new_x, new_y) in obstacles):
        board.coords(me, new_x * Width + Width * 2 / 10,
                     new_y * Width + Width * 2 / 10,
                     new_x * Width + Width * 8 / 10,
                     new_y * Width + Width * 8 / 10)
        player = (new_x, new_y)

    for (i, j, c, w) in goals:
        if new_x == i and new_y == j:
            score -= walk_reward
            score += w
            if score > 0:
                print("Success! score: ", score)
            else:
                print("Fail! score: ", score)
            restart = True
            return


def call_up(event):
    try_move(0, -1)


def call_down(event):
    try_move(0, 1)


def call_left(event):
    try_move(-1, 0)


def call_right(event):
    try_move(1, 0)


# Action Declaration won't affect the training process
master.bind("<Up>", call_up)
master.bind("<Down>", call_down)
master.bind("<Right>", call_right)
master.bind("<Left>", call_left)


def restart_game():
    global player, score, me, restart
    player = start_pos
    score = 1
    restart = False
    board.coords(me,
                 player[0] * Width + Width * 2 / 10,
                 player[1] * Width + Width * 2 / 10,
                 player[0] * Width + Width * 8 / 10,
                 player[1] * Width + Width * 8 / 10)


def has_restarted():
    return restart


me = board.create_rectangle(player[0] * Width + Width * 2 / 10,
                            player[1] * Width + Width * 2 / 10,
                            player[0] * Width + Width * 8 / 10,
                            player[1] * Width + Width * 8 / 10,
                            fill="orange", width=1, tag="me")

board.grid(row=0, column=0)


def start_game():
    master.mainloop()
