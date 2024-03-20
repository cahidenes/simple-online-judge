# matrixin içindeki sayılar 0'dan n*n-1'e kadar olmalıdır. Çözülmüş bulmaca: [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
# Çıktısı hamleler içeren bir liste, her hamle iki tuple dan oluşur: 1. tuple tutulacak blok, 2. tuple getirilecek blok
def solve(mat):
    solution = []
    n = len(mat)

    def move(x0, y0, x1, y1):
        if x0 == x1 and y0 == y1:
            return
        if x0 == x1:
            dif = y1 - y0
            if dif < 0:
                dif += len(mat)
            for _ in range(dif):
                tmp = mat[x0][-1]
                for j in range(len(mat)-2, -1, -1):
                    mat[x0][j+1] = mat[x0][j]
                mat[x0][0] = tmp
            solution.append((x0+n, dif))
        elif y0 == y1:
            dif = x1 - x0
            if dif < 0:
                dif += len(mat)
            for _ in range(dif):
                tmp = mat[-1][y0]
                for i in range(len(mat)-2, -1, -1):
                    mat[i+1][y0] = mat[i][y0]
                mat[0][y0] = tmp
            solution.append((y0, dif))
        else:
            print('cannot move', x0, y0, 'to', x1, y1)
            exit(1)


    def getpos(a, mat):
        for i in range(len(mat)):
            for j in range(len(mat)):
                if mat[i][j] == a:
                    return (i, j)
    for i in range(n):
        for j in range(n):
            if j == n-1:
                break
            posx, posy = getpos(i*n+j, mat)

            if j == 0 and posx == i:
                move(posx, posy, posx, n-2)
                continue

            if posx == i:
                move(posx, posy, posx, n-1)
                if i == 0:
                    move(posx, n-1, posx+1, n-1)
                    move(posx, n-1, posx, posy)
                    posx, posy = posx+1, n-1
                else:
                    move(posx, n-1, posx-1, n-1)
                    move(posx, n-1, posx, posy)
                    posx, posy = posx-1, n-1
            move(posx, posy, posx, n-1)
            move(posx, n-1, i, n-1)
            move(i, n-1, i, n-2)
    for a in range(2*n-1, n*(n-1), n):
        posx, posy = getpos(a, mat)
        if posy != n-1:
            move(n-1, n-1, n-2, n-1)
            move(n-1, n-2, n-1, n-1)
            move(n-1, n-1, n-2, n-1)
            move(n-1, n-1, n-1, n-2)
        move(posx, n-1, n-1, n-1)
        move(n-1, n-2, n-1, n-1)
        posx, posy = getpos(a-n, mat)
        move(posx, posy, n-2, n-1)
        move(n-1, n-1, n-1, n-2)
        posx, posy = getpos(n-1, mat)
    posx, posy = getpos(n-1, mat)
    move(posx, posy, 0, n-1)

    posx, posy = getpos(n*n-1, mat)
    if (posx, posy) != (n-1, n-1):
        move(posx, posy, n-1, n-1)
        move(posy, posx, n-1, n-1)
        move(n-1, n-1, posx, posy)
        move(n-1, n-1, posy, posx)

    islem = True
    while islem:
        islem = False
        for i in range(len(solution)-1, -1, -1):
            if solution[i][1] == 0:
                solution.pop(i)
                islem = True

        for i in range(len(solution)-2, -1, -1):
            if solution[i][0] == solution[i+1][0]:
                sum = solution[i][1] + solution[i+1][1]
                if sum >= n:
                    sum -= n
                solution[i] = (solution[i][0], sum)
                solution.pop(i+1)
                islem = True

    enson = []

    for line, dif in solution:
        if line < n:
            pose1 = (0, line)
            pose2 = (dif, line)
        else:
            pose1 = (line-n, 0)
            pose2 = (line-n, dif)

        enson.append((pose1, pose2))
    return enson

