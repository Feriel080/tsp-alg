import random
import time
import os
import csv
from greedy_alg import GreedyAlgorithm
from local_search import LocalSearch
from helping_func import generate_villages
# from colorama import Fore, Style

random.seed(42)

def save_row(path, row):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    new = not os.path.exists(path)
    with open(path, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(row))
        if new:
            w.writeheader()
        w.writerow(row)
        
N = [10, 20, 50, 100]

for n in N:
    villages = generate_villages(n)
    starting_village = 0

    Gr_A = GreedyAlgorithm(n, start_village=starting_village, villages=villages)
    t0_gr = time.perf_counter()
    Gr_A.run()
    t_gr = time.perf_counter() - t0_gr
    
    init_route, initial_distance = Gr_A.T, Gr_A.total_distance
    Local_S = LocalSearch(n, starting_village=starting_village, villages=villages, initial_route=init_route)
    t0_ls = time.perf_counter()
    Local_S.run()
    t_ls = time.perf_counter() - t0_ls
    final_route, best_distance, accepted_swaps = Local_S.best_route, Local_S.best_distance, Local_S.accepted_swaps
    gain = Local_S.gain
    save_row(f"results/results.csv", dict(Nbr_ville=n, Longueur_glouton=initial_distance, t_glouton=round(t_gr, 6),
                                         Longueur_LS=best_distance, t_LS=round(t_ls, 6), Gain=gain))
        

# print(f"{Fore.GREEN}Initial Route: {Style.RESET_ALL}{init_route}")
# print(f"{Fore.GREEN}Total Distance: {Style.RESET_ALL}{Gr_A.total_distance}")
# print(f"{Fore.GREEN}Final Route: {Style.RESET_ALL}{final_route}")
# print(f"{Fore.GREEN}Best Distance: {Style.RESET_ALL}{best_distance}")
# print(f"{Fore.GREEN}Accepted Swaps: {Style.RESET_ALL}{accepted_swaps}")
# print(f"{Fore.GREEN}Gain: {Style.RESET_ALL}{gain}")