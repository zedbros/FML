#########################################
# Code pour lab_2_game_of_life
# version 1.8
# Renaud Richardet, ISC-HEVS
#########################################

import copy
import time
import os

# Taille de la grille
WIDTH, HEIGHT = 50, 30

# Initialiser un canevas vide (0 pour une cellule morte, 1 pour vivante)
def create_empty_grid():
    return [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

# Configuration initiale
def initialize_grid(grid):
    # On place un oscillateur "blinker" par exemple:
    grid[4][5] = 1
    grid[4][6] = 1
    grid[4][7] = 1

def count_neighbors(grid, row, col):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0: 
                continue
            r = (row + i) % HEIGHT
            c = (col + j) % WIDTH
            count += grid[r][c]
    return count

# Mettre à jour la grille (une itération)
def update_grid(grid):
    new_grid = create_empty_grid()
    for i in range(HEIGHT):
        for j in range(WIDTH):
            neighbors = count_neighbors(grid, i, j)
            # Règles de survie
            if grid[i][j] == 1:
                new_grid[i][j] = 1 if neighbors in [2, 3] else 0
            else:
                new_grid[i][j] = 1 if neighbors == 3 else 0
    return new_grid

# Afficher la grille dans la console
def print_grid(grid, generation):
    os.system('cls' if os.name == 'nt' else 'clear') # efface grille précédente
    print(f"Generation {generation}")
    for row in grid:
        print(''.join(['█' if cell == 1 else ' ' for cell in row]))

if __name__ == "__main__":
    grid = create_empty_grid()
    initialize_grid(grid)
    generation = 0
    while True:
        print_grid(grid, generation)
        grid = update_grid(grid)
        generation += 1
        time.sleep(0.5)
