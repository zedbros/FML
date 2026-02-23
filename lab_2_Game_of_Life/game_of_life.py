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

def glider_initialize_grid(grid):
    grid[0][1] = 1
    grid[1][2] = 1
    grid[2][0] = 1
    grid[2][1] = 1
    grid[2][2] = 1

def beehive_initialize_grid(grid):
    # place la ruche en position (4,4)
    grid[4][5] = 1
    grid[4][6] = 1
    grid[5][4] = 1
    grid[5][7] = 1
    grid[6][5] = 1
    grid[6][6] = 1

def taod_initialize_grid(grid):
    # place le toad en position (4,4)
    grid[4][5] = 1
    grid[4][6] = 1
    grid[4][7] = 1
    grid[5][4] = 1
    grid[5][5] = 1
    grid[5][6] = 1

def pulsar_initialize_grid(grid):
    # première rangée horizontale de bras
    grid[2][4] = 1; grid[2][5] = 1; grid[2][6] = 1
    grid[2][10] = 1; grid[2][11] = 1; grid[2][12] = 1
    # partie haute
    grid[4][2] = 1; grid[4][7] = 1; grid[4][9] = 1; grid[4][14] = 1
    grid[5][2] = 1; grid[5][7] = 1; grid[5][9] = 1; grid[5][14] = 1
    grid[6][2] = 1; grid[6][7] = 1; grid[6][9] = 1; grid[6][14] = 1
    # partie basse symétrique
    grid[7][4] = 1; grid[7][5] = 1; grid[7][6] = 1; grid[7][10] = 1; grid[7][11] = 1; grid[7][12] = 1
    grid[9][4] = 1; grid[9][5] = 1; grid[9][6] = 1; grid[9][10] = 1; grid[9][11] = 1; grid[9][12] = 1
    grid[10][2] = 1; grid[10][7] = 1; grid[10][9] = 1; grid[10][14] = 1
    grid[11][2] = 1; grid[11][7] = 1; grid[11][9] = 1; grid[11][14] = 1
    grid[12][2] = 1; grid[12][7] = 1; grid[12][9] = 1; grid[12][14] = 1
    # rangée horizontale basse (mi-oscillation)
    grid[14][4] = 1; grid[14][5] = 1; grid[14][6] = 1; grid[14][10] = 1; grid[14][11] = 1; grid[14][12] = 1

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
