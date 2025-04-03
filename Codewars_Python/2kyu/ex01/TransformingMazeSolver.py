from collections import deque

def maze_solver(maze):
    rows, cols = len(maze), len(maze[0])
    directions = {'N': (-1, 0), 'W': (0, -1), 'S': (1, 0), 'E': (0, 1)}
    reverse_dir = {'N': 'S', 'W': 'E', 'S': 'N', 'E': 'W'}

    def rotate_walls(value):
        """Rotates the walls of a cell clockwise."""
        return ((value >> 1) | ((value & 1) << 3)) & 0b1111

    # Precompute wall rotations for each cell
    cell_rotations = {}
    for r in range(rows):
        for c in range(cols):
            cell = maze[r][c]
            if isinstance(cell, int):
                rotations = []
                for _ in range(4):
                    rotations.append(cell)
                    cell = rotate_walls(cell)
                cell_rotations[(r, c)] = rotations
            else:
                # Special cells (B or X) have no walls
                cell_rotations[(r, c)] = [0, 0, 0, 0]

    # Find start ('B') and destination ('X')
    start, destination = None, None
    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == 'B':
                start = (r, c)
            elif maze[r][c] == 'X':
                destination = (r, c)

    if not start or not destination:
        return []  # Start or destination not found

    # BFS to find the shortest path
    queue = deque([(start[0], start[1], 0, [])])  # (row, col, time, path)
    visited = set()

    while queue:
        row, col, time, path = queue.popleft()

        if (row, col) == destination:
            return path  # Reached destination

        cell_walls = cell_rotations[(row, col)][time % 4]
        state = (row, col, time % 4)
        if state in visited:
            continue
        visited.add(state)

        for d, (dr, dc) in directions.items():
            nr, nc = row + dr, col + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                next_cell_walls = cell_rotations[(nr, nc)][(time + 1) % 4]

                # Check if the move is valid
                if ((cell_walls >> "NWSE".index(d)) & 1) == 0 and ((next_cell_walls >> "NWSE".index(reverse_dir[d])) & 1) == 0:
                    queue.append((nr, nc, time + 1, path + [d]))

    return []  # No path found
