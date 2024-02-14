from tmpcode import make_move
import helper, random
import time

def computer_move(board):
    for sutun in helper.get_available(board):
        oynadim = helper.simulate_move(board, sutun, 1)
        if helper.get_winner(oynadim) == 1:
            return sutun

    for sutun in helper.get_available(board):
        oynadi = helper.simulate_move(board, sutun, -1)
        if helper.get_winner(oynadi) == -1:
            return sutun

    return random.choice(helper.get_available(board))

def invert_board(board):
    return [[-x for x in row] for row in board]

score = 0
for i in range(10):
    board = [[0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0]]
    for movecount in range(1000):
        if (i+movecount) % 2:
            start = time.time()
            playermove = make_move(board)
            end = time.time()
            if end - start > 1:
                print('Ohoo sen oynayana kadar süre bitti')
                exit(1)
            if playermove not in helper.get_available(board):
                break
            board = helper.simulate_move(board, playermove, 1)
        else:
            computermove = computer_move(invert_board(board))
            board = helper.simulate_move(board, computermove, -1)
        if helper.get_winner(board) != 0:
            if helper.get_winner(board) == 1:
                score += 1
            break
        if helper.get_available == []:
            score += 0.5
            break

print('10 oyunda puanın', score)
print('Maalesef botun bir çöp')
if score >= 8:
    exit(0)
else:
    exit(1)



