def get_fours():
    a = []
    for i in range(3):
        for j in range(7):
            a.append([(i, j), (i+1, j), (i+2, j), (i+3, j)])

    for i in range(6):
        for j in range(4):
            a.append([(i, j), (i, j+1), (i, j+2), (i, j+3)])

    for i in range(3):
        for j in range(4):
            a.append([(i, j), (i+1, j+1), (i+2, j+2), (i+3, j+3)])
            a.append([(i+3, j), (i+2, j+1), (i+1, j+2), (i, j+3)])

    return a


def get_winner(board):
    for four in get_fours():
        for i, j in four:
            if board[i][j] != 1:
                break
        else:
            return 1
        for i, j in four:
            if board[i][j] != -1:
                break
        else:
            return -1
    return 0


def get_available(board):
    available = []
    for j in range(7):
        if board[0][j] == 0:
            available.append(j)
    return available

def simulate_move(board, place, player):
    tmp = copy_board(board)
    for i in range(5, -1, -1):
        if tmp[i][place] == 0:
            tmp[i][place] = player
            break
    else:
        raise Exception("Invalid move")
    return tmp

def copy_board(board):
    tmp = []
    for i in range(6):
        tmp.append([])
        for j in range(7):
            tmp[i].append(board[i][j])
    return tmp

def print_board(board):
    print('-'*23)
    for i in range(6):
        print('|', end='')
        for j in range(7):
            if board[i][j] == 1:
                print(' X ', end='')
            elif board[i][j] == -1:
                print(' O ', end='')
            else:
                print(' . ', end='')
        print('|')
    print('-'*23)

