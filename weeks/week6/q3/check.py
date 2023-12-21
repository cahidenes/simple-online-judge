from tmpcode import asalmi
import random

def asal(n):
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

for i in range(100):
    n = random.randint(1, 100)
    open('tmpinput', 'w').write(f'asalmi({n})')
    open('tmpexpected', 'w').write(f'{asal(n)}')
    cevap = asalmi(n)
    open('tmpoutput', 'w').write(f'{cevap}')
    if cevap != asal(n):
        exit(1)
exit(0)


