# siyah olan yerlerin 1, beyaz olan yerlerin 0 olduğu bir matris alıyor, basılması gereken yerlerin 1, basılmaması gereken yerlerin 0 olduğu bir matris döndürüyor.
def get_solution(mat):
    n, m = len(mat), len(mat[0])

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
            return solution
        for i in range(n):
            for j in range(m):
                if solution[i][j]:
                    bas(i, j)

