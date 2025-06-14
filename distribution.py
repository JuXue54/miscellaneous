import numpy as np
from matplotlib import pyplot as plt


def gamma(z):
    n = 5000
    m = 500
    t = np.logspace(0, 10, num=n, base=10)
    x = np.linspace(0, z, m)
    y = np.zeros(m)
    for i in range(len(t)):
        if i > 0:
            delta = t[i] - t[i - 1]
        else:
            delta = t[i]
        y += t[i] ** (x - 1) * np.exp(-t[i]) * delta
    return x.flatten(), y


def factorial(n):
    f = 1
    for i in range(1, n + 1):
        f *= i
    return f


if __name__ == '__main__':
    x, y = gamma(20)
    x0 = list(range(20))
    y0 = list(map(factorial, x0))
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(x - 1, y, '-r', label='gamma')
    ax.plot(x0, y0, marker='x', label='factorial')
    ax.set_yscale('log')
    ax.legend()
    plt.show()
