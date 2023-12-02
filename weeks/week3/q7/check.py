from tmpcode import get, set
import random

for i in range(100):
    r = random.randint(1, 200)
    set(r)
    open('tmpinput', 'w').write('set('+str(r)+')\nget()')
    open('tmpexpected', 'w').write(str(r))
    x = get()
    open('tmpoutput', 'w').write(str(x))
    if x != r:
        exit(1)

exit(0)
