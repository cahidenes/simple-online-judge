n, m = [int(x) for x in input().split()]
mat = []
for i in range(n):
    mat.append([int(x) for x in input().split()])


for sol in range(2**(n*m)):
    solution = [x[:] for x in mat]
    for i in range(n):
        for j in range(m):
            if sol & (1 << (i*m+j)):
                solution[i][j] = 1
            else:
                solution[i][j] = 0
    dogru = True
    for ii in range(n):
        for jj in range(m):
            son = mat[ii][jj] ^ solution[ii][jj]
            if ii > 0:
                son ^= solution[ii-1][jj]
            if ii < n-1:
                son ^= solution[ii+1][jj]
            if jj > 0:
                son ^= solution[ii][jj-1]
            if jj < m-1:
                son ^= solution[ii][jj+1]
            if son == 1:
                dogru = False
                break
        if not dogru:
            break
    if dogru:
        for i in range(n):
            print(" ".join([str(x) for x in solution[i]]))
        break

