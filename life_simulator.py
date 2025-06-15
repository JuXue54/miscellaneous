# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation


def rand_one(matrix, num):
    m, n = len(matrix), len(matrix[0])
    rd = np.random.randint(0, m * n, size=num)
    for x in rd:
        matrix[x // n, x % n] = 1


def neighbors(board, i, j):
    m, n = len(board), len(board[0])
    count = 0
    if i > 0:
        count += board[i - 1][j]
        if j > 0:
            count += board[i - 1][j - 1]
        if j < n - 1:
            count += board[i - 1][j + 1]
    if i < m - 1:
        count += board[i + 1][j]
        if j > 0:
            count += board[i + 1][j - 1]
        if j < n - 1:
            count += board[i + 1][j + 1]
    if j > 0:
        count += board[i][j - 1]
    if j < n - 1:
        count += board[i][j + 1]
    if board[i][j] == 1:
        if count < 2 or count > 3:
            return 0
        else:
            return 1
    else:
        if count != 3:
            return 0
        else:
            return 1


def life(board, copy):
    m, n = len(board), len(board[0])
    for i in range(m):
        for j in range(n):
            copy[i][j] = neighbors(board, i, j)

class LifeBox:

    def __init__(self, width, height):
        self.matrix = np.zeros([height, width], dtype='int')
        self.copy = np.zeros([height, width], dtype='int')
        rand_one(self.matrix, 7000)

    def step(self):
        life(self.matrix, self.copy)
        self.matrix, self.copy = self.copy, self.matrix
        return self.matrix



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    width = 300
    height = 300
    box = LifeBox(width, height)

    fig = plt.figure()
    img = plt.imshow(box.matrix, animated=True, cmap=plt.get_cmap("viridis"), aspect="equal")


    def animate(*args):
        img.set_array(box.step())
        return (img,)

    ani = animation.FuncAnimation(fig, animate, interval=60, blit=True,cache_frame_data=False)
    plt.show()

    # while True:
    #     life(matrix, matrix_1)
    #     matrix, matrix_1 = matrix_1, matrix
    #     img.set_data(matrix)
    #     fig.canvas.draw()
    #     plt.pause(0.01)


# plt.show()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
