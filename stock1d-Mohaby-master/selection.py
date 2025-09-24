
# selection.py

import random

# For all the functions here, it's strongly recommended to
# review the documentation for Python's random module:
# https://docs.python.org/3/library/random.html

# Parent selection functions---------------------------------------------------
def uniform_random_selection(population, n, **kwargs):
    # TODO: select n individuals uniform randomly
        return random.choices(population, k=n)


def k_tournament_with_replacement(population, n, k, **kwargs):
    # TODO: perform n k-tournaments with replacement to select n individuals
    parents = []
    for _ in range(n):
        tournament = random.sample(population, k)
        winner = max(tournament, key=lambda individual: individual.fitness)
        parents.append(winner)
    return parents



def fitness_proportionate_selection(population, n, **kwargs):
    # TODO: select n individuals using fitness proportionate selection
    fitnesses = [individual.fitness for individual in population]
    min_fitness = min(fitnesses)

    if min_fitness < 0:
        adjusted_fitnesses = [fitness - min_fitness for fitness in fitnesses]
    else:
        adjusted_fitnesses = fitnesses
    total_fitness = sum(adjusted_fitnesses)
    
    if total_fitness == 0:
        return random.choices(population, k=n)
    probabilities = [fitness / total_fitness for fitness in adjusted_fitnesses]
    return random.choices(population, weights=probabilities, k=n)




# Survival selection functions-------------------------------------------------
def truncation(population, n, **kwargs):
    # TODO: perform truncation selection to select n individuals
    sorted_population = sorted(population, key=lambda individual: individual.fitness, reverse=True)
    return sorted_population[:n]


def k_tournament_without_replacement(population, n, k, **kwargs):
    # TODO: perform n k-tournaments without replacement to select n individuals
    # Note: an individual should never be cloned from surviving twice!
    # Also note: be careful if using list.remove(), list.pop(), etc.
    # since this can be EXTREMELY slow on large populations if not handled properly
    # A better alternative to my_list.pop(i) is the following:
    # my_list[i] = my_list[-1]
    # my_list.pop()
    selected = []
    population_copy = population[:] 
    for _ in range(n):
        tournament = random.sample(population_copy, k)
        winner = max(tournament, key=lambda individual: individual.fitness)
        selected.append(winner)
        population_copy.remove(winner)
    return selected



# Yellow deliverable parent selection function---------------------------------
def stochastic_universal_sampling(population, n, **kwargs):
    # Recall that yellow deliverables are required for students in the grad
    # section but bonus for those in the undergrad section.
    # TODO: select n individuals using stochastic universal sampling

    fitnesses = [individual.fitness for individual in population]
    min_fitness = min(fitnesses)

    if min_fitness < 0:
        adjusted_fitnesses = [fitness - min_fitness for fitness in fitnesses]
    else:
        adjusted_fitnesses = fitnesses

    total_fitness = sum(adjusted_fitnesses)

    if total_fitness == 0:
        return random.choices(population, k=n)

    cumulative_sum = [sum(adjusted_fitnesses[:i+1]) for i in range(len(adjusted_fitnesses))]
    step_size = total_fitness / n
    start_point = random.uniform(0, step_size)
    points = [start_point + i * step_size for i in range(n)]


    selected = []
    current_point = 0
    for point in points:
        while point > cumulative_sum[current_point]:
            current_point += 1
        selected.append(population[current_point])
    
    return selected

