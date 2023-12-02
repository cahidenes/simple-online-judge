from tmpcode import kontrol
import random
import os

for _ in range(100):
    a = random.randint(0, 100)
    fun = lambda x: x%2 == 0
    open('tmpinput', 'w').write(f'kontrol({a}, {fun})')
    open('tmpoutput', 'w').write(str(kontrol(a, fun)))
    print(True)
    if True != kontrol(a, fun):
        exit(1)

for _ in range(100):
    a = random.randint(0, 100)
    fun = lambda x: x%2 == 1
    open('tmpinput', 'w').write(f'kontrol({a}, {fun})')
    open('tmpoutput', 'w').write(str(kontrol(a, fun)))
    print(False)
    if False != kontrol(a, fun):
        exit(1)
exit(0)
