import random
n, m = random.randint(3, 10), random.randint(3, 10)
print(n, m)
for i in range(n):
    for j in range(m):
        if random.randint(0, 5) == 0:
            print('1', end=' ')
        else:
            print('0', end=' ')
    print()

