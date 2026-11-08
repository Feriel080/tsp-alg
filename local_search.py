import random
import os
import numpy as np
import matplotlib.pyplot as plt
from colorama import Fore, Style
from helping_func import generate_villages, distance_matrix, longueur, realizable_solution

class LocalSearch: 
    def __init__(self, N, starting_village = None, villages = None, initial_route = None):
        self.n = N
        self.villages = villages if villages != None else generate_villages(self.n)
        self.M = distance_matrix(self.n, self.villages)
        if initial_route is not None:
            self.initial_route = initial_route
            self.starting_village = self.initial_route[0]
        else:
            self.starting_village = starting_village if starting_village is not None else random.randrange(0, self.n)
            villages_list = [i for i in range(self.n) if i != self.starting_village]
            random.shuffle(villages_list)
            self.initial_route = [self.starting_village] + villages_list + [self.starting_village]
            
        self.initial_distance = longueur(self.n, self.initial_route, self.M)
        self.best_route = self.initial_route
        self.best_distance = self.initial_distance
        self.accepted_swaps = 0
        self.gain = 0
        
    def voisins(self, T):
        neighbors = []
        for i in range(1, self.n - 1):
            for j in range(i + 1, self.n):
                neighbor = T.copy()
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                neighbors.append((longueur(self.n, neighbor, self.M), neighbor))
        return neighbors
    
    def run(self):
        route, distance = self.initial_route, self.initial_distance
        accepted_swaps = 0
        while True:
            best_distance, best_route = min(self.voisins(route), key=lambda x: x[0])
            if best_distance >= distance:
                break
            if realizable_solution(self.n, self.best_route):
                route, distance = best_route, best_distance
            accepted_swaps += 1
        self.best_route = route
        self.best_distance = distance
        self.accepted_swaps = accepted_swaps
        self.gain = ((self.initial_distance - self.best_distance) / self.initial_distance) * 100 if self.initial_distance > 0 else 0
        
    def draw_map(self):
        coords = np.array(self.villages)
        node_size = 900
        stop_arrow = np.sqrt(node_size) / 2 + 2

        fig, ax = plt.subplots(figsize=(9, 9))
        ax.grid(False)

        for i in range(self.n):
            u, v = self.best_route[i], self.best_route[i + 1]
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

        ax.set_title(f"Total distance = {self.best_distance:.2f} | Gain = {self.gain:.1f}% | Swaps = {self.accepted_swaps}")
        ax.set_aspect("equal")
        ax.set_xlabel("x")
        ax.set_ylabel("y")

        image_path = os.path.abspath(f"LocalSearch/Tournee_map_{self.starting_village}.png")
        fig.savefig(image_path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        print(f"{Fore.CYAN}Map saved at: {image_path}{Style.RESET_ALL}")