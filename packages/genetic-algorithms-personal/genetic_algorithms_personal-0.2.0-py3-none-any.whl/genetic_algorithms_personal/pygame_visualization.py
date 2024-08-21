# genetic_algorithms/pygame_visualization.py

import pygame
import sys
from genetic_algorithms_personal.genetic_algorithm import GeneticAlgorithm

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GENOME_LENGTH = 50
CELL_SIZE = 10
FPS = 10

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Genetic Algorithm Visualization")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Draw the population
def draw_population(population, generation):
    screen.fill(WHITE)
    for idx, genome in enumerate(population):
        for gene_idx, gene in enumerate(genome):
            color = GREEN if gene == 1 else BLACK
            pygame.draw.rect(
                screen,
                color,
                pygame.Rect(
                    gene_idx * CELL_SIZE,
                    idx * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                )
            )
    font = pygame.font.SysFont(None, 36)
    text = font.render(f'Generation: {generation}', True, BLACK)
    screen.blit(text, (10, SCREEN_HEIGHT - 40))
    pygame.display.flip()

# Main function to run the Genetic Algorithm with Pygame visualization
def run_genetic_algorithm_with_visualization():
    ga = GeneticAlgorithm(
        population_size=SCREEN_HEIGHT // CELL_SIZE,
        genome_length=GENOME_LENGTH,
        mutation_rate=0.01,
        crossover_rate=0.7,
        generations=500,
        enable_debug=False,
        elitism_rate=0.05,
        early_stopping_rounds=50
    )

    for generation in range(ga.generations):
        ga.evolve()
        draw_population(ga.population, generation)
        clock.tick(FPS)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Early stopping check
        if ga.stagnant_generations >= ga.early_stopping_rounds:
            break

    pygame.quit()

if __name__ == "__main__":
    run_genetic_algorithm_with_visualization()
