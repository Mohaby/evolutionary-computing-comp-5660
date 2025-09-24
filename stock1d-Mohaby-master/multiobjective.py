from math import inf
import math
import numpy as np


# TODO: Return True if A dominates B based on the objective member variables of both objects.
#       If attempting the YELLOW deliverable, your code must be able to gracefully handle
#       any number of objectives, i.e., don't hardcode an assumption that there are 2 objectives.
def dominates(A, B):
    # HINT: We strongly recommend use of the built-in functions any() and all()

    a_obj = A.objectives
    b_obj = B.objectives

    # A must be at least as good as B in all objectives
    not_worse_in_all = all(a >= b for a, b in zip(a_obj, b_obj))

    # A must be strictly better than B in at least one objective
    strictly_better_in_one = any(a > b for a, b in zip(a_obj, b_obj))

    return not_worse_in_all and strictly_better_in_one


# TODO: Use the dominates function (above) to sort the input population into levels
#       of non-domination, and assign to the level members based on an individual's level.
def nondomination_sort(population):
    for individual in population:
        individual.dominated_solutions = []
        individual.domination_count = 0

    # Compare each individual with every other individual
    for i, A in enumerate(population):
        for j, B in enumerate(population):
            if i == j:
                continue
            if dominates(A, B):
                A.dominated_solutions.append(B)
            elif dominates(B, A):
                A.domination_count += 1

    # Initialize levels
    current_front = [ind for ind in population if ind.domination_count == 0]
    for ind in current_front:
        ind.level = 1

    level = 1
    while current_front:
        next_front = []
        for ind in current_front:
            for dominated in ind.dominated_solutions:
                dominated.domination_count -= 1
                if dominated.domination_count == 0:
                    dominated.level = level + 1
                    next_front.append(dominated)
        level += 1
        current_front = next_front



# TODO: Calculate the crowding distance from https://ieeexplore.ieee.org/document/996017
#       For each individual in the population, and assign this value to the crowding member variable.
#       Use the inf constant (imported at the top of this file) to represent infinity where appropriate.
# IMPORTANT: Note that crowding should be calculated for each level of nondomination independently.
#            That is, only individuals within the same level should be compared against each other for crowding.
# stock_population_evaluation.py

def assign_crowding_distances(population):
    levels = {}
    for ind in population:
        if ind.level not in levels:
            levels[ind.level] = []
        levels[ind.level].append(ind)

    # calculate crowding distances independently
    for level_individuals in levels.values():
        num_individuals = len(level_individuals)

        # If there are only two individuals, assign them both infinite crowding distance
        if num_individuals <= 2:
            for ind in level_individuals:
                ind.crowding = inf
            continue

        # Initialize crowding distance to zero for all individuals in this level
        for ind in level_individuals:
            ind.crowding = 0.0

        # Number of objectives in the problem 
        num_objectives = len(level_individuals[0].objectives)

        # sort the individuals based on that objective
        for obj_index in range(num_objectives):
            level_individuals.sort(key=lambda x: x.objectives[obj_index])

            # Boundary individuals get infinite crowding distance
            level_individuals[0].crowding = inf
            level_individuals[-1].crowding = inf

            # Get the minimum and maximum values for this objective for normalization
            min_obj = level_individuals[0].objectives[obj_index]
            max_obj = level_individuals[-1].objectives[obj_index]

            # If all individuals have the same value for this objective, skip the rest of this loop
            if max_obj == min_obj:
                continue

            # Calculate crowding distance for individuals not on the boundary
            for i in range(1, num_individuals - 1):
                next_value = level_individuals[i + 1].objectives[obj_index]
                prev_value = level_individuals[i - 1].objectives[obj_index]

                # Increment crowding distance based on normalized difference in objective value
                level_individuals[i].crowding += (next_value - prev_value) / (max_obj - min_obj)



# This function is implemented for you. You should not modify it.
# It uses the above functions to assign fitnesses to the population.
def assign_fitnesses(population, crowding, failure_fitness, **kwargs):
    # Assign levels of nondomination.
    nondomination_sort(population)

    # Assign fitnesses.
    max_level = max(map(lambda x:x.level, population))
    for individual in population:
        individual.fitness = max_level + 1 - individual.level

    # Check if we should apply crowding penalties.
    if not crowding:
        for individual in population:
            individual.crowding = 0

    # Apply crowding penalties.
    else:
        assign_crowding_distances(population)
        for individual in population:
            if individual.crowding != inf:
                assert 0 <= individual.crowding <= len(individual.objectives),\
                    f'A crowding distance ({individual.crowding}) was not in the correct range. ' +\
                    'Make sure you are calculating them correctly in assign_crowding_distances.'
                individual.fitness -= 1 - 0.999 * (individual.crowding / len(individual.objectives))




# The remainder of this file is code used to calculate hypervolumes.
# You do not need to read, modify or understand anything below this point.
# Implementation based on https://ieeexplore.ieee.org/document/5766730


def calculate_hypervolume(front, reference_point=None):
    point_set = [individual.objectives for individual in front]
    if reference_point is None:
        # Defaults to (-1)^n, which assumes the minimal possible scores are 0.
        reference_point = [-1] * len(point_set[0])
    return wfg_hypervolume(list(point_set), reference_point, True)


def wfg_hypervolume(pl, reference_point, preprocess=False):
    if preprocess:
        pl_set = {tuple(p) for p in pl}
        pl = list(pl_set)
        if len(pl[0]) >= 4:
            pl.sort(key=lambda x: x[0])

    if len(pl) == 0:
        return 0
    return sum([wfg_exclusive_hypervolume(pl, k, reference_point) for k in range(len(pl))])


def wfg_exclusive_hypervolume(pl, k, reference_point):
    return wfg_inclusive_hypervolume(pl[k], reference_point) - wfg_hypervolume(limit_set(pl, k), reference_point)


def wfg_inclusive_hypervolume(p, reference_point):
    return math.prod([abs(p[j] - reference_point[j]) for j in range(len(p))])


def limit_set(pl, k):
    ql = []
    for i in range(1, len(pl) - k):
        ql.append([min(pl[k][j], pl[k+i][j]) for j in range(len(pl[0]))])
    result = set()
    for i in range(len(ql)):
        interior = False
        for j in range(len(ql)):
            if i != j:
                if all(ql[j][d] >= ql[i][d] for d in range(len(ql[i]))) and any(ql[j][d] > ql[i][d] for d in range(len(ql[i]))):
                    interior = True
                    break
        if not interior:
            result.add(tuple(ql[i]))
    return list(result)
