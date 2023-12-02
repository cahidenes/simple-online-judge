from tmpcode import kutu
import random

def mykutu(en=10, boy=10, karakter='#', ic='bos', bosluk=' '):
    s = ''
    for i in range(boy):
        for j in range(en):
            s += karakter if i == 0 or j == 0 or i == boy-1 or j == en-1 or ic == 'dolu' else bosluk
        s += '\n'
    return s

def ayar(**d):
    s = 'kutu('
    for k, v in d.items():
        s += '%s=%s, ' % (k, repr(v))
    s = s[:-2]
    s += ')'
    return s


for i in range(100):
    d = {}
    if random.randint(0, 1):
        d['en'] = random.randint(1, 20)
    if random.randint(0, 1):
        d['boy'] = random.randint(1, 20)
    if random.randint(0, 1):
        d['karakter'] = random.choice(['*', '#', '@', 'X', 'O'])
    if random.randint(0, 1):
        d['ic'] = random.choice(['dolu', 'bos'])
    if random.randint(0, 1):
        d['bosluk'] = random.choice([' ', '.', '-', '_'])
    open('tmpinput', 'w').write(ayar(**d))
    open('tmpoutput', 'w').write(kutu(**d))
    open('tmpexpected', 'w').write(mykutu(**d))
    if kutu(**d).strip() != mykutu(**d).strip():
        exit(1)
exit(0)
