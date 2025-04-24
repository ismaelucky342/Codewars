import numpy as np
from functools import reduce

def minimum_transportation_price(suppliers, consumers, costs):
    filas, cols = len(costs), len(costs[0])
    sol_table = [[None for _ in range(cols)] for _ in range(filas)]
    
    uf, cc, vectors = precio_min(sol_table, suppliers, consumers, costs)

    while True:
        u, v = potenciales(costs, sol_table, uf, cc, vectors)
        
        max_delta, j_max_d, i_max_d = deltas_calc(u, v, costs, cols)
        if max_delta <= 0:
            break

        path = pathciclo(j_max_d, i_max_d, uf, cc)
        reconteo(path, sol_table, uf, cc)

    return sum(sum(sol_table[cell[0]][cell[1]] * costs[cell[0]][cell[1]] for cell in row_cells) for row_cells in uf)


def deltas_calc(u, v, costs, cols):
    matr_delta = np.array(v) + np.array(u)[:, None] - np.array(costs)
    flat_index = np.argmax(matr_delta)
    j_max_d, i_max_d = divmod(flat_index, cols)
    return matr_delta[j_max_d][i_max_d], j_max_d, i_max_d

def potenciales(costs, table, uf, cc, vectors):
    u = [None] * len(costs)
    v = [None] * len(costs[0])
    u[0] = 0

    def row_search(row):
        for cell in uf[row]:
            if v[cell[1]] is None and u[row] is not None:
                v[cell[1]] = costs[row][cell[1]] - u[row]
                column_search(cell[1])

    def column_search(column):
        for cell in cc[column]:
            if u[cell[0]] is None and v[column] is not None:
                u[cell[0]] = costs[cell[0]][column] - v[column]
                row_search(cell[0])

    row_search(0)
    if None in u or None in v:
        j_unknowns = [j for j, el in enumerate(u) if el is None]
        i_unknowns = [i for i, el in enumerate(v) if el is None]
        possible_placements = [(j, i) for j in j_unknowns for i in range(len(costs[0])) if table[j][i] is None] + \
                             [(j, i) for i in i_unknowns for j in range(len(costs)) if table[j][i] is None]
        possible_placements.sort(key=lambda x: costs[x[0]][x[1]])
        j, i = possible_placements[0]
        table[vectors[0]][vectors[1]] = None
        uf[vectors[0]].remove(vectors)
        cc[vectors[1]].remove(vectors)
        table[j][i] = 0
        uf[j].append((j, i))
        cc[i].append((j, i))
        row_search(j)
        column_search(i)

    return u, v

def pathciclo(start_j, start_i, row_basis_cells, cc):
    pathciclo.cycle_path = []
    row_basis_cells[start_j].append((start_j, start_i))
    cc[start_i].append((start_j, start_i))

    def row_search(row, curr_path):
        for cell in row_basis_cells[row]:
            if cell == (start_j, start_i) and len(curr_path) > 1:
                pathciclo.cycle_path = curr_path.copy()
                return
            if cell not in curr_path:
                column_search(cell[1], curr_path + [cell])

    def column_search(column, curr_path):
        for cell in cc[column]:
            if cell == (start_j, start_i) and len(curr_path) > 1:
                pathciclo.cycle_path = curr_path.copy()
                return
            if cell not in curr_path:
                row_search(cell[0], curr_path + [cell])

    row_search(start_j, [(start_j, start_i)])
    return pathciclo.cycle_path

def reconteo(cycle_path, table, uf, cc):
    min_el_vectors = min([cycle_path[i] for i in range(1, len(cycle_path), 2)], key=lambda x: table[x[0]][x[1]])
    min_el = table[min_el_vectors[0]][min_el_vectors[1]]
    table[cycle_path[0][0]][cycle_path[0][1]] = min_el
    table[min_el_vectors[0]][min_el_vectors[1]] = None
    uf[min_el_vectors[0]].remove(min_el_vectors)
    cc[min_el_vectors[1]].remove(min_el_vectors)

    for index, cell in enumerate(cycle_path):
        if cell != min_el_vectors and index:
            if index % 2 == 0:
                table[cell[0]][cell[1]] += min_el
            else:
                table[cell[0]][cell[1]] -= min_el

def precio_min(table, suppliers, consumers, costs):
    cells_queue = sorted([(j, i) for i in range(len(costs[0])) for j in range(len(costs))], key=lambda x: costs[x[0]][x[1]], reverse=True)
    
    uf = [[] for _ in range(len(costs))]
    cc = [[] for _ in range(len(costs[0]))]
    filas = set(range(len(costs)))
    cols = set(range(len(costs[0])))

    while cells_queue:
        curr_j, curr_i = cells_queue.pop()
        if curr_j not in filas or curr_i not in cols:
            continue

        supply, demand = suppliers[curr_j], consumers[curr_i]
        allocation = min(supply, demand)
        table[curr_j][curr_i] = allocation
        uf[curr_j].append((curr_j, curr_i))
        cc[curr_i].append((curr_j, curr_i))

        if supply == demand:
            suppliers[curr_j] = 0
            cols.remove(curr_i)
        elif supply < demand:
            suppliers[curr_j] = 0
            consumers[curr_i] -= supply
            filas.remove(curr_j)
        else:
            consumers[curr_i] = 0
            suppliers[curr_j] -= demand
            cols.remove(curr_i)

        if not filas or not cols:
            break
    j, i = 0, 0

    if sum(len(cells) for cells in uf) < len(costs) + len(costs[0]) - 1:
        aux_queue = sorted([(j, i) for i in range(len(costs[0])) for j in range(len(costs)) if table[j][i] is None], key=lambda x: costs[x[0]][x[1]])
        if aux_queue:
            j, i = aux_queue[0]
            table[j][i] = 0
            uf[j].append((j, i))
            cc[i].append((j, i))

    return uf, cc, (j, i)
