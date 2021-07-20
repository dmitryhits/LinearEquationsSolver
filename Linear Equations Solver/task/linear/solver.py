import argparse
from copy import deepcopy


swapped_columns = []


def set_non_zero_diagonal(m):
    print('set_diag in', m)
    new_m = deepcopy(m)
    for i in range(len(new_m)):
        new_m = find_leading_non_zero(new_m, i)
        print('set diag loop', new_m)
    print('set_diag out', new_m)
    return new_m


def find_leading_non_zero(m, j):
    """finds leading non-zero element in jth row"""
    # first look for non-zero elements below the j,j element
    # print('find lead non-zero in:', m)
    for i in range(j, len(m)):
        if m[i][j] == 0:
            # print('lead non-zero', i, j, m[i][j])
            continue
        # if non-zero element found in the ith row swap it with jth
        elif m[i][j] != 0 and i != j:
            return swap_rows(m, i, j)
    # if all elements below j,j are zero look for non-zero element to the right of j,j
    else:
        print('before second loop')
        for i in range(j, len(m[j]) - 1):
            if m[j][i] == 0:
                continue
            # if non-zero element found in the ith column swap it with jth
            elif m[j][i] != 0 and j != i:
                swapped_columns.append((j, i))
                return swap_columns(m, i, j)
        # if there are only zeros to the right and below j,j element then look in the lower right corner
        else:
            print('before third loop')
            if j + 1 < len(m) and j + 1 < len(m[j]) - 1:
                for i in range(j + 1,  len(m)):
                    for k in range(j + 1, len(m[j]) - 1):
                        if m[i][k] != 0:
                            swapped_columns.append((j, k))
                            return swap_rows(swap_columns(m, j, k), j, i)
                        else:
                            continue
                else:
                    print('default return 1')
                    return m
            else:
                print('default return 2')
                return m


def swap_columns(m, i, j):
    #print('swap col in', m)
    new_m = deepcopy(m)
    for k in range(len(m)):
        new_m[k][i] = m[k][j]
        new_m[k][j] = m[k][i]
    #print('swap col out', new_m)
    return new_m


def swap_rows(m, i, j):
    # print('swap rows in', m)
    new_m = deepcopy(m)
    new_m[i] = m[j].copy()
    new_m[j] = m[i].copy()
    # print('swap rows out', new_m)
    return new_m


def subtract_ith_row(m, i):
    new_m = []
    new_ith_row = [c / m[i][i] for c in m[i]]
    for n, row in enumerate(m):
        if n == i:
            new_m.append(new_ith_row)
            continue
        else:
            new_row = [c - c0 * row[i] for c, c0 in zip(row, new_ith_row)]
            new_m.append(new_row)
    return new_m


def triangulize(m):
    print('tiang in', m)
    new_m = set_non_zero_diagonal(m)
    for i in range(min(len(new_m), len(new_m[0]) - 1)):
        if new_m[i][i] != 0:
            new_m = subtract_ith_row(new_m, i)
        else:
            continue
    print('tiang out', new_m)
    return new_m


def check_if_solvable(m):
    new_m = triangulize(m)
    n_nonzero_rows = 0
    for i in range(len(new_m)):
        # if all elements in the row are zero but the last element is not then there are no solution
        #print('solvable?')
        print('solvable', new_m[i])
        if not any(new_m[i][:-1]) and new_m[i][-1]:
            return 'No solutions'
        # else if there are any non zero element in the row count it as a non-zeo row
        elif any(new_m[i]):
            n_nonzero_rows += 1
    # keep only non-zero rows
    new_m = new_m[:n_nonzero_rows]
    if len(new_m) == len(new_m[0]) - 1:
        # print('zeros removed', new_m)
        return new_m
    elif len(new_m) < len(new_m[0]) - 1:
        return 'Infinitely many solutions'
    else:
        return 'No solutions'


def diagonalize(m):
    out = check_if_solvable(m)
    if type(out) == list:
        new_m = out
    else:
        return out
    for i in reversed(range(len(new_m))):
        new_m = subtract_ith_row(new_m, i)
    # print('diag out')
    # print(new_m)
    return new_m


def solution(m, n):
    out_solution = {}
    out = diagonalize(m)
    if type(out) == list:
        new_m = out
    else:
        return out
    print('before re-swap', new_m)
    if swapped_columns:
        print('swapped', swapped_columns)
        for i, j in reversed(swapped_columns):
            new_m = swap_columns(new_m, i, j)

    print('sol after reswap', new_m)
    for i in range(n):
        # print(new_m[i])
        out_solution[new_m[i].index(1)] = new_m[i][-1]
    return out_solution


def read_in_matrix(infile_path):
    in_matrix = []
    with open(infile_path) as f_in:
        # read the first line
        n_vars, n_rows = map(int, f_in.readline().split())
        print('n vars:', n_vars, 'n rows:', n_rows)
        # read the rest of the lines
        for line in f_in:
            # print(line)
            in_matrix.append(list(map(read_in_complex, line.split())))
    print('in matrix', in_matrix)
    return in_matrix, n_vars


def read_in_complex(c):
    if 'j' in c:
        return complex(c)
    else:
        return float(c)


def write_out_solution(file_out, out_solution):
    with open(file_out, 'w') as f_out:
        if type(out_solution) == dict:
            for key in sorted(out_solution):
                print('key:', key, 'sol:', out_solution[key])
                f_out.write(str(out_solution[key]) + '\n')
        else:
            print(out_solution)
            f_out.write(out_solution + '\n')



parser = argparse.ArgumentParser()
parser.add_argument('--infile')
parser.add_argument('--outfile')
args = parser.parse_args()
infile = args.infile
outfile = args.outfile

matrix, n_variables = read_in_matrix(infile)
solution_list = solution(matrix, n_variables)
write_out_solution(outfile, solution_list)
