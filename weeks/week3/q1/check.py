from tmpcode import alan
import random
import os

for _ in range(100):
    a = random.randint(0, 100)
    b = random.randint(0, 100)
    open('tmpinput', 'w').write(f'alan({a}, {b})')
    open('tmpoutput', 'w').write(str(alan(a, b)))
    print(a*b, 2*(a+b))
    if (a*b, 2*(a+b)) != alan(a, b):
        exit(1)

for _ in range(100):
    a = random.randint(0, 100)
    open('tmpinput', 'w').write(f'alan({a})')
    open('tmpoutput', 'w').write(str(alan(a)))
    print(a*a, 2*(a+a))
    if (a*a, 2*(a+a)) != alan(a):
        exit(1)
exit(0)
