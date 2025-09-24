
# genetic_programming.py

import random
from base_evolution import BaseEvolutionPopulation

class GeneticProgrammingPopulation(BaseEvolutionPopulation):
    def generate_children(self):
        children = []
        recombined_child_count = 0
        mutated_child_count = 0

        # 2b TODO: Generate self.num_children children by either:
        #          recombining two parents OR
        #          generating a mutated copy of a single parent.
        #          Use self.mutation_rate to decide how each child should be made.
        #          Use your Assignment Series 1 generate_children function as a reference.
        #          Count the number of recombined/mutated children in the provided variables.
        while len(children) < self.num_children:
            if random.random() < self.mutation_rate:
                # Mutation
                parent = self.parent_selection(
                    self.population, n=1, **self.parent_selection_kwargs
                )[0]
                mutated_child = parent.mutate(**self.mutation_kwargs)
                children.append(mutated_child)
                mutated_child_count += 1
            else:
                # Recombination
                parents = self.parent_selection(
                    self.population, n=2, **self.parent_selection_kwargs
                )
                child = parents[0].recombine(parents[1], **self.recombination_kwargs)
                children.append(child)
                recombined_child_count += 1


        self.log.append(f'Number of children: {len(children)}')
        self.log.append(f'Number of recombinations: {recombined_child_count}')
        self.log.append(f'Number of mutations: {mutated_child_count}')

        return children