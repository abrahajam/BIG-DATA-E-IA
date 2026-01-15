import random
import numpy as np
from collections import deque

# Constantes públicas (las usaremos en el entorno)
WIDTH = 15
HEIGHT = 15
BUILDING = 0
ROAD = 1
DOOR = 2
START = 3
BUILDING_DENSITY = 0.3


def all_roads_connected(grid):
    start = None
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if grid[y][x] in (ROAD, START):
                start = (x, y)
                break
        if start:
            break
    if not start:
        return True

    visited = set([start])
    queue = deque([start])
    while queue:
        x, y = queue.popleft()
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
                if grid[ny][nx] in (ROAD, START) and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny))

    total_roads = sum(1 for y in range(HEIGHT)
                      for x in range(WIDTH) if grid[y][x] in (ROAD, START))
    return len(visited) == total_roads


def count_road_neighbors(grid, x, y):
    count = 0
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
            if grid[ny][nx] in (ROAD, START):
                count += 1
    return count


def remove_dead_ends(grid):
    changed = True
    while changed:
        changed = False
        for y in range(1, HEIGHT - 1):
            for x in range(1, WIDTH - 1):
                if grid[y][x] == ROAD:
                    if count_road_neighbors(grid, x, y) <= 1:
                        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
                        random.shuffle(directions)
                        opened = False
                        for dx, dy in directions:
                            nx, ny = x + dx, y + dy
                            if grid[ny][nx] == BUILDING:
                                grid[ny][nx] = ROAD
                                if all_roads_connected(grid):
                                    opened = True
                                    changed = True
                                    break
                                else:
                                    grid[ny][nx] = BUILDING
                        if not opened:
                            grid[y][x] = BUILDING
                            changed = True


def generate_map():
    # 1. Crear base
    grid = [[BUILDING for _ in range(WIDTH)] for _ in range(HEIGHT)]

    # 2. Laberinto DFS
    start_x, start_y = random.randrange(
        1, WIDTH, 2), random.randrange(1, HEIGHT, 2)
    grid[start_y][start_x] = ROAD
    stack = [(start_x, start_y)]
    directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]

    while stack:
        x, y = stack[-1]
        random.shuffle(directions)
        carved = False
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 1 <= nx < WIDTH - 1 and 1 <= ny < HEIGHT - 1:
                if grid[ny][nx] == BUILDING:
                    grid[ny][nx] = ROAD
                    grid[y + dy // 2][x + dx // 2] = ROAD
                    stack.append((nx, ny))
                    carved = True
                    break
        if not carved:
            stack.pop()

    # 3. Ensanchar y Densidad
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if grid[y][x] == ROAD and random.random() < 0.25:
                for dx, dy in random.sample([(1, 0), (-1, 0), (0, 1), (0, -1)], 2):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
                        grid[ny][nx] = ROAD

    road_cells = [(x, y) for y in range(1, HEIGHT-1)
                  for x in range(1, WIDTH-1) if grid[y][x] == ROAD]
    random.shuffle(road_cells)
    removals = int(len(road_cells) * BUILDING_DENSITY)
    for x, y in road_cells[:removals]:
        grid[y][x] = BUILDING
        if not all_roads_connected(grid):
            grid[y][x] = ROAD

    remove_dead_ends(grid)

    # 4. Puertas (Objetivos)
    doors = 0
    while doors < 3:
        x, y = random.randint(1, WIDTH-2), random.randint(1, HEIGHT-2)
        if grid[y][x] == BUILDING:
            if any(grid[y+dy][x+dx] == ROAD for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]):
                grid[y][x] = DOOR
                doors += 1

    # 5. Inicio
    roads = [(x, y) for y in range(HEIGHT)
             for x in range(WIDTH) if grid[y][x] == ROAD]
    if roads:
        sx, sy = random.choice(roads)
        grid[sy][sx] = START
    else:
        grid[0][0] = START

    # CONVERTIR A NUMPY PARA EL ENTORNO GYM
    return np.array(grid)
