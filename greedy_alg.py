import random
import os
import numpy as np
import matplotlib.pyplot as plt
from colorama import Fore, Style
from helping_func import longueur, generate_villages, distance_matrix, realizable_solution

random.seed(42)


class GreedyAlgorithm:  # applicable only for this problem
    def __init__(self, N, start_village=None, villages=None):
        self.n = N
        self.villages = villages if villages is not None else generate_villages(self.n)
        self.M = distance_matrix(self.n, self.villages)
        self.starting_village = start_village if start_village != None else random.randrange(
            0, self.n)
        self.T = [self.starting_village]
        self.total_distance = 0

    def run(self):
        while len(self.T) < self.n:
            sorted_villages = np.argsort(self.M[self.T[-1]])
            for j in range(self.n):
                close_village = sorted_villages[j]
                if close_village not in self.T:
                    print(
                        f"{Fore.MAGENTA} The close village to {Fore.GREEN}{self.T[-1]}{Style.RESET_ALL} is {Fore.GREEN}{close_village}{Style.RESET_ALL}")
                    self.T.append(int(close_village))
                    print(
                        f"{Fore.MAGENTA}Adding it to the route:{Style.RESET_ALL} {Fore.GREEN}{self.T}{Style.RESET_ALL}")
                    break

        # to make sure the last village is the first visited village
        self.T.append(self.starting_village)
        if realizable_solution(self.n, self.T):
            self.total_distance = longueur(self.n, self.T, self.M)
            print(f"{Fore.CYAN}This solution respects the constraints. Total distance is: {self.total_distance}{Style.RESET_ALL}")
        else:
            print(
                f"{Fore.RED}This solution does not respect the constraints. Run the algorithm again.{Style.RESET_ALL}")

    def draw_map(self):
        coords = np.array(self.villages)
        node_size = 900
        stop_arrow = np.sqrt(node_size) / 2 + 2

        fig, ax = plt.subplots(figsize=(9, 9))
        ax.grid(False)

        for i in range(self.n):
            u, v = self.T[i], self.T[i + 1]
            ax.annotate(
                "",
                xy=coords[v], xytext=coords[u],
                arrowprops=dict(arrowstyle="-|>", color="orange", lw=1.8,
                                shrinkA=stop_arrow, shrinkB=stop_arrow,
                                mutation_scale=18),
            )
            mid = (coords[u] + coords[v]) / 2
            ax.text(mid[0], mid[1], f"{self.M[u, v]:.2f}",
                    ha="center", va="center", fontsize=8, zorder=5,
                    bbox=dict(boxstyle="round,pad=0.15", fc="white",
                              ec="none", alpha=0.85))

        colors = ["lightgreen" if k == self.starting_village else "lightblue"
                  for k in range(self.n)]
        ax.scatter(coords[:, 0], coords[:, 1], s=node_size, c=colors,
                   edgecolors="black", zorder=3)

        for k, (x, y) in enumerate(coords):
            ax.text(x, y, str(k), ha="center", va="center",
                    fontsize=10, zorder=4)

        ax.set_title(f"Total distance = {round(self.total_distance, 2)}")
        ax.set_aspect("equal")
        ax.set_xlabel("x")
        ax.set_ylabel("y")

        image_path = os.path.abspath(f"Greedy/Tournee_map_{self.starting_village}.png")
        fig.savefig(image_path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        print(f"{Fore.CYAN}Map saved at: {image_path}{Style.RESET_ALL}")
