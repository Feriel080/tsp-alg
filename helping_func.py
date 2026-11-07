import random
import math
import numpy as np

random.seed(42)


def generate_villages(N):
    return [(random.randint(0, 100), random.randint(0, 100)) for _ in range(N)]


def distance(ville1, ville2):
    return math.sqrt(math.pow(ville1[0] - ville2[0], 2) + math.pow(ville1[1] - ville2[1], 2))


def distance_matrix(N, villes):
    """Distance Matrix

    Args:
        N (int): Number of vilalges
        villes (List[tuple]): Liste des coordonnées des ville 
            ex: [(3, 5), (2, 6), (10, 60)...]

    Returns:
        M: Distances matrix 
    """
    M = np.zeros((N, N))

    for i in range(N):
        for j in range(N):
            M[i, j] = distance(villes[i], villes[j])

    return M


def longueur(N, T, M):
    """Route Distance

    Args:
        T (list[int]): contains the route indices
            ex: [5, 2, 3...]
        M (numpy.ndarray): the distance matrix, where M[i, j] is the
            distance between villages i and j.

    Returns:
        total_distance: total distance between the villages of T
    """
    total_distance = 0

    for i, j in zip(range(N - 1), range(1, N)):
        total_distance += M[T[i], T[j]]

    return total_distance


def realizable_solution(N, T):
    """Testing if the provided solution was realizable (meets the constraints)

    Args:
        N (int): Number of villages
        T (list[int]): Turn of villages

    Returns:
        boolean: `True` if the solution meets the contraints, `False` if not.
    """
    solution = set(T)

    # Check if the first visited village is the last village
    if T[0] != T[N]:
        return False

    # Check if the solution contains all villages, and all are unique
    if len(solution) != N:
        return False

    return True
