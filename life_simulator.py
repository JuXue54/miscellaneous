# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


import matplotlib.pyplot as plt
import numpy as np


def rand_one(matrix, num):
    m, n = len(matrix), len(matrix[0])
    rd = np.random.randint(0, m * n, size=num)
    for x in rd:
        matrix[x // n, x % n] = 1


def neighbors(board, i, j):
    m, n = len(board), len(board[0])
    count = 0
    if i > 0:
        count += (board[i - 1][j] & 1)
        if j > 0:
            count += (board[i - 1][j - 1] & 1)
        if j < n - 1:
            count += (board[i - 1][j + 1] & 1)
    if i < m - 1:
        count += (board[i + 1][j] & 1)
        if j > 0:
            count += (board[i + 1][j - 1] & 1)
        if j < n - 1:
            count += (board[i + 1][j + 1] & 1)
    if j > 0:
        count += (board[i][j - 1] & 1)
    if j < n - 1:
        count += (board[i][j + 1] & 1)
    if board[i][j] == 1:
        if count < 2 or count > 3:
            return 3
        else:
            return 1
    else:
        if count != 3:
            return 0
        else:
            return 2


def life(board):
    m, n = len(board), len(board[0])
    for i in range(m):
        for j in range(n):
            board[i][j] = neighbors(board, i, j)
    for i in range(m):
        for j in range(n):
            if board[i][j] > 1:
                board[i][j] ^= 3


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    width = 200
    height = 200
    matrix = np.zeros([height, width], dtype='int')
    rand_one(matrix, 7000)

    fig = plt.figure()
    img = plt.imshow(matrix)

    while True:
        life(matrix)
        img.set_data(matrix)
        fig.canvas.draw()
        plt.pause(0.01)

# plt.show()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
