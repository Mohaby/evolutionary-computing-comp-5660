
# gpac_population_evaluation.py

from fitness import *


# 2b TODO: Evaluate the population and assign base_fitness, fitness, and log
#          member variables as described in the Assignment 2b notebook.
def base_population_evaluation(population, parsimony_coefficient, experiment, **kwargs):
    if experiment.casefold() == 'green':
        # Evaluate a population of Pac-Man controllers against the default ghost agent.
        # Sample call: score, log = play_GPac(controller, **kwargs)
        for individual in population:
            score, log = play_GPac(individual.genes, **kwargs)      
            # Calculate tree size
            size = individual.genes.count_nodes(individual.genes.root)
            
            individual.base_fitness = score
            individual.fitness = score - size * parsimony_coefficient
            individual.log = log


    elif experiment.casefold() == 'yellow':
        # YELLOW: Evaluate a population of Pac-Man controllers against the default ghost agent.
        # Apply parsimony pressure as a second objective to be minimized, rather than a penalty.
        # Sample call: score, log = play_GPac(controller, **kwargs)
        for individual in population:
            # Evaluate the controller
            score, log = play_GPac(individual.genes, **kwargs)
            # Calculate tree size
            size = individual.genes.count_nodes(individual.genes.root)
            
            individual.base_fitness = score
            individual.log = log
            individual.fitness = (score, size)  

            
    elif experiment.casefold() == 'red1':
        # RED1: Evaluate a population of Pac-Man controllers against the default ghost agent.
        # Use the score vectors to calculate fitness sharing.
        # Sample call: score, log, score_vector = play_GPac(controller, score_vector=True, **kwargs)
        for individual in population:
            # Evaluate individual 
            score, log, score_vector = play_GPac(individual.genes, score_vector=True, **kwargs)
            individual.base_fitness = score
            individual.log = log
            individual.score_vector = score_vector

        # Apply parsimony pressure 
        for individual in population:
            size = individual.genes.count_nodes(individual.genes.root)
            penalized_fitness = individual.base_fitness - size * parsimony_coefficient

            # Fitness sharing
            distances = [
                phenotype_distance(individual.score_vector, other.score_vector)
                for other in population
            ]
            sharing_factor = sum(sharing_function(d, sigma, alpha) for d in distances)
            individual.fitness = penalized_fitness / sharing_factor



    elif experiment.casefold() == 'red2':
        # RED2: Evaluate a population of Pac-Man controllers against the default ghost agent.
        # Sample call: score, log = play_GPac(controller, **kwargs)
         for individual in population:
             score, log = play_GPac(individual.genes, multi_agents=True, **kwargs)
             size = individual.genes.count_nodes(individual.genes.root)
             individual.base_fitness = score
             individual.fitness = score - size * parsimony_coefficient
             individual.log = log

    elif experiment.casefold() == 'red3':
        # RED3: Evaluate a population where each game has multiple different Pac-Man controllers.
        # You must write your own play_GPac_multicontroller function, and use that.

        num_agents = kwargs.get("num_agents", 4)  
        for individual in population:
            controllers = random.sample(population, k=num_agents)
            score, log = play_GPac_multicontroller(controllers, **kwargs)
            size = individual.genes.count_nodes(individual.genes.root)
            individual.base_fitness = score
            individual.fitness = score - size * parsimony_coefficient
            individual.log = log

    elif experiment.casefold() == 'red4':
        # RED4: Evaluate a population of ghost controllers against the default Pac-Man agent.
        # Sample call: score, log = play_GPac(None, controller, **kwargs)
        for individual in population:
            score, log = play_GPac(None, individual.genes, **kwargs)
            size = individual.genes.count_nodes(individual.genes.root)
            individual.base_fitness = -score 
            individual.fitness = individual.base_fitness - size * parsimony_coefficient
            individual.log = log
            
    elif experiment.casefold() == 'red5':
        # RED5: Evaluate a population where each game has multiple different ghost controllers.
        # You must write your own play_GPac_multicontroller function, and use that.
        num_ghosts = kwargs.get("num_ghosts", 4)  
        for individual in population:
            controllers = random.sample(population, k=num_ghosts)
            score, log = play_GPac_multicontroller(pac_controller=None, ghost_controllers=controllers, **kwargs)
            size = individual.genes.count_nodes(individual.genes.root)
            individual.base_fitness = -score
            individual.fitness = individual.base_fitness - size * parsimony_coefficient
            individual.log = log



    # This code will strip out unnecessary log member variables, to save your memory.
    # We remove the log from any individual that doesn't have a maximal fitness.
    max_fit = max(individual.fitness for individual in population)
    max_base_fit = max(individual.base_fitness for individual in population)
    for individual in population:
        if individual.fitness != max_fit and individual.base_fitness != max_base_fit:
            del individual.log
            individual.log = None

def sharing_function(distance, sigma, alpha=1.0):
    """Fitness sharing function based on distance."""
    if distance < sigma:
        return 1 - (distance / sigma) ** alpha
    return 0



def phenotype_distance(vector1, vector2):
    """Calculate Euclidean distance between two phenotype vectors."""
    return sum((x - y) ** 2 for x, y in zip(vector1, vector2)) ** 0.5



# 2c TODO: Perform competitive population evaluations as described in the Assignment 2c notebook.
def competitive_population_evaluation(pac_population, ghost_population,
                                      pac_parsimony_coefficient,
                                      ghost_parsimony_coefficient, **kwargs):
    # TODO: Perform matchmaking to generate pairs of individuals, one from each population.
    # Make sure to read the above description very carefully; matchmaking is not trivial,
    # and your submitted code MUST be able to handle arbitrary population sizes,
    # including cases where the two populations have different sizes.



    # TODO: Evaluate the matches with the play_Gpac function.
    # Hint: play_GPac(pac_controller, ghost_controller, **kwargs)



    # TODO: Calculate and assign fitness and base_fitness members.
    # Don't forget each population may have different parsimony coefficients,
    # and that you need to handle cases where an individual played multiple games.
    pass
