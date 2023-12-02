from tmpcode import carp
import random

for i in range(100):
    r = random.randint(0, 1000)
    k = random.randint(0, 1000)
    open('tmpinput', 'w').write(f'f = carp({r})\nf({k})')
    open('tmpoutput', 'w').write(str(carp(r)(k)))
    open('tmpexpected', 'w').write(str(k*r))
    if k*r != carp(r)(k):
        exit(1)

exit(0)
