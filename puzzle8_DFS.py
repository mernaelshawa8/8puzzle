import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 300, 300
TILE_SIZE = WIDTH // 3
FPS = 10  # Lower FPS for visualization of the solution
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


def dfs(initial_state):
    frontier = [initial_state]  # Initialize the stack with the initial state
    explored = set()  # to track visited states
    parent_map = {initial_state: None}  # map states to their parent states

    while frontier:
        current_state = frontier.pop()  # Lifo behavior
        if current_state == GOAL_STATE:
            return current_state, parent_map, len(explored)  # Return the goal state, parent map and number of visited states
        explored.add(current_state)

        for child in generate_children(current_state):
            if child not in explored and child not in parent_map:
                frontier.append(child)  # Add the successor state to the stack
                parent_map[child] = current_state  # Map the parent state

    return None, None, len(explored)  # Return None if no solution

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

def solve_puzzle(initial_state):
    start_time = time.time()  # Start timing 
    goal_state, parent_map, visited_states = dfs(initial_state)
    end_time = time.time()  # End timing 
    time_cost_DFS = end_time - start_time
    print(f"Time taken by DFS algorithm: {time_cost_DFS:.4f} seconds")

    if goal_state is None:
        print("No solution found.")
        return []

    # Backtrack the path from goal state the initial state
    path = []
    current_state = goal_state

    while current_state is not None:
        path.append(current_state)
        current_state = parent_map[current_state]  # Move to the parent state

    path.reverse()  # Reverse the path to get it from initial to goal
    total_cost = len(path) - 1  # Cost is the number of moves
    print(f"Total cost (number of moves): {total_cost}")
    print("Path to the goal:")
    print(len(path))  
    depth = len(path) - 1
    print(f"Depth of the solution: {depth}")
    print("Explored Nodes:", visited_states)
    
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