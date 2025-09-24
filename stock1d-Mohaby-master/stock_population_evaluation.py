
# stock_population_evaluation.py

from cutting_stock.fitness_functions import *

# 1b TODO: Evaluate the population and assign the fitness
# member variable as described in the Assignment 1b notebook
def base_population_evaluation(population, **kwargs):
    # Use base_fitness_function, i.e.,
    # base_fitness_function(individual.genes, **kwargs)
  
        
    for individual in population:
        fitness_result = base_fitness_function(individual.genes, **kwargs)
        
        if isinstance(fitness_result, dict) and 'fitness' in fitness_result:
            fitness_value = fitness_result['fitness']
        else:
            raise ValueError(f"Unexpected fitness result format: {fitness_result}")
        
        if not isinstance(fitness_value, (int, float)):
            raise ValueError(f"Fitness value must be numeric, got {fitness_value} of type {type(fitness_value)}")

        individual.fitness = fitness_value



# 1c TODO: Evaluate the population and assign the base_fitness, violations, and fitness
# member variables as described in the constraint satisfaction portion of Assignment 1c
def unconstrained_population_evaluation(population, penalty_coefficient, red=None, **kwargs):
    # Use unconstrained_fitness_function, i.e.,
    # unconstrained_fitness_function(individual.genes, **kwargs)
        # GREEN deliverable logic goes here
   if not red: 
        for individual in population:
            output = unconstrained_fitness_function(individual.genes, **kwargs)
            individual.base_fitness = output['base fitness']
            individual.violations = output['violations']
            individual.fitness = output['unconstrained fitness'] - individual.violations * penalty_coefficient

   else:
        pass

# 1d TODO: Evaluate the population and assign the objectives
# member variable as described in the multi-objective portion of Assignment 1d
def multiobjective_population_evaluation(population, yellow=None, **kwargs):
    # Evaluate each individual using the multiobjective fitness function
    for individual in population:
        fitness_output = multiobjective_fitness_function(individual.genes, **kwargs)

        if not yellow:
            # GREEN deliverable - 2 objectives
            individual.objectives = [fitness_output['length'], fitness_output['width']]
        else:
            # YELLOW deliverable - 3 objectives (length, width, shared edges)
            individual.objectives = [
                fitness_output['length'],
                fitness_output['width'],
                fitness_output.get('shared edges', 0) 
            ]




