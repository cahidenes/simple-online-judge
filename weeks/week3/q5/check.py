from tmpcode import topla
import random

for i in range(100):
    l = random.sample(range(100), random.randint(1, 100))
    if topla(*l) != sum(l):
        exit(1)

exit(0)
