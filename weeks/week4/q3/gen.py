import random
s = set()
for _ in range(random.randint(10, 20)):
    s.add(random.randint(1, 20))

for i in s:
    print(i, end=' ')
print()

print(random.randint(20, 60))
