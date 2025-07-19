import matplotlib.pyplot as plt
import numpy as np


def curve(x, a, b):
    """
    y^2 = x^3 + ax + b
    Parameters
    ----------
    x

    Returns
    -------
    y
    """
    y_2 = np.power(x, 3) + a * x + b
    y = np.power(y_2, 0.5)
    return y, -y


def plot(func, a, b):
    x = np.linspace(-2, 4, 2000)
    v1, v2 = func(x, a, b)
    mask = ~np.isnan(v1)
    v1 = v1[mask]
    v2 = v2[mask]
    x = x[mask]
    # plt.plot(x, v1, 'r', x, v2, 'r')

    points = np.append(np.flip(v1), v2)
    x2 = np.append(np.flip(x), x)
    print(points)
    plt.plot(x2, points)
    plt.show()


if __name__ == '__main__':
    plot(curve, 0, 7)
