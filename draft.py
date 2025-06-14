import torch as t
import torch.optim as optim
from matplotlib import pyplot as plt
from torch import nn
from torch.autograd import Variable as V


def normalize(x):
    maxinum, _ = t.max(x, dim=0)
    mininum, _ = t.min(x, dim=0)
    return (x - mininum) / (maxinum - mininum), mininum, maxinum - mininum


def main():
    x = t.Tensor([[27, 30, 15, 26,
                   27, 20, 16, 18,
                   19, 20],
                  [5000, 7000, 5102,
                   8019, 1200, 7210,
                   6200, 9214, 4012,
                   3102],
                  [110, 120, 110,
                   80, 90, 119,
                   116, 100, 90,
                   76]]).t_()
    y = t.Tensor([[92, 84, 87, 82,
                   98, 94, 75, 80,
                   83, 89]]).t_()
    layer = nn.Linear(3, 1)
    optimizer = optim.Adagrad(layer.parameters(), lr=0.1)
    norm_x, mini_x, q_x = normalize(x)
    norm_y, mini_y, q_y = normalize(y)
    input = V(norm_x)
    target = V(norm_y)
    criterion = nn.MSELoss()
    loss_trend = []
    for i in range(1000):
        output = layer(input)
        loss = criterion(output, target)
        loss_trend.append(loss.detach().numpy())
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    # print(loss)
    result = {}
    for name, parameter in layer.named_parameters():
        if 'weight' in name:
            result[name] = parameter * q_y / q_x
        else:
            result[name] = parameter * q_y + mini_y - t.sum(result['weight'] * mini_x, dim=1)
    print(result)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.set_title('learn rate', color='r')
    ax.plot(loss_trend, label='Adagrad')
    ax.legend()
    plt.show()


if __name__ == "__main__":
    main()
