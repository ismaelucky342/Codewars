import numpy as np
from functools import reduce

def minimum_transportation_price(suppliers, consumers, costs):
    # Initialize the solution table with None values
    rows, cols = len(costs), len(costs[0])
    sol_table = [[None for _ in range(cols)] for _ in range(rows)]
    
    # Get the initial basic feasible solution
    rows_basis_cells, columns_basis_cells, coords = get_basic_solution_min_price_method(sol_table, suppliers, consumers, costs)

    while True:
        # Calculate potentials for rows and columns
        u, v = find_potentials(costs, sol_table, rows_basis_cells, columns_basis_cells, coords)
        
        # Calculate deltas and find the maximum delta
        max_delta, j_max_d, i_max_d = deltas_calc(u, v, costs, cols)

        # If the maximum delta is less than or equal to 0, the solution is optimal
        if max_delta <= 0:
            break

        # Find the cycle path for the entering variable
        path = get_cycle_path(j_max_d, i_max_d, rows_basis_cells, columns_basis_cells)
        
        # Recount the cycle to update the solution table
        cycle_recounting(path, sol_table, rows_basis_cells, columns_basis_cells)

    # Calculate the total minimum transportation cost
    return sum(sum(sol_table[cell[0]][cell[1]] * costs[cell[0]][cell[1]] for cell in row_cells) for row_cells in rows_basis_cells)

def get_basic_solution_min_price_method(table, suppliers, consumers, costs):
    # Create a sorted queue of cells based on cost in descending order
    cells_queue = sorted([(j, i) for i in range(len(costs[0])) for j in range(len(costs))], key=lambda x: costs[x[0]][x[1]], reverse=True)
    
    # Initialize basis cells for rows and columns
    rows_basis_cells = [[] for _ in range(len(costs))]
    columns_basis_cells = [[] for _ in range(len(costs[0]))]
    rows = set(range(len(costs)))
    cols = set(range(len(costs[0])))

    while cells_queue:
        curr_j, curr_i = cells_queue.pop()
        if curr_j not in rows or curr_i not in cols:
            continue

        # Allocate supply and demand to the current cell
        supply, demand = suppliers[curr_j], consumers[curr_i]
        allocation = min(supply, demand)
        table[curr_j][curr_i] = allocation
        rows_basis_cells[curr_j].append((curr_j, curr_i))
        columns_basis_cells[curr_i].append((curr_j, curr_i))

        # Update suppliers and consumers based on the allocation
        if supply == demand:
            suppliers[curr_j] = 0
            cols.remove(curr_i)
        elif supply < demand:
            suppliers[curr_j] = 0
            consumers[curr_i] -= supply
            rows.remove(curr_j)
        else:
            consumers[curr_i] = 0
            suppliers[curr_j] -= demand
            cols.remove(curr_i)

        if not rows or not cols:
            break

    # Initialize default values for j and i
    j, i = 0, 0

    # Handle degenerate case
    if sum(len(cells) for cells in rows_basis_cells) < len(costs) + len(costs[0]) - 1:
        aux_queue = sorted([(j, i) for i in range(len(costs[0])) for j in range(len(costs)) if table[j][i] is None], key=lambda x: costs[x[0]][x[1]])
        if aux_queue:
            j, i = aux_queue[0]
            table[j][i] = 0
            rows_basis_cells[j].append((j, i))
            columns_basis_cells[i].append((j, i))

    return rows_basis_cells, columns_basis_cells, (j, i)

def deltas_calc(u, v, costs, cols):
    # Calculate the deltas matrix
    deltas_matrix = np.array(v) + np.array(u)[:, None] - np.array(costs)
    
    # Find the maximum delta and its coordinates
    flat_index = np.argmax(deltas_matrix)
    j_max_d, i_max_d = divmod(flat_index, cols)
    return deltas_matrix[j_max_d][i_max_d], j_max_d, i_max_d

def find_potentials(costs, table, rows_basis_cells, columns_basis_cells, coords):
    # Initialize potentials for rows and columns
    u = [None] * len(costs)
    v = [None] * len(costs[0])
    u[0] = 0

    def row_search(row):
        for cell in rows_basis_cells[row]:
            if v[cell[1]] is None and u[row] is not None:
                v[cell[1]] = costs[row][cell[1]] - u[row]
                column_search(cell[1])

    def column_search(column):
        for cell in columns_basis_cells[column]:
            if u[cell[0]] is None and v[column] is not None:
                u[cell[0]] = costs[cell[0]][column] - v[column]
                row_search(cell[0])

    row_search(0)

    # Handle degenerate case
    if None in u or None in v:
        j_unknowns = [j for j, el in enumerate(u) if el is None]
        i_unknowns = [i for i, el in enumerate(v) if el is None]
        possible_placements = [(j, i) for j in j_unknowns for i in range(len(costs[0])) if table[j][i] is None] + \
                             [(j, i) for i in i_unknowns for j in range(len(costs)) if table[j][i] is None]
        possible_placements.sort(key=lambda x: costs[x[0]][x[1]])
        j, i = possible_placements[0]
        table[coords[0]][coords[1]] = None
        rows_basis_cells[coords[0]].remove(coords)
        columns_basis_cells[coords[1]].remove(coords)
        table[j][i] = 0
        rows_basis_cells[j].append((j, i))
        columns_basis_cells[i].append((j, i))
        row_search(j)
        column_search(i)

    return u, v

def cycle_recounting(cycle_path, table, rows_basis_cells, columns_basis_cells):
    # Find the minimum element in the cycle path
    min_el_coords = min([cycle_path[i] for i in range(1, len(cycle_path), 2)], key=lambda x: table[x[0]][x[1]])
    min_el = table[min_el_coords[0]][min_el_coords[1]]
    
    # Update the solution table based on the cycle path
    table[cycle_path[0][0]][cycle_path[0][1]] = min_el
    table[min_el_coords[0]][min_el_coords[1]] = None
    rows_basis_cells[min_el_coords[0]].remove(min_el_coords)
    columns_basis_cells[min_el_coords[1]].remove(min_el_coords)

    for index, cell in enumerate(cycle_path):
        if cell != min_el_coords and index:
            if index % 2 == 0:
                table[cell[0]][cell[1]] += min_el
            else:
                table[cell[0]][cell[1]] -= min_el

def get_cycle_path(start_j, start_i, row_basis_cells, columns_basis_cells):
    get_cycle_path.cycle_path = []
    row_basis_cells[start_j].append((start_j, start_i))
    columns_basis_cells[start_i].append((start_j, start_i))

    def row_search(row, curr_path):
        for cell in row_basis_cells[row]:
            if cell == (start_j, start_i) and len(curr_path) > 1:
                get_cycle_path.cycle_path = curr_path.copy()
                return
            if cell not in curr_path:
                column_search(cell[1], curr_path + [cell])

    def column_search(column, curr_path):
        for cell in columns_basis_cells[column]:
            if cell == (start_j, start_i) and len(curr_path) > 1:
                get_cycle_path.cycle_path = curr_path.copy()
                return
            if cell not in curr_path:
                row_search(cell[0], curr_path + [cell])

    row_search(start_j, [(start_j, start_i)])
    return get_cycle_path.cycle_path