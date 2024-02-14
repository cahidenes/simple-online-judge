n, m = [int(x) for x in input().split()]
mat = []
for i in range(n):
    mat.append([int(x)*9 for x in input().split()])

def valid(i, j):
    return i >= 0 and i < n and j >= 0 and j < m

for i in range(n):
    for j in range(m):
        if mat[i][j] == 9:
            continue
        for farki in [-1, 0, 1]:
            for farkj in [-1, 0, 1]:
                if valid(i+farki, j+farkj) and mat[i+farki][j+farkj] == 9:
                    mat[i][j] += 1

for i in range(n):
    for j in range(m):
        print(mat[i][j], end=" ")
    print()
