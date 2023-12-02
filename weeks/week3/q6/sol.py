def kutu(en=10, boy=10, karakter='#', ic='bos', bosluk=' '):
    s = ''
    for i in range(boy):
        for j in range(en):
            s += karakter if i == 0 or j == 0 or i == boy-1 or j == en-1 or ic == 'dolu' else bosluk
        s += '\n'
    return s

