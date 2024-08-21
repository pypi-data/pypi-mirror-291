# genetic_algorithms/utilities.py

import random

def roulette_wheel_selection(population, fitness_values):
    """Selects a parent using roulette wheel selection."""
    total_fitness = sum(fitness_values)
    pick = random.uniform(0, total_fitness)
    current = 0
    for individual, fitness_value in zip(population, fitness_values):
        current += fitness_value
        if current > pick:
            return individual

def random_selection(population, num_parents):
    """Selects a random subset of parents from the population."""
    return random.sample(population, num_parents)

def calculate_average_fitness(fitness_values):
    """Calculates the average fitness of the population."""
    return sum(fitness_values) / len(fitness_values)
