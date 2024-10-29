import heapq
import pygame
import sys
import time
from collections import deque

pygame.init()

# Constants
WIDTH, HEIGHT = 300, 300
TILE_SIZE = WIDTH // 3
FPS = 1  # Lower FPS for visualization of the solution
GOAL_STATE = '012345678'

# Directions for movement (Up, Down, Left, Right)
DIRECTIONS = {
    'Up': -3,
    'Down': 3,
    'Left': -1,
    'Right': 1
}

# Valid moves based on the index of the blank space (0)
VALID_MOVES = {
    0: ['Down', 'Right'],
    1: ['Down', 'Left', 'Right'],
    2: ['Down', 'Left'],
    3: ['Up', 'Down', 'Right'],
    4: ['Up', 'Down', 'Left', 'Right'],
    5: ['Up', 'Down', 'Left'],
    6: ['Up', 'Right'],
    7: ['Up', 'Left', 'Right'],
    8: ['Up', 'Left']
}

def get_blank_index(state):
    return state.index('0')

def count_inversions(state):
    inversions = 0
    state_list = [int(x) for x in state if x != '0']  # Ignoring the blank space when checking solvability
    for i in range(len(state_list)):
        for j in range(i + 1, len(state_list)):
            if state_list[i] > state_list[j]:
                inversions += 1
    return inversions


def generate_children(state):
    children = []
    blank_index = get_blank_index(state)

    for direction in VALID_MOVES[blank_index]:
        new_index = blank_index + DIRECTIONS[direction]
        if 0 <= new_index < 9:
            new_state_list = list(state)
            new_state_list[blank_index], new_state_list[new_index] = new_state_list[new_index], new_state_list[blank_index]
            new_state = ''.join(new_state_list)
            children.append((new_state))  # Return (new_state)

    return children


def draw(screen, state):
    screen.fill((255, 255, 255))
    for i in range(9):
        if state[i] != '0':
            x = (i % 3) * TILE_SIZE
            y = (i // 3) * TILE_SIZE
            pygame.draw.rect(screen, (0, 128, 255), (x, y, TILE_SIZE, TILE_SIZE))
            font = pygame.font.Font(None, 74)
            text = font.render(state[i], True, (255, 255, 255))
            screen.blit(text, (x + TILE_SIZE // 4, y + TILE_SIZE // 4))

    pygame.display.flip()

def manhattan_distance(state):
    # Calculate the Manhattan distance of the current state to the goal state
    distance = 0
    goal_positions = {str(i): (i // 3, i % 3) for i in range(9)}  # Goal positions for each tile
    
    for index, tile in enumerate(state):
        if tile != '0':  # Skip the blank tile
            current_pos = (index // 3, index % 3)
            goal_pos = goal_positions[tile]
            distance += abs(current_pos[0] - goal_pos[0]) + abs(current_pos[1] - goal_pos[1])

    return distance

def a_star(initial_state):
    # Priority queue stores (f_cost, g_cost, state, parent_state)
    priority_queue = [(manhattan_distance(initial_state), 0, initial_state, None)]
    visited = {initial_state: None}  # Map each state to its parent
    g_costs = {initial_state: 0}  # Cost from start to each state

    while priority_queue:
        # Pop the state with the lowest f-cost
        f_cost, g_cost, current_state, parent_state = heapq.heappop(priority_queue)
        visited[current_state] = parent_state  # Record the parent for path reconstruction

        # Check if we reached the goal state
        if current_state == GOAL_STATE:
            path = []
            while current_state is not None:
                path.append(current_state)
                current_state = visited[current_state]
            return path[::-1] , visited # Return path from start to goal

        # Generate successors
        for successor in generate_children(current_state):
            successor_g_cost = g_cost + 1  # Increment cost by 1 for each move

            if successor not in g_costs or successor_g_cost < g_costs[successor]:
                # Calculate new f-cost for successor
                g_costs[successor] = successor_g_cost
                f_cost = successor_g_cost + manhattan_distance(successor)
                heapq.heappush(priority_queue, (f_cost, successor_g_cost, successor, current_state))

    return None  # No solution found

def solve_puzzle(initial_state):
    start_time = time.time()  # Start timing 
    path, visited_states = a_star(initial_state)
    end_time = time.time()  # End timing 
    time_cost_BFS = end_time - start_time
    print(f"Time taken by BFS algorithm: {time_cost_BFS:.4f} seconds")

    # if path is None:
    #     print("No solution found.")
    #     return []

    # # Backtrack the path from goal state the initial state
    
    # current_state = goal_state

    # while current_state is not None:
    #     path.append(current_state)
    #     current_state = parent_map[current_state]  # Move to the parent state

    # path.reverse()  # Reverse the path to get it from initial to goal
    total_cost = len(path) - 1  # Cost is the number of moves
    print(f"Total cost (number of moves): {total_cost}")
    # for state in path:
    #     if state in visited_states:
    #         print(f"{state} is in visited states.")
    #     else:
    #         print(f"{state} is NOT in visited states!")
    print("Path to the goal:")
    print(path)  
    depth = len(path) - 1
    print(f"Depth of the solution: {depth}")
    print("Explored Nodes:", len(visited_states))
    
    return path

def main():
    initial_state = input("Enter the initial state of the puzzle 8 numbers where 0 is the blank space: ")
    if len(initial_state) != 9 or not all(char in '012345678' for char in initial_state):
        print("Enter exactly 9 digits (0-8).")
        initial_state = input("Enter the initial state of the puzzle 8 numbers where 0 is the blank space: ")
        return
    inversions = count_inversions(initial_state)
    if inversions % 2 != 0:
        print("This puzzle is unsolvable (odd number of inversions).")
        return

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("8-Puzzle Game")
    clock = pygame.time.Clock()

    solving = False
    solution_path = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Press Enter to solve
                    solving = True
                    solution_path = solve_puzzle(initial_state)

        if solving and solution_path:
            if solution_path:
                initial_state = solution_path.pop(0)  # Update state to next in solution path
            else:
                solving = False  # Stop solving when the path is finished

        draw(screen, initial_state)
        clock.tick(FPS)

if __name__ == "__main__":
    main()