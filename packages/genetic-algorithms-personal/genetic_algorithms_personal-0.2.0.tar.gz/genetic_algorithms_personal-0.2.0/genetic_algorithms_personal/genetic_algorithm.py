import random
import concurrent.futures
import numpy as np

class GeneticAlgorithm:
    def __init__(self, population_size=100, genome_length=50, mutation_rate=0.01, crossover_rate=0.7, 
                 generations=5000, fitness_function=None, enable_debug=False, elitism_rate=0.01, 
                 early_stopping_rounds=100):
        self.population_size = population_size
        self.genome_length = genome_length
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.generations = generations
        self.fitness_function = fitness_function or self.default_fitness
        self.elitism_rate = elitism_rate
        self.early_stopping_rounds = early_stopping_rounds
        self.enable_debug = enable_debug
        self.population = self.init_population()
        self.best_fitness = -float('inf')
        self.stagnant_generations = 0

    def random_genome(self):
        return [random.randint(0, 1) for _ in range(self.genome_length)]

    def init_population(self):
        return [self.random_genome() for _ in range(self.population_size)]

    def default_fitness(self, genome):
        return sum(genome)

    def evaluate_fitness(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            return list(executor.map(self.fitness_function, self.population))

    def select_parent(self, fitness_values):
        total_fitness = sum(fitness_values)
        pick = random.uniform(0, total_fitness)
        current = 0
        for individual, fitness_value in zip(self.population, fitness_values):
            current += fitness_value
            if current > pick:
                return individual

    def crossover(self, parent1, parent2):
        if random.random() < self.crossover_rate:
            crossover_point = random.randint(1, len(parent1) - 1)
            return (parent1[:crossover_point] + parent2[crossover_point:], 
                    parent2[:crossover_point] + parent1[crossover_point:])
        return parent1, parent2

    def mutate(self, genome):
        return [abs(gene - 1) if random.random() < self.mutation_rate else gene for gene in genome]

    def moving_average(self, arr, window_size=10):
        """Calculate moving average to help with early stopping."""
        if len(arr) < window_size:
            return np.mean(arr)
        return np.mean(arr[-window_size:])

    def apply_elitism(self, fitness_values):
        elite_size = int(self.elitism_rate * self.population_size)
        elite_indices = sorted(range(len(fitness_values)), key=lambda i: fitness_values[i], reverse=True)[:elite_size]
        return [self.population[i] for i in elite_indices]

    def evolve(self):
        fitness_history = []
        for generation in range(self.generations):
            fitness_values = self.evaluate_fitness()

            current_best_fitness = max(fitness_values)
            if current_best_fitness > self.best_fitness:
                self.best_fitness = current_best_fitness
                self.stagnant_generations = 0
            else:
                self.stagnant_generations += 1

            fitness_history.append(current_best_fitness)
            average_fitness = self.moving_average(fitness_history, window_size=self.early_stopping_rounds)

            if self.stagnant_generations >= self.early_stopping_rounds and average_fitness == self.best_fitness:
                print(f"Stopping early due to lack of improvement for {self.early_stopping_rounds} generations.")
                break

            new_population = self.apply_elitism(fitness_values)

            while len(new_population) < self.population_size:
                parent1 = self.select_parent(fitness_values)
                parent2 = self.select_parent(fitness_values)
                offspring1, offspring2 = self.crossover(parent1, parent2)
                new_population.extend([self.mutate(offspring1), self.mutate(offspring2)])

            self.population = new_population[:self.population_size]

            if self.enable_debug:
                self.debug(generation, fitness_values)

        self.report_final_result(fitness_values)

    def debug(self, generation, fitness_values):
        average_fitness = sum(fitness_values) / len(fitness_values)
        print(f"Generation {generation}: Best Fitness = {self.best_fitness}, Average Fitness = {average_fitness}")

    def report_final_result(self, fitness_values):
        best_index = fitness_values.index(self.best_fitness)
        best_solution = self.population[best_index]
        print(f"Best Solution: {best_solution}")
        print(f"Best Fitness: {self.best_fitness}")

if __name__ == "__main__":
    # Standard Genetic Algorithm run
    ga = GeneticAlgorithm(population_size=100, genome_length=500, mutation_rate=0.01, crossover_rate=0.7, 
                          generations=5000, enable_debug=True, elitism_rate=0.05, early_stopping_rounds=200)
    ga.evolve()

    # Custom fitness function example
    def custom_fitness(genome):
        return genome.count(1) * 2 - genome.count(0)

    ga_custom = GeneticAlgorithm(population_size=100, genome_length=500, mutation_rate=0.01, crossover_rate=0.7, 
                                 generations=5000, fitness_function=custom_fitness, elitism_rate=0.05, 
                                 early_stopping_rounds=200)
    ga_custom.evolve()
