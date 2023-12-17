import random
name = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz', 5))

select = random.randint(0, 2)
if select == 0:
    print(f'for {name} in range({random.randint(1, 20)}):')
elif select == 1:
    print(f'for {name} in range({random.randint(1, 10)}, {random.randint(11, 20)}):')
else:
    print(f'for {name} in range({random.randint(1, 10)}, {random.randint(11, 20)}, {random.randint(1, 5)}):')

