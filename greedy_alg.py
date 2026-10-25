import random
import os
import pygraphviz as pgv
import numpy as np
from colorama import Fore, Style
from helping_func import longueur, generate_villages, distance_matrix, realizable_solution


class GreedyAlgorithm:  # applicable only for this problem
    def __init__(self, N, start_village=None):
        self.n = N
        self.villages = generate_villages(self.n)
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

    def draw_graph(self):
        edges = [(self.T[i], self.T[j])
                 for i, j in zip(range(self.n), range(1, self.n + 1))]
        
        G = pgv.AGraph(directed=True, rankdir="LR")
        G.add_nodes_from(self.T)
        
        for u, v in edges:
            distance = self.M[u, v]
            G.add_edge(u, v, label=str(round(distance, 2)))

        G.graph_attr["label"] = f"Total distance = {self.total_distance}"
        G.node_attr["shape"] = "circle"
        G.edge_attr["color"] = "orange"

        G.layout("dot")
        image_path = os.path.abspath("Tournee.png")
        G.draw(image_path)
        print(f"{Fore.CYAN}Graph saved at: {image_path}{Style.RESET_ALL}")
