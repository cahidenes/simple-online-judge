import random
import chess

while True:
    try:
        b = chess.Board()
        for _ in range(random.randint(20, 40)):
            moves = list(b.legal_moves)
            if len(moves) == 0:
                raise Exception
            b.push(random.choice(moves))
        print(b.fen())
        break
    except:
        continue
