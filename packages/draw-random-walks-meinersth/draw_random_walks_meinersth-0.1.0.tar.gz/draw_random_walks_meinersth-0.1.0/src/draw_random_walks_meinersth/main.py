import sys
import argparse

import numpy as np
import random as rd
import matplotlib.pyplot as plt


RANDOM_WALKERS = 2


def parse_args(args):
    parser = argparse.ArgumentParser(
        description="A program to draw custom random walks"
    )
    
    parser.add_argument("--walkers", nargs="?", type=int, default=RANDOM_WALKERS)
    parser.add_argument("--size", nargs="?", type=int, default=2000)
    parser.add_argument("--loc", nargs="?", type=int, default=0)
    parser.add_argument("--scale", nargs="?", type=int, default=10)
    parser.add_argument("--uniform", action="store_true")

    return parser.parse_args(args)


def run(
    walkers: int = RANDOM_WALKERS,
    mu: float = 0.,
    sigma: float = 0.1,
    size: int = 2000
):
    """
    create image of random walks
    """
    parser = parse_args(sys.argv[1:])

    if parser.walkers:
        walkers = parser.walkers

    if parser.size:
        size = parser.size

    if parser.loc:
        mu = parser.loc

    if parser.scale:
        sigma = 1./parser.scale

    while walkers > 0:
        # create probability distribution for walker
        distribution = np.random.normal(mu, sigma, size)

        if parser.uniform:
            distribution = np.random.uniform(-100, 100, size)

        # draw single walkers
        draw(distribution, size)

        # next walker
        walkers -= 1

    # save figure
    plt.savefig("walks.png")


def draw(distribution, size: int):
    """
    draw random walker
    """
    # data
    x = range(size)
    y = [sum(distribution[:k]) for k in range(size)]

    # colors
    colors = [
        "#0D1F2D",
        "#546A7B",
        "#9EA3B0",
        "#FAE1DF",
        "#E4C3AD"
    ]

    # graph
    plt.axes().set(facecolor="xkcd:light blue")
    plt.plot(x, y, color=rd.choice(colors))
    y_abs = [abs(value) for value in y]
    y_limit = max(size/200, max(y_abs) + max(y_abs)/10)
    plt.ylim(-y_limit, y_limit)
    plt.xlim(0, size)
    plt.axis("off")


if __name__ == "__main__":
    run()
