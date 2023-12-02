from tmpcode import topla
import random
import os

for _ in range(100):
    a = random.randint(0, 100)
    b = random.randint(0, 100)
    open('tmpinput', 'w').write(f'topla({a}, {b})')
    open('tmpoutput', 'w').write(str(topla(a, b)))
    print(a+b)
    if a + b != topla(a, b):
        exit(1)
exit(0)
