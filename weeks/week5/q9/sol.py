n, m = [int(x) for x in input().split()]
mat = []
for i in range(n):
    mat.append([int(x) for x in input().split()])

def bas(i, j):
    mat[i][j] ^= 1
    if i > 0:
        mat[i-1][j] ^= 1
    if i < n-1:
        mat[i+1][j] ^= 1
    if j > 0:
        mat[i][j-1] ^= 1
    if j < m-1:
        mat[i][j+1] ^= 1


for sol in range(2**m):
    solution = [[0 for _ in x] for x in mat]
    for i in range(m):
        if sol & (1 << i):
            bas(0, i)
            solution[0][i] = 1
    for i in range(1, n):
        for j in range(m):
            if mat[i-1][j]:
                bas(i, j)
                solution[i][j] = 1
    if all(all(x == 0 for x in row) for row in mat):
        for row in solution:
            print(' '.join(str(x) for x in row))
        exit(0)
    for i in range(n):
        for j in range(m):
            if solution[i][j]:
                bas(i, j)

