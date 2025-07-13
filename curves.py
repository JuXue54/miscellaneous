import matplotlib.pyplot as plt
import numpy as np
import math

def curve(x):
    """
    y^2 = x^3 - 7x + 10
    Parameters
    ----------
    x

    Returns
    -------
    y
    """
    y_2 = np.pow(x, 3) - 7 * x + 10
    y = np.pow(y_2, 0.5)
    return y, -y

def plot(func):
    x = np.linspace(-4, 4, 2000)
    v1,v2 = func(x)
    plt.plot(x, v1,x, v2)
    plt.show()





if __name__=='__main__':
    plot(curve)