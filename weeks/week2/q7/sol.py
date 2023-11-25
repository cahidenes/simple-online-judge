fen = input().split()[0]
for satir in fen.split('/'):
    for c in satir:
        if c.isdigit():
            print('. '*int(c), end='')
        else:
            print(c, end=' ')
    print()
