import random

class GreedyAlgorithm:
    def __init__(self, N):
        self.starting_village = random.randrange(0, N)
        self.T = [self.starting_village]
        
    def run(self, N, M):
        while len(self.T) < N + 1:
            